#!/usr/bin/env python3
"""
build-cards.py — turns the existing per-region SKU + pricing + retirement data
into a single flat data/cards.json file consumed by the Azure Top Trumps game.

Phase 1 of the pivot. This script is the only data transformation that the
game depends on; everything downstream (game UI, deck shuffling, AI) reads
cards.json and never touches the raw region files.

Run:
    python scripts/build-cards.py

Inputs (read from ./data/):
    config.json (project root)            target regions
    data/<region>.json                    SKU specs (vCPUs, memoryGB, maxNICs, maxDataDisks, family, ...)
    data/<region>-pricing.json            PAYG/spot prices keyed by size
    data/retirements.json                 family-level retirement dates

Output:
    data/cards.json                       flat list of card objects (schema in plan.md §6)
"""
from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
CONFIG = ROOT / "config.json"
OUT = DATA / "cards.json"

# ---------------------------------------------------------------------------
# Calibration constants
# ---------------------------------------------------------------------------

# Power-score weights — must sum to 1.0
WEIGHTS = {
    "vcpus": 0.25,
    "memory": 0.25,
    "data_disks": 0.05,
    "nics": 0.05,
    "gpu": 0.40,
}

# Soft caps used to normalise stats to 0..1 before weighting.
# Picked from the high-water marks in current data so a flagship card hits ~95.
CAPS = {
    "vcpus": 192,
    "memory_gb": 4000,
    "data_disks": 64,
    "nics": 8,
}

# GPU tier: token in family name -> 0..1 contribution to power score.
# Order matters (most-specific first) since the family name is matched longest-first.
GPU_TIERS = [
    ("B200",   1.00, "Blackwell B200"),
    ("MI300X", 1.00, "MI300X"),
    ("H100",   0.95, "H100"),
    ("A100",   0.80, "A100"),
    ("V100",   0.65, "V100"),
    ("A10",    0.50, "A10"),
    ("V620",   0.50, "V620"),
    ("T4",     0.30, "T4"),
    ("M60",    0.30, "M60"),
    ("K80",    0.20, "K80"),
]

# Family-prefix → workload type. Mirrors index.html's familyMap typing
# but driven off the bare letter prefix so it works even for new families.
FAMILY_TYPE_BY_PREFIX = [
    ("NC", "GPU Accelerated"),
    ("ND", "GPU Accelerated"),
    ("NV", "GPU Accelerated"),
    ("NG", "GPU Accelerated"),
    ("HB", "HPC"),
    ("HC", "HPC"),
    ("HX", "HPC"),
    ("H",  "HPC"),
    ("M",  "Memory Optimized"),
    ("EC", "Confidential"),
    ("DC", "Confidential"),
    ("E",  "Memory Optimized"),
    ("F",  "Compute Optimized"),
    ("L",  "Storage Optimized"),
    ("G",  "Memory Optimized"),
    ("D",  "General Purpose"),
    ("B",  "General Purpose"),
    ("A",  "General Purpose"),
]

TYPE_COLORS = {
    "General Purpose":   "#0f6cbd",
    "Compute Optimized": "#e97548",
    "Memory Optimized":  "#8764b8",
    "Storage Optimized": "#038387",
    "GPU Accelerated":   "#c4314b",
    "HPC":               "#4f52b2",
    "Confidential":      "#7a7574",
}

# Region → short label and friendly name for the set badge.
REGION_LABELS = {
    "australiaeast":   ("AU-EAST",  "Australia East"),
    "australiasoutheast": ("AU-SE",  "Australia Southeast"),
    "newzealandnorth": ("NZ-NORTH", "New Zealand North"),
    "southeastasia":   ("SE-ASIA",  "Southeast Asia"),
    "japaneast":       ("JP-EAST",  "Japan East"),
    "westeurope":      ("EU-WEST",  "West Europe"),
    "northeurope":     ("EU-NORTH", "North Europe"),
    "eastus":          ("US-EAST",  "East US"),
    "eastus2":         ("US-EAST2", "East US 2"),
    "westus2":         ("US-WEST2", "West US 2"),
    "westus3":         ("US-WEST3", "West US 3"),
    "centralus":       ("US-CENT",  "Central US"),
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def scale(value: float, lo: float, hi: float) -> float:
    """Linearly normalise into [0,1] with clamping."""
    if hi <= lo:
        return 0.0
    return max(0.0, min(1.0, (value - lo) / (hi - lo)))


def family_clean(family: str) -> str:
    """Strip 'Standard' prefix and 'Family' suffix, case-insensitive."""
    if not family:
        return ""
    f = re.sub(r"^[Ss]tandard", "", family)
    f = re.sub(r"[Ff]amily$", "", f)
    return f


def family_type(family: str) -> str:
    name = family_clean(family).lower()
    for prefix, typ in FAMILY_TYPE_BY_PREFIX:
        if name.startswith(prefix.lower()):
            return typ
    return "General Purpose"


def gpu_for(family: str) -> tuple[float, str | None]:
    """Return (gpu_tier_0_to_1, gpu_label_or_None) for a family name."""
    name = family.upper() if family else ""
    for token, tier, label in GPU_TIERS:
        if token.upper() in name:
            return tier, label
    return 0.0, None


def power_score(vcpus: int, memory_gb: float, data_disks: int,
                nics: int, gpu_tier: float) -> int:
    """
    sqrt-scale the long-tailed CPU/memory dimensions so mid-range cards
    don't feel like cardboard, while flagships still cap near 100.
    """
    import math
    s = (
        WEIGHTS["vcpus"]      * math.sqrt(scale(vcpus,      1, CAPS["vcpus"]))
      + WEIGHTS["memory"]     * math.sqrt(scale(memory_gb,  1, CAPS["memory_gb"]))
      + WEIGHTS["data_disks"] * math.sqrt(scale(data_disks, 1, CAPS["data_disks"]))
      + WEIGHTS["nics"]       * math.sqrt(scale(nics,       1, CAPS["nics"]))
      + WEIGHTS["gpu"]        * gpu_tier
    )
    return max(1, min(100, int(round(s * 100))))


def assign_rarity(sku: dict, gpu_tier: float, fam_type: str) -> str:
    """Heuristic — mirrors plan.md §2.4. Tunable."""
    name = (sku.get("name") or "").upper()
    fam = (sku.get("family") or "").upper()
    mem = sku.get("memoryGB") or 0
    vcpus = sku.get("vCPUs") or 0

    # Legendaries: top GPUs and giant M-series
    if "B200" in fam or "MI300X" in fam or "H100" in fam:
        return "legendary"
    if fam_type == "Memory Optimized" and mem >= 1750:
        return "legendary"

    # Epics: A100/V100, big M, very large general
    if "A100" in fam or "V100" in fam:
        return "epic"
    if fam_type == "Memory Optimized" and mem >= 700:
        return "epic"
    if vcpus >= 96:
        return "epic"

    # Rares: other GPUs, HPC, high-spec memory/compute
    if gpu_tier > 0:
        return "rare"
    if fam_type == "HPC":
        return "rare"
    if fam_type == "Confidential" and vcpus >= 16:
        return "rare"
    if fam_type == "Memory Optimized" and mem >= 256:
        return "rare"
    if vcpus >= 48:
        return "rare"

    # Uncommons: mid-range E/F, larger D, mid memory
    if fam_type in ("Memory Optimized", "Compute Optimized"):
        return "uncommon"
    if vcpus >= 8 or mem >= 32:
        return "uncommon"

    # Everything else: A/B v1, low D, tiny burst
    return "common"


# ---------------------------------------------------------------------------
# Nicknames
# ---------------------------------------------------------------------------

# Family-prefix → adjective pool, deterministic-by-size.
# These are intentionally a bit playful but never wrong-for-the-archetype.
NICK_ADJ = {
    "GPU Accelerated":   ["GPU", "Tensor", "CUDA", "Render", "Vector"],
    "HPC":               ["Throttle", "Compute", "Hyper", "Parallel", "Crunch"],
    "Memory Optimized":  ["Memory", "Cache", "RAM", "Heap", "Buffer"],
    "Compute Optimized": ["Throttle", "Compute", "Burst", "Cycle", "Clock"],
    "Storage Optimized": ["Spindle", "Ledger", "Vault", "Stream", "Archive"],
    "Confidential":      ["Cipher", "Sealed", "Vault", "Veil", "Cloak"],
    "General Purpose":   ["Worker", "Daily", "Pocket", "Field", "Steady"],
}
NICK_NOUN = {
    "common":    ["Pup",     "Sprout",   "Whelp",    "Cub",     "Drone"],
    "uncommon":  ["Runner",  "Squire",   "Worker",   "Scout",   "Builder"],
    "rare":      ["Hunter",  "Champion", "Vanguard", "Guardian", "Knight"],
    "epic":      ["Crusher", "Titan",    "Warlord",  "Behemoth", "Reaver"],
    "legendary": ["King",    "Sovereign", "Avatar",  "Colossus", "Apex"],
}

def nickname_for(sku_name: str, fam_type: str, rarity: str) -> str:
    """Deterministic-from-sku-name nickname. Never random."""
    h = sum(ord(c) for c in sku_name)
    adj_pool = NICK_ADJ.get(fam_type, NICK_ADJ["General Purpose"])
    noun_pool = NICK_NOUN.get(rarity,  NICK_NOUN["common"])
    return f"{adj_pool[h % len(adj_pool)]} {noun_pool[(h // 7) % len(noun_pool)]}"


# ---------------------------------------------------------------------------
# Card builder
# ---------------------------------------------------------------------------

def build_ability(sku: dict, gpu_label: str | None,
                  retirement: dict | None,
                  family_clean_name: str = "",
                  fam_type: str = "") -> dict | None:
    """
    One-line factoid for the bottom of the card.

    Priority cascade (first match wins):
      1. Retirement notice (with learn-more URL).
      2. Family-specific factoid (teaches something true about the series).
      3. Capability-based factoid (GPU, multi-NIC, big memory, spot, etc.).
      4. Family-type honest fallback (no more "Pocket Worker" filler).
    """
    if retirement:
        out = {
            "title": "Sunset Era",
            "description": f"{retirement['name']} is retiring on {retirement['date']}. Plan a migration to a newer family.",
        }
        if retirement.get("url"):
            out["url"] = retirement["url"]
        return out

    # ---- 2. Family-specific factoids -----------------------------------
    # Match on the cleaned family name lowercased (e.g. "dsv5", "bsv2",
    # "hbv4", "dasv6", "ncadsh100v5", "lsv3", "msv3", "dpsv5"). Order
    # matters — more specific patterns first.
    fclow = (family_clean_name or "").lower()
    FAMILY_FACTOIDS: list[tuple[str, str, str]] = [
        # Confidential (AMD SEV-SNP and Intel TDX) — check before generic D-/E-.
        (r"^(dc|ec)a[a-z]*v?\d*",
         "AMD SEV-SNP",
         "Confidential VM with AMD SEV-SNP — TEE-protected memory and attestation for sensitive workloads."),
        (r"^(dc|ec)e[a-z]*v?\d*",
         "Intel TDX",
         "Confidential VM with Intel TDX — hardware-isolated VM memory for regulated workloads."),
        (r"^(dc|ec)[a-z]*v?\d*",
         "Confidential VM",
         "Hardware-rooted trusted execution — protected memory and remote attestation."),

        # HPC fabric (RDMA + InfiniBand)
        (r"^hb[a-z]*v?\d*",
         "AMD EPYC HPC",
         "AMD EPYC + 200/400 Gb InfiniBand — memory-bandwidth-bound CFD, weather, seismic, reservoir."),
        (r"^hc[a-z]*v?\d*",
         "HPC Intel Xeon",
         "Intel Xeon Platinum with FP64-heavy workloads in mind — tightly-coupled MPI via InfiniBand."),
        (r"^hx[a-z]*v?\d*",
         "Memory-Bound HPC",
         "Built for memory-bound HPC (EDA, structural FEA) — large per-core RAM and InfiniBand."),
        (r"^h[a-z]*v?\d*",
         "RDMA HPC",
         "High-frequency CPU with RDMA fabric — sub-microsecond MPI for tightly-coupled simulation."),

        # GPU families — per-series notes that complement the gpu_label.
        (r"^nc[a-z]*h100v?\d*",
         "H100 Tensor Cores",
         "NVIDIA H100 + NVLink/NVSwitch — flagship training and large-model inference."),
        (r"^nd[a-z]*h100v?\d*",
         "H100 Scale-Out",
         "8× H100 with NDR InfiniBand — multi-node distributed training fabric."),
        (r"^nd[a-z]*a100v?\d*",
         "A100 Scale-Out",
         "8× A100 with HDR InfiniBand — proven backbone for large-model training."),
        (r"^nc[a-z]*a100v?\d*",
         "A100 Tensor Cores",
         "NVIDIA A100 with MIG support — flexible GPU partitioning for inference at scale."),
        (r"^nc[a-z]*v?\d*",
         "Compute GPU",
         "NVIDIA compute GPU — CUDA training and inference workloads."),
        (r"^nv[a-z]*v?\d*",
         "Visualization GPU",
         "Designed for remote workstations, CAD, 3D rendering, and game streaming."),
        (r"^nd[a-z]*v?\d*",
         "Deep-Learning Scale-Out",
         "Multi-GPU + InfiniBand — purpose-built for distributed deep-learning training."),

        # Storage Optimized (local NVMe)
        (r"^ls?v?\d*[a-z]*",
         "Local NVMe SSD",
         "Direct-attached NVMe — multi-GB/s throughput for transactional DBs, NoSQL, big-data scans."),

        # Memory Optimized — M-series (SAP HANA)
        (r"^m[a-z]*v?\d*",
         "SAP HANA Class",
         "Certified for SAP HANA — multi-TB RAM for in-memory analytics and large databases."),

        # General Purpose Arm (Cobalt/Ampere) — must beat the generic D-/E- below.
        (r"^dp[a-z]*v?\d*|^ep[a-z]*v?\d*",
         "Arm64 Native",
         "Cobalt / Ampere Altra Arm cores — efficient price-perf for cloud-native scale-out."),

        # E-series memory
        (r"^e[a-z]*v?\d*",
         "Memory Heavy",
         "Higher memory-per-vCPU ratio — built for in-memory caches, relational DBs, and analytics."),

        # Compute Optimized
        (r"^f[a-z]*v?\d*",
         "Compute Heavy",
         "Higher CPU-per-memory ratio — web tier, batch processing, gaming servers, build agents."),

        # Burstable (Bs / Bsv2)
        (r"^bs?v?\d*[a-z]*",
         "Burstable Credits",
         "Banks CPU credits at idle and bursts on-demand — cost-effective for spiky, low-baseline workloads."),

        # General Purpose modern (Dv5/Dasv5/Ddsv5 etc.) — versioned form.
        (r"^d[a-z]*v[3-9][a-z]*$",
         "Modern General Purpose",
         "Balanced CPU/memory on the latest silicon — the default for most production workloads."),
        # General Purpose D-series (older or unversioned).
        (r"^d[a-z]*v?\d*",
         "General Purpose",
         "Balanced CPU and memory — the everyday choice for most line-of-business apps."),
        # A-series legacy
        (r"^a[a-z]*v?\d*",
         "Entry Tier",
         "Entry-tier general-purpose — dev/test and light workloads on older silicon."),
    ]
    for pattern, title, desc in FAMILY_FACTOIDS:
        if re.search(pattern, fclow):
            return {"title": title, "description": desc}

    # ---- 3. Capability-based factoids ----------------------------------
    if gpu_label:
        return {
            "title": gpu_label,
            "description": f"Onboard {gpu_label} GPU — built for AI training, inference, and visualisation.",
        }
    if sku.get("acceleratedNetworking") and (sku.get("maxNICs") or 0) >= 4:
        return {
            "title": "Multi-NIC Fabric",
            "description": f"{sku['maxNICs']} NICs with accelerated networking — strong for NVAs and multi-tier apps.",
        }
    if (sku.get("memoryGB") or 0) >= 700:
        return {
            "title": "Memory Vault",
            "description": "Built for in-memory databases & SAP HANA-class workloads.",
        }
    if sku.get("spotEligible"):
        return {
            "title": "Spot Eligible",
            "description": "Runs on spare capacity at up to ~90% off — great for interruptible batch and CI.",
        }
    if sku.get("encryptionAtHost"):
        return {
            "title": "Encryption at Host",
            "description": "Temp disk and data disks are encrypted on the host hardware.",
        }
    if sku.get("ephemeralOSDisk"):
        return {
            "title": "Ephemeral OS Disk",
            "description": "OS disk lives on local SSD — faster boots, no storage cost, stateless by design.",
        }
    if sku.get("premiumIO"):
        return {
            "title": "Premium IO",
            "description": "Supports Premium SSD — low-latency, high-IOPS storage for production workloads.",
        }
    arch = sku.get("cpuArchitecture")
    if arch and arch.lower() == "arm64":
        return {
            "title": "Arm64 Native",
            "description": "Ampere Altra-class CPU — great price/perf for cloud-native and microservice workloads.",
        }

    # ---- 4. Honest family-type fallback (no more "Pocket Worker") ------
    FAMILY_TYPE_FALLBACK = {
        "General Purpose":   ("General Purpose",   "Balanced CPU and memory — the everyday choice for most workloads."),
        "Compute Optimized": ("Compute Optimized", "Higher CPU-to-memory ratio — web tier, batch, gaming, build agents."),
        "Memory Optimized":  ("Memory Optimized",  "Higher memory-to-CPU ratio — caches, relational DBs, analytics."),
        "Storage Optimized": ("Storage Optimized", "Local NVMe storage — IOPS-heavy databases and big-data scans."),
        "GPU Accelerated":   ("GPU Accelerated",   "GPU-attached — purpose-built for AI/ML, rendering, and visualisation."),
        "HPC":               ("HPC",               "High-frequency CPU + RDMA networking — tightly-coupled simulation."),
        "Confidential":      ("Confidential VM",   "Hardware-rooted TEE — protected memory for sensitive workloads."),
    }
    title, desc = FAMILY_TYPE_FALLBACK.get(
        fam_type,
        ("General Purpose", "Balanced CPU and memory — the everyday choice for most workloads."),
    )
    return {"title": title, "description": desc}


def build_card(sku: dict, region: str, prices: dict,
               retirement_lookup: dict) -> dict | None:
    name = sku.get("name")
    size = sku.get("size") or (name or "").replace("Standard_", "")
    if not name or not size:
        return None

    family = sku.get("family") or ""
    fam_type = family_type(family)
    gpu_tier, gpu_label = gpu_for(family)

    vcpus = int(sku.get("vCPUs") or 0)
    memory_gb = float(sku.get("memoryGB") or 0)
    data_disks = int(sku.get("maxDataDisks") or 0)
    nics = int(sku.get("maxNICs") or 0)

    # Pricing (PAYG Linux preferred, fall back through alternatives)
    price_block = prices.get(size) or {}
    price = (price_block.get("linux")
             or price_block.get("windows")
             or price_block.get("spot")
             or None)

    # Retirement
    retirement = retirement_lookup.get(family.lower())

    rarity = assign_rarity(sku, gpu_tier, fam_type)
    power = power_score(vcpus, memory_gb, data_disks, nics, gpu_tier)
    nick = nickname_for(name, fam_type, rarity)

    region_short, region_display = REGION_LABELS.get(
        region, (region.upper()[:8], region.title())
    )

    card = {
        "id": f"{region}::{name}",
        "sku": name,
        "displayName": size.replace("_", " "),
        "nickname": nick,
        "region": region,
        "regionShort": region_short,
        "regionDisplay": region_display,
        "family": family,
        "familyDisplay": family_clean(family),
        "familyType": fam_type,
        "familyColor": TYPE_COLORS.get(fam_type, "#0f6cbd"),
        "rarity": rarity,
        "stats": {
            "vcpus":         vcpus,
            "memoryGB":      round(memory_gb, 1),
            "maxDataDisks":  data_disks,
            "nics":          nics,
            "pricePerHourUSD": round(price, 4) if price is not None else None,
            "powerScore":    power,
        },
        "tags": {
            "gpu":                   gpu_label,
            "acceleratedNetworking": bool(sku.get("acceleratedNetworking")),
            "premiumIO":             bool(sku.get("premiumIO")),
            "spotEligible":          bool(sku.get("spotEligible")),
            "encryptionAtHost":      bool(sku.get("encryptionAtHost")),
            "ephemeralOSDisk":       bool(sku.get("ephemeralOSDisk")),
            "cpuArchitecture":       sku.get("cpuArchitecture"),
            "retiring":              bool(retirement),
            "retirementDate":        retirement["date"] if retirement else None,
        },
        "ability": build_ability(sku, gpu_label, retirement,
                                 family_clean_name=family_clean(family),
                                 fam_type=fam_type),
    }

    # Filter out cards that have no usable price AND aren't a flagship —
    # keeping a 5-stat playable card is fine, but skip totally empty rows.
    if price is None and vcpus == 0:
        return None

    return card


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def main() -> int:
    if not CONFIG.exists():
        print(f"ERROR: missing {CONFIG}", file=sys.stderr)
        return 1
    cfg = load_json(CONFIG)
    # Top Trumps deck has a much narrower regional scope than the locator app
    # itself. Prefer an explicit `topTrumpsRegions` list; fall back to
    # `targetRegions` so the script still works in repos that only have one.
    raw_regions = cfg.get("topTrumpsRegions") or cfg.get("targetRegions") or []
    # Accept either ["region"] or [{"name": "region", ...}]
    regions = [r["name"] if isinstance(r, dict) else r for r in raw_regions]
    if not regions:
        print("ERROR: config.json has no topTrumpsRegions or targetRegions", file=sys.stderr)
        return 1

    # Retirement lookup (family.lower() -> {name, date, url})
    retirement_lookup: dict[str, dict] = {}
    ret_path = DATA / "retirements.json"
    if ret_path.exists():
        retirements = load_json(ret_path).get("retirements", [])
        for r in retirements:
            fam = (r.get("family") or "").lower()
            if fam:
                retirement_lookup[fam] = {
                    "name": r.get("name") or fam,
                    "date": r.get("retireDate") or "",
                    "url":  r.get("learnMoreUrl") or "",
                }

    cards: list[dict] = []
    summary: dict[str, int] = {}
    for region in regions:
        sku_path = DATA / f"{region}.json"
        price_path = DATA / f"{region}-pricing.json"
        if not sku_path.exists():
            print(f"WARN: skipping {region} — {sku_path.name} not found")
            continue
        sku_doc = load_json(sku_path)
        price_doc = load_json(price_path) if price_path.exists() else {}
        prices = price_doc.get("prices") or {}

        region_cards = 0
        skipped = 0
        for sku in sku_doc.get("skus", []):
            card = build_card(sku, region, prices, retirement_lookup)
            if card is None:
                skipped += 1
                continue
            cards.append(card)
            region_cards += 1
        summary[region] = region_cards
        print(f"  {region}: {region_cards} cards (skipped {skipped})")

    # Rarity distribution sanity check
    rarity_counts: dict[str, int] = {}
    for c in cards:
        rarity_counts[c["rarity"]] = rarity_counts.get(c["rarity"], 0) + 1

    out = {
        "version": "1.0",
        "generated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "regions": [
            {
                "id": r,
                "short": REGION_LABELS.get(r, (r.upper()[:8], r))[0],
                "display": REGION_LABELS.get(r, (r, r.title()))[1],
                "cardCount": summary.get(r, 0),
            }
            for r in regions
        ],
        "rarityCounts": rarity_counts,
        "cards": cards,
    }

    OUT.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    print()
    print(f"Wrote {len(cards)} cards across {len(summary)} regions → {OUT.relative_to(ROOT)}")
    print(f"Rarity distribution: {rarity_counts}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
