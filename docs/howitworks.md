# How It Works — Azure VM SKU by Region

> Technical deep-dive into the application architecture and implementation.

## Architecture

This is a **single-file HTML web application** with **static JSON data files** — all HTML, CSS, and JavaScript live in one `index.html` file, and pre-fetched data is stored as JSON in the `data/` directory. There are no frameworks, no build tools, and no external dependencies.

🔗 **Live at [vmsku.djtools.co.nz](https://vmsku.djtools.co.nz)**

### Why This Approach?
- **No authentication needed**: Data is pre-fetched, so users don't need to log in
- **Zero setup**: Just visit the URL
- **No dependencies**: Nothing to install, update, or break
- **Fast**: Static JSON loads instantly, no API calls at runtime

## Data Pipeline

### Sources

| Data Set | Source | Script |
|----------|--------|--------|
| VM SKUs | Azure Resource SKU API | `scripts/normalize-skus.py` |
| Managed Disk SKUs | Azure Resource SKU API | `scripts/normalize-disks.py` |
| VM Pricing | Azure Retail Prices API | `scripts/fetch-pricing.py` |
| Retirement Dates | Azure Updates page | `scripts/update-retirements.py` |

The list of regions to fetch is configured in `config.json`.

### VM SKU Normalization
Raw SKU data has capabilities buried in a `capabilities[]` array of `{name, value}` pairs. The normalize script flattens these into clean fields:

```
Raw: capabilities: [{name: "vCPUs", value: "4"}, {name: "MemoryGB", value: "16"}, ...]
Normalized: { vCPUs: 4, memoryGB: 16, ... }
```

### Key normalized VM fields
- `vCPUs`, `memoryGB`, `maxDataDisks`, `maxNICs`
- `cpuArchitecture` (x64 or Arm64)
- `acceleratedNetworking`, `premiumIO`, `ephemeralOSDisk`, `encryptionAtHost`
- `spotEligible`, `zones`, `restrictions`

### Disk SKU Normalization
Raw disk data is filtered (type-level entries removed) and normalized to include:
- `maxIOPS`, `maxThroughputMBps`, `burstIOPS`, `burstThroughputMBps`
- `maxSizeGiB`, `maxShares`, `zones`
- Tier labels: Premium SSD, Standard SSD, Standard HDD, Ultra, PremiumV2

### Processor Detection
The `getProcessorType(size)` helper parses SKU name suffixes to identify processor type:
- `a` suffix → AMD
- `p` suffix → ARM (Ampere)
- Otherwise → Intel

### History Archiving
Before each data refresh, previous data files are archived to `data/history/` with timestamps. This enables the What's New feature to compare current data against the previous month and surface added/removed SKUs.

### Schedule
Data is refreshed monthly via the `refresh-vm-skus.yml` GitHub Actions workflow on a self-hosted runner. The workflow also supports manual dispatch via the GitHub Actions UI.

## Data Loading

### Lazy Loading
The app loads region data on demand — when a user selects a region, it fetches `data/{regionName}.json` and `data/{regionName}-disks.json`. Data is cached in memory for the session.

### Startup Data
On initialization, the app loads:
- `data/regions.json` — all available Azure regions
- `data/metadata.json` — last refresh timestamp and region availability
- `data/retirements.json` — VM family retirement data

## Sections & Features

### Tab Layout
The app uses a **tabbed interface** with 6 tabs in a sticky tab strip:
1. **📊 Overview** — Summary KPI cards, What's New (month-over-month SKU changes), Workload Recommendations
2. **🔍 Browse SKUs** — Filterable SKU table with search, filters, column chooser
3. **🎯 Find a Match** — Deployment requirements checker with ranked results
4. **📌 Pinned** — Shortlist, pricing comparison, multi-region availability compare
5. **💿 Disk SKUs** — Managed disk browser with tier filters and collapsible groups
6. **📖 Reference** — VM naming convention guide, CLI guidance, deployment snippets

Tabs support keyboard shortcuts (1–6), URL hash routing, and dynamic badge counts.

### Browse SKUs (See What's Available)
- Filterable, sortable table grouped alphabetically by first letter
- Filters: text search, size, version, family type, vCPU range, processor type
- Column chooser to show/hide columns
- Click any SKU for deployment snippet modal (CLI, PowerShell, Bicep)
- Retirement badges on SKUs from families being retired

### Find a Match (Deployment Checker)
Users specify minimum requirements (vCPUs, memory, disks, NICs, processor, features) and get ranked matches with percentage scores. Results can be pinned or exported to CSV.

### Pinned Shortlist & Multi-Region Compare
- Pin SKUs from browse table or checker results
- Chips display key specs at a glance
- Compare pinned SKU availability across up to 5 additional regions
- Export pinned shortlist to CSV

### Disk SKUs
- Summary cards showing disk count by tier
- Collapsible groups by disk tier with expand/collapse all
- Filters: disk type, redundancy (LRS/ZRS), availability zones, IOPS range
- Performance details: IOPS, throughput, burst, max shares

### KPI Dashboard
Summary cards showing: Total SKUs, vCPU Range, Memory Range, Unique Families, Intel count, AMD/ARM count, plus data freshness indicator.

## Theme System

### CSS Custom Properties
```css
:root {
  --brand-primary: #0f6cbd;
  --bg-base: #fafafa;
  --text-primary: #242424;
}
```

### Dark Mode
- Toggled via header button or `T` keyboard shortcut
- System preference detected on first visit via `prefers-color-scheme`
- Preference saved to `localStorage`

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `T` | Toggle light/dark theme |
| `F` | Focus search input |
| `C` | Clear all filters |
| `X` | Export to CSV |
| `?` | Show keyboard shortcuts panel |
| `Esc` | Close modals/panels |

## Deployment

### Azure Static Web Apps
The app is hosted on Azure Static Web Apps (Free tier) with a custom domain and managed SSL.

### CI/CD Pipeline
```
Push to main → GitHub Actions → swa deploy (staging folder) → Live
```

Only web-servable files are deployed (`index.html`, `config.json`, `data/`). Scripts and docs are excluded.

### Data Refresh Pipeline
```
Monthly trigger → fetch VM/disk/pricing/retirement data → swa deploy → git commit → push
```

The refresh pipeline runs on a self-hosted runner with Azure CLI access.
