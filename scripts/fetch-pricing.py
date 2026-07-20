"""Fetch VM pricing from Azure Retail Prices API (no auth required).

Produces a JSON file per region with pay-as-you-go and reserved instance
pricing for each SKU. Supports any of the 17 currencies via --currency flag.
"""
import json
import sys
import urllib.request
import urllib.parse
import time
import argparse

parser = argparse.ArgumentParser(description='Fetch VM pricing from Azure Retail Prices API')
parser.add_argument('region_file', help='Path to region SKU data JSON file')
parser.add_argument('output_file', help='Path to output pricing JSON file')
parser.add_argument('--currency', default='USD', help='Currency code (default: USD)')
parser.add_argument('--payg-only', action='store_true', help='Fetch PAYG pricing only (skip RI data)')
args = parser.parse_args()

region_file = args.region_file
output_file = args.output_file
currency = args.currency.upper()
payg_only = args.payg_only

with open(region_file, encoding='utf-8') as f:
    region_data = json.load(f)

region_name = region_data.get('region', '')
sku_names = sorted(set(s['size'] for s in region_data.get('skus', [])))

# API uses "Standard_" prefix for SKU names
api_sku_map = {}
for name in sku_names:
    api_name = name if name.startswith('Standard_') else f'Standard_{name}'
    api_sku_map[api_name] = name

api_sku_names = sorted(api_sku_map.keys())
print(f"  Fetching pricing for {len(api_sku_names)} SKUs in {region_name} ({currency})...")


def fetch_batched(api_sku_names, region_name, currency, price_type):
    """Fetch pricing items from the API in batches."""
    items = []
    BATCH_SIZE = 10
    for i in range(0, len(api_sku_names), BATCH_SIZE):
        batch = api_sku_names[i:i + BATCH_SIZE]
        sku_filter = ' or '.join(f"armSkuName eq '{s}'" for s in batch)
        odata_filter = (
            f"serviceName eq 'Virtual Machines' "
            f"and armRegionName eq '{region_name}' "
            f"and ({sku_filter}) "
            f"and priceType eq '{price_type}'"
        )
        url = f"https://prices.azure.com/api/retail/prices?currencyCode='{currency}'&$filter={urllib.parse.quote(odata_filter)}"

        pages = 0
        while url and pages < 10:
            for attempt in range(3):
                try:
                    req = urllib.request.Request(url)
                    with urllib.request.urlopen(req, timeout=30) as resp:
                        data = json.loads(resp.read().decode())
                    items.extend(data.get('Items', []))
                    url = data.get('NextPageLink')
                    pages += 1
                    break
                except Exception as e:
                    if attempt < 2:
                        time.sleep(2 * (attempt + 1))
                    else:
                        print(f"  [WARN] Failed to fetch batch {i//BATCH_SIZE + 1} ({price_type}): {e}")
                        url = None

        if i + BATCH_SIZE < len(api_sku_names):
            time.sleep(0.2)
    return items


# --- Pass 1: Consumption (PAYG) pricing ---
all_items = fetch_batched(api_sku_names, region_name, currency, 'Consumption')

# Build pricing map: { skuName: { linux, windows, spot, linuxLowPri } }
pricing = {}
for item in all_items:
    sku_api = item.get('armSkuName', '')
    if not sku_api:
        continue
    sku = api_sku_map.get(sku_api, sku_api)

    is_windows = 'Windows' in item.get('productName', '')
    is_spot = 'Spot' in item.get('meterName', '')
    is_low_pri = 'Low Priority' in item.get('meterName', '')
    price = item.get('retailPrice', 0)

    if sku not in pricing:
        pricing[sku] = {}

    if is_spot and not is_windows:
        pricing[sku]['spot'] = price
    elif is_low_pri and not is_windows:
        pricing[sku]['linuxLowPri'] = price
    elif is_windows and not is_spot and not is_low_pri:
        pricing[sku]['windows'] = price
    elif not is_windows and not is_spot and not is_low_pri:
        pricing[sku]['linux'] = price

# --- Pass 2: Reservation (RI) pricing (skip if --payg-only) ---
if not payg_only:
    print(f"  Fetching RI pricing for {len(api_sku_names)} SKUs...")
    ri_items = fetch_batched(api_sku_names, region_name, currency, 'Reservation')

    HOURS_1YR = 8760
    HOURS_3YR = 26280

    for item in ri_items:
        sku_api = item.get('armSkuName', '')
        if not sku_api:
            continue
        sku = api_sku_map.get(sku_api, sku_api)
        # RI pricing is OS-agnostic (Linux-equivalent); skip Windows-named products
        if 'Windows' in item.get('productName', ''):
            continue

        term = item.get('reservationTerm', '')
        price = item.get('retailPrice', 0)
        if not price:
            continue

        if sku not in pricing:
            pricing[sku] = {}

        if term == '1 Year':
            pricing[sku]['ri1yr'] = round(price / HOURS_1YR, 6)
        elif term == '3 Years':
            pricing[sku]['ri3yr'] = round(price / HOURS_3YR, 6)

output = {
    'region': region_name,
    'currency': currency,
    'lastUpdated': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
    'prices': pricing
}

with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(output, f, separators=(',', ':'))

matched = sum(1 for v in pricing.values() if v)
ri_matched = sum(1 for v in pricing.values() if v.get('ri1yr'))
print(f"  [OK] Pricing fetched ({currency}): {matched}/{len(sku_names)} SKUs with PAYG, {ri_matched} with RI")
