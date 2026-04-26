# VM SKU Per Region — Specification

> Version: v0.0.1-beta

## 1. Overview

This application helps Azure VM administrators browse virtual machine SKU availability across Azure regions. It displays pre-fetched SKU data with filtering, sorting, and CSV export — no authentication required.

**Target users:** Azure infrastructure administrators who need to understand what VM sizes are available in specific regions before deploying.

## 2. Architecture

- **Type**: Single-file HTML web application (`index.html`) with static JSON data files
- **Frameworks**: None — pure HTML/CSS/JavaScript
- **Dependencies**: Zero external dependencies
- **Data source**: Pre-fetched from Azure Resource SKUs API (`az vm list-skus`)
- **Data refresh**: Monthly via GitHub Actions scheduled workflow
- **Authentication**: None required — all data is pre-fetched
- **Hosting**: Azure Blob Storage static website
- **CI/CD**: GitHub Actions → Azure Storage deploy on push to main

## 3. Data Model

### Region SKU Data (per-region JSON)

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | VM SKU name (e.g., `Standard_D2s_v5`) |
| `family` | string | SKU family (e.g., `standardDSv5Family`) |
| `tier` | string | Tier (`Standard`) |
| `size` | string | Size identifier (e.g., `D2s_v5`) |
| `vCPUs` | number | Number of virtual CPUs |
| `memoryGB` | number | Memory in gigabytes |
| `maxDataDisks` | number | Maximum data disks |
| `maxNICs` | number | Maximum network interfaces |
| `cpuArchitecture` | string | `x64` or `Arm64` |
| `hyperVGenerations` | string | Supported Hyper-V generations |
| `acceleratedNetworking` | boolean | Accelerated networking support |
| `premiumIO` | boolean | Premium storage support |
| `ephemeralOSDisk` | boolean | Ephemeral OS disk support |
| `encryptionAtHost` | boolean | Encryption at host support |
| `spotEligible` | boolean | Spot VM eligibility |
| `zones` | string[] | Available availability zones |
| `restrictions` | string[] | Restriction reason codes |

### Retirement Data (`data/retirements.json`)

| Field | Type | Description |
|-------|------|-------------|
| `family` | string | VM family name being retired |
| `retirementDate` | string | Planned retirement date |
| `replacementFamily` | string | Recommended replacement family |

### History Snapshots (`data/history/`)

Monthly archives of previous SKU data, used for tracking changes over time (What's New feature). Each snapshot captures the full per-region JSON from the prior refresh cycle.

### Region Configuration (`config.json`)

Target regions for data refresh. Defines which Azure regions are included in the scheduled pipeline run.

### Metadata

| Field | Type | Description |
|-------|------|-------------|
| `lastUpdated` | ISO 8601 | Timestamp of last data refresh |
| `lastUpdatedDisplay` | string | Human-readable month (e.g., "April 2026") |
| `availableRegions` | string[] | Regions with data files |

## 4. Data Pipeline

### Refresh Process
1. GitHub Actions cron job runs monthly
2. Authenticates via service principal / OIDC
3. Archives previous data to `data/history/` before overwriting (for What's New feature)
4. Reads target regions from `config.json`
5. Runs `az vm list-skus` for each configured region
6. Normalizes raw capabilities into flat fields via `scripts/normalize-skus.py`
7. Refreshes retirement data via `scripts/update-retirements.py`
8. Saves per-region JSON to `data/` directory
9. Updates `metadata.json` with refresh timestamp
10. Commits and pushes (triggers deploy)

### Family Display Names
SKU family names (e.g., `standardDSv5Family`) are mapped to user-friendly names (e.g., `Dsv5`) and Azure documentation URLs. This mapping is best-effort — unknown families fall back to the general sizes overview page.

## 5. User Interface

### Region Selector
- Single region dropdown (default: New Zealand North)
- Regions grouped by geography in the dropdown

### Filters
- Text search (SKU name)
- Dropdowns for Size, Version, Family Type, and vCPU Range
- Reset button

### SKU Table
- Displays all results grouped by first letter (A–Z sections)
- Sortable by clicking column headers
- Column Chooser (⚙️ Columns button) lets users show/hide columns; Pin and Size columns are always visible
- Feature indicators: AccelNet, PremIO, EphOS, EncHost, Spot
- ⚠️ Retiring badge shown on SKUs from families being retired (data loaded from `data/retirements.json`)

### Summary Dashboard
- Cards showing Total SKUs, vCPU Range, Memory Range
- Data Freshness badge (color-coded green/yellow/red based on age of data)

### Find a Match (Deployment Checker)
- Users specify requirements: min vCPUs, min memory, min data disks, min NICs
- Checkboxes for features (accelerated networking, premium IO, etc.)
- App finds and ranks matching SKUs with percentage match scores

### Pinned Shortlist
- Users can pin individual SKUs from the table or deployment checker
- Pinned SKUs show as chips with key specs
- Section auto-expands on first pin
- Export shortlist to CSV
- Clear all pins button

### Multi-Region Compare
- Located inside the Pinned Shortlist section
- Select up to 5 other regions
- Shows ✅/❌ availability matrix for pinned SKUs across selected regions

### Snippet Modal
- Click any SKU size name to open a modal
- Provides Azure CLI, PowerShell, and Bicep deployment code snippets for that SKU

### Workload Recommendations
- Cards for each workload type (general purpose, compute-optimized, memory-optimized, etc.)
- Shows which series are available with badges

### What's New (History/Trends)
- Section showing SKUs added/removed since last monthly refresh
- Trend badge displayed on the summary dashboard

### Region Proximity Suggestions
- When filters or deployment checker return 0 results, suggests nearby Azure regions that might have matching SKUs

### Export
- CSV download of currently filtered results
- Includes all fields (not just visible columns)
- Filename includes region name and date

### CLI Guidance
- Collapsible section with `az vm list-skus` command
- Updates dynamically based on selected region
- Links to Azure CLI installation docs

### Welcome Modal
- Feature overview shown on first visit

### Guided Tips
- 3-step walkthrough shown after welcome modal dismissal

### First-Pin Flyout
- One-time notification when user pins their first SKU

## 6. Theme
- Light and dark mode with system detection
- Toggle via header button
- Preference saved to localStorage

## 7. Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `T` | Toggle light/dark theme |
| `F` | Focus search input |
| `C` | Clear all filters |
| `X` | Export to CSV |
| `?` | Show keyboard shortcuts panel |
| `Esc` | Close modals/panels |

## 8. Deployment

- **Hosting**: Azure Blob Storage `$web` container
- **CI/CD**: GitHub Actions workflow on push to `main`
- **Runner**: Self-hosted runner at `C:\actions-runner-vmsku`
- **Data files**: Deployed alongside `index.html` in `data/` directory
