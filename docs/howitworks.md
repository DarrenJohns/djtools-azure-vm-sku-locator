# How It Works — VM SKU Per Region

> Technical deep-dive into the application architecture and implementation.

## Architecture

This is a **single-file HTML web application** with **static JSON data files** — all HTML, CSS, and JavaScript live in one `index.html` file, and pre-fetched VM SKU data is stored as JSON in the `data/` directory. There are no frameworks, no build tools, and no external dependencies.

### Why This Approach?
- **No authentication needed**: Data is pre-fetched, so users don't need to log in
- **Zero setup**: Serve the directory and open in a browser
- **Simple deployment**: Upload files to Azure Blob Storage
- **No dependencies**: Nothing to install, update, or break
- **Fast**: Static JSON loads instantly, no API calls at runtime

## Data Pipeline

### Source
VM SKU data comes from the Azure Resource SKUs API, accessed via `az vm list-skus`. This is the same data source used by the Azure Portal and CLI. The list of regions to fetch is configured in `config.json`.

### Normalization
Raw SKU data has capabilities buried in a `capabilities[]` array of `{name, value}` pairs. The `scripts/normalize-skus.py` script normalizes these into flat fields:

```
Raw: capabilities: [{name: "vCPUs", value: "4"}, {name: "MemoryGB", value: "16"}, ...]
Normalized: { vCPUs: 4, memoryGB: 16, ... }
```

### Key normalized fields
- `vCPUs`, `memoryGB`, `maxDataDisks`, `maxNICs`
- `cpuArchitecture` (x64 or Arm64)
- `hyperVGenerations`
- `acceleratedNetworking`, `premiumIO`, `ephemeralOSDisk`, `encryptionAtHost`
- `spotEligible`
- `zones` (availability zone support)
- `restrictions` (subscription-level restrictions)

### History Archiving
Before each data refresh, previous data files are archived to `data/history/` with timestamps. This enables the What's New feature to compare current SKU data against the previous month's snapshot and surface added/removed SKUs.

### Retirement Data
The `scripts/update-retirements.py` script scrapes Azure retirement announcements and writes `data/retirements.json`, which contains VM families being retired along with their retirement dates and recommended replacement families.

### Schedule
Data is refreshed monthly via the `refresh-vm-skus.yml` GitHub Actions workflow, which runs on a self-hosted runner at `C:\actions-runner-vmsku`. The workflow also supports manual dispatch. The app displays the refresh date prominently.

## Data Loading

### Lazy Loading
The app loads region data on demand — when a user selects a region, it fetches `data/{regionName}.json`. Data is cached in memory for the session.

### Region List
All available Azure regions are loaded from `data/regions.json` on app initialization.

### Metadata
`data/metadata.json` contains the last refresh timestamp and list of regions with available data.

### Retirement Data
Retirement data is loaded from `data/retirements.json` on app initialization and cross-referenced with SKU families to display retirement badges.

### History Data
History snapshots from `data/history/` are loaded for the What's New section, enabling comparison between current and previous data.

## Family Display Names

SKU family names from Azure (e.g., `standardDSv5Family`) are mapped to user-friendly display names (e.g., `Dsv5`) via a lookup table in the JavaScript. Unknown families are handled with a best-effort string transformation (strip `standard` prefix and `Family` suffix).

## Azure Docs Links

Each SKU family links to the relevant Azure VM size documentation page. The mapping is best-effort — if a family isn't in the lookup table, the link falls back to the general sizes overview page at `https://learn.microsoft.com/en-us/azure/virtual-machines/sizes/overview`.

## Retirement System

SKUs from families being retired show ⚠️ **Retiring** badges in the table. Data comes from `data/retirements.json`, which includes retirement dates and recommended replacement families. This data is loaded at app initialization and cross-referenced with SKU family names to flag affected SKUs.

## History & Trends (What's New)

The app compares current SKU data with the previous month's snapshot from `data/history/` to surface changes:
- **Added SKUs**: New SKUs available since the last refresh
- **Removed SKUs**: SKUs no longer available since the last refresh
- A **trend badge** appears on the summary dashboard indicating changes
- History snapshots are archived automatically during the refresh pipeline

## Filtering & Sorting

### Filters
- **Text search**: Matches against SKU name and size fields
- **Size dropdown**: Filter by size category
- **Version dropdown**: Filter by version
- **Family Type dropdown**: Filter by family type
- **vCPU Range dropdown**: Filter by vCPU range

### Column Chooser
The ⚙️ **Columns** button lets users show/hide table columns. Pin and Size columns are always visible.

### Sorting
Click any column header to sort. Clicking again toggles between ascending and descending. Supports string and numeric sorting.

### Table Display
Results are displayed grouped alphabetically by first letter with A-Z letter headers. All matching results are shown — there is no row cap.

## Find a Match (Deployment Checker)

Users specify minimum requirements to find compatible SKUs:
- **Resource requirements**: vCPUs, memory (GB), data disks, NICs
- **Feature checkboxes**: accelerated networking, premium IO, ephemeral OS disk, encryption at host, spot eligible

The app searches loaded SKU data and ranks matches by a percentage score. Results are sorted by match quality, making it easy to find the best-fit SKU.

## Pinned Shortlist

Users can pin individual SKUs from the table or from deployment checker results:
- Pinned SKUs appear as chips with key specs (vCPUs, memory, etc.)
- The section auto-expands when the first SKU is pinned
- **First-Pin Flyout**: A one-time notification appears on the first pin to introduce the feature
- Export pinned shortlist to CSV
- Clear all pins button

### Multi-Region Compare
Located inside the Pinned Shortlist section. Select up to 5 additional regions to compare against. Shows a ✅/❌ availability matrix for all pinned SKUs across selected regions. Each comparison region's data is fetched on demand.

## Snippet Modal

Click any SKU size name in the table to open a modal showing deployment code snippets:
- **Azure CLI**
- **PowerShell**
- **Bicep**

Snippets are pre-populated with the SKU name and selected region, ready to copy and use.

## Region Proximity Suggestions

When filters or the deployment checker return 0 results, the app suggests nearby Azure regions that may have the SKUs the user needs. This helps users find alternative regions without manually searching.

## Workload Recommendations

Cards for each workload type provide guided SKU selection:
- General purpose, compute-optimized, memory-optimized, storage-optimized, GPU, and more
- Each card shows which VM series are available in the currently selected region
- Badges indicate series availability

## CSV Export

The export function generates a CSV with all normalized fields (not just the visible table columns). The file includes a BOM for proper Unicode handling in Excel. The filename includes the selected region names and current date. Two export modes are available:
- **Filtered table results**: Exports the current filtered/sorted table data
- **Pinned shortlist**: Exports only the pinned SKUs

## Onboarding Experience

- **Welcome Modal**: A feature overview shown on first visit, dismissed and not shown again
- **Guided Tips**: A 3-step walkthrough after the welcome modal introduces key features
- Preferences stored in `localStorage`

## Theme System

### CSS Custom Properties
```css
:root {
  --brand-primary: #0f6cbd;
  --bg-base: #fafafa;
  --text-primary: #242424;
  /* ... */
}
```

### Dark Mode
- Toggled via header button
- Overrides CSS custom properties via JavaScript
- Preference saved to `localStorage`
- System preference detected on first visit via `prefers-color-scheme`

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `T` | Toggle light/dark theme |
| `F` | Focus search input |
| `C` | Clear all filters |
| `X` | Export to CSV |
| `?` | Show keyboard shortcuts panel |
| `Esc` | Close modals/panels |

## UI Details

- **Collapsible Sections**: All major sections use ▼/▶ toggle, collapsed by default except the region selector
- **Summary Dashboard**: Cards showing Total SKUs, vCPU Range, Memory Range with count badges
- **Data Freshness Badge**: Color-coded indicator (green/yellow/red) based on data age
- **Scrollbar Shift Fix**: `overflow-y: scroll` on `html` to prevent layout shift when content changes

## Deployment

### Azure Blob Storage
The app is hosted as a static website on Azure Blob Storage. The `$web` container serves `index.html` and the `data/` directory at the storage account's static website endpoint.

### CI/CD Pipeline
```
Push to main → GitHub Actions → az storage blob upload → Live
```

### Data Refresh Pipeline
```
Monthly cron → archive previous data → az vm list-skus → normalize-skus.py → update-retirements.py → commit → push → deploy
```

The refresh pipeline runs on a self-hosted runner at `C:\actions-runner-vmsku`.
