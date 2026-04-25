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
VM SKU data comes from the Azure Resource SKUs API, accessed via `az vm list-skus`. This is the same data source used by the Azure Portal and CLI.

### Normalization
Raw SKU data has capabilities buried in a `capabilities[]` array of `{name, value}` pairs. The pipeline normalizes these into flat fields:

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

### Schedule
Data is refreshed monthly via a GitHub Actions workflow. The app displays the refresh date prominently.

## Data Loading

### Lazy Loading
The app loads region data on demand — when a user selects a region, it fetches `data/{regionName}.json`. Data is cached in memory for the session.

### Region List
All available Azure regions are loaded from `data/regions.json` on app initialization.

### Metadata
`data/metadata.json` contains the last refresh timestamp and list of regions with available data.

## Family Display Names

SKU family names from Azure (e.g., `standardDSv5Family`) are mapped to user-friendly display names (e.g., `Dsv5`) via a lookup table in the JavaScript. Unknown families are handled with a best-effort string transformation (strip `standard` prefix and `Family` suffix).

## Azure Docs Links

Each SKU family links to the relevant Azure VM size documentation page. The mapping is best-effort — if a family isn't in the lookup table, the link falls back to the general sizes overview page at `https://learn.microsoft.com/en-us/azure/virtual-machines/sizes/overview`.

## Filtering & Sorting

### Filters
- **Text search**: Matches against SKU name and size fields
- **Family**: Dropdown populated dynamically from loaded data
- **Architecture**: x64 or Arm64
- **vCPU count**: Predefined options (1, 2, 4, 8, 16, 32, 48, 64, 96+)

### Sorting
Click any column header to sort. Clicking again toggles between ascending and descending. Supports string and numeric sorting.

### Performance
Table rendering is capped at 500 rows. For larger result sets, a message indicates the cap.

## CSV Export

The export function generates a CSV with all normalized fields (not just the visible table columns). The file includes a BOM for proper Unicode handling in Excel. The filename includes the selected region names and current date.

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

## Deployment

### Azure Blob Storage
The app is hosted as a static website on Azure Blob Storage. The `$web` container serves `index.html` and the `data/` directory at the storage account's static website endpoint.

### CI/CD Pipeline
```
Push to main → GitHub Actions → az storage blob upload → Live
```

### Data Refresh Pipeline
```
Monthly cron → az vm list-skus → normalize → commit → push → deploy
```
