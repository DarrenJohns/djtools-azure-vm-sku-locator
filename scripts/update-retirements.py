#!/usr/bin/env python3
"""Refresh VM family retirement records from Microsoft's lifecycle table."""

import json
import os
import sys
from datetime import date, datetime
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(SCRIPT_DIR, "..", "data", "retirements.json")
RETIREMENT_PAGE = (
    "https://learn.microsoft.com/en-us/azure/virtual-machines/sizes/lifecycle/"
    "retirements-and-capacity-restrictions"
)

# These are exact Azure family identifiers emitted by normalize-skus.py.
# Dedicated Host entries are intentionally excluded: they are not VM SKU families.
SERIES_TO_FAMILIES = {
    "D-series": ["standarddfamily"],
    "Ds-series": ["standarddsfamily"],
    "Dv2-series": ["standarddv2family", "standarddv2promofamily"],
    "Dsv2-series": ["standarddsv2family", "standarddsv2promofamily"],
    "Av2/Amv2-series": ["standardav2family", "standardamv2family"],
    "B-series (V1)": ["standardbsfamily"],
    "Dv3-series": ["standarddv3family"],
    "Dsv3-series": ["standarddsv3family"],
    "DCsv2-series": ["standarddcsv2family"],
    "DCas_cc_v5/DCads_cc_v5-series": [
        "standarddcaccv5family",
        "standarddcadccv5family",
    ],
    "DCsv3/DCdsv3-series": ["standarddcsv3family", "standardddcsv3family"],
    "F-series": ["standardffamily"],
    "Fs-series": ["standardfsfamily"],
    "Fsv2-series": ["standardfsv2family"],
    "G-series": ["standardgfamily"],
    "Gs-series": ["standardgsfamily"],
    "Ev3-series": ["standardev3family"],
    "Esv3-series": ["standardesv3family"],
    "Standard_M192idms_v2": ["standardmidsmediummemoryv2family"],
    "Standard_M192ids_v2": ["standardmidsmediummemoryv2family"],
    "Standard_M192ims_v2": ["standardmismediummemoryv2family"],
    "Standard_M192is_v2": ["standardmismediummemoryv2family"],
    "ECas_cc_v5/ECads_cc_v5-series": [
        "standardecaccv5family",
        "standardecadccv5family",
    ],
    "Ls-series": ["standardlsfamily"],
    "Lsv2-series": ["standardlsv2family"],
    "NCv3-NC24rs Series": ["standardncsv3family"],
    "NCv3-Series": ["standardncsv3family"],
    "NVv3-series": ["standardnvsv3family"],
    "NVv4-series": ["standardnvsv4family"],
    "NP-series": ["standardnpsfamily"],
    "HC-series": ["standardhcsfamily"],
    "HBv2-series": ["standardhbrsv2family"],
}

TABLE_HEADERS = [
    "Series name",
    "Retirement Status",
    "Retirement Announcement",
    "Planned Retirement Date",
    "Modernization guide",
]


def parse_date(value):
    """Convert Microsoft's table date to an ISO date; retain blanks as empty."""
    value = value.strip()
    if not value or value == "-":
        return ""
    for date_format in ("%m/%d/%y", "%m/%d/%Y"):
        try:
            return datetime.strptime(value, date_format).date().isoformat()
        except ValueError:
            continue
    raise ValueError(f"Unsupported retirement date format: {value}")


def fetch_retirements():
    """Fetch official retirement rows and expand them to exact SKU family keys."""
    response = requests.get(RETIREMENT_PAGE, timeout=30)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    retirements = {}
    supported_rows = 0

    for table in soup.find_all("table"):
        rows = table.find_all("tr")
        if not rows:
            continue
        headers = [cell.get_text(" ", strip=True) for cell in rows[0].find_all(["th", "td"])]
        if headers != TABLE_HEADERS:
            continue

        for row in rows[1:]:
            cells = row.find_all(["th", "td"])
            if len(cells) != len(TABLE_HEADERS):
                continue

            series_name = cells[0].get_text(" ", strip=True)
            family_keys = SERIES_TO_FAMILIES.get(series_name)
            if family_keys is None:
                print(
                    f"[INFO] No VM family mapping for official row: {series_name}",
                    file=sys.stderr,
                )
                continue

            status = cells[1].get_text(" ", strip=True)
            if status not in ("Announced", "Retired"):
                raise ValueError(f"Unsupported retirement status for {series_name}: {status}")

            guide = cells[4].find("a", href=True)
            guide_url = urljoin(RETIREMENT_PAGE, guide["href"]) if guide else RETIREMENT_PAGE
            entry = {
                "name": series_name,
                "retireDate": parse_date(cells[3].get_text(" ", strip=True)),
                "retirementStatus": status,
                "learnMoreUrl": guide_url,
            }
            for family_key in family_keys:
                retirements[family_key] = {"family": family_key, **entry}
            supported_rows += 1

    if not supported_rows:
        raise ValueError("No supported retirement rows found on the official page.")
    return list(retirements.values())


def main():
    print("=" * 60)
    print("VM SKU Retirement Data Updater")
    print("=" * 60)

    retirements = fetch_retirements()
    data = {
        "lastUpdated": date.today().isoformat(),
        "source": RETIREMENT_PAGE,
        "retirements": sorted(retirements, key=lambda entry: entry["family"]),
    }
    with open(DATA_FILE, "w", encoding="utf-8") as output:
        json.dump(data, output, indent=2, ensure_ascii=False)
        output.write("\n")

    print(f"[OK] Wrote {len(retirements)} VM family retirement entries to {DATA_FILE}")


if __name__ == "__main__":
    main()
