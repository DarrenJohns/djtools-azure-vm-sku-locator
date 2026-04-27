# VM SKU Per Region — Specification

> Version: v1.0.0-beta

## 1. Overview

This application helps Azure VM administrators browse virtual machine SKU availability across Azure regions. It displays pre-fetched SKU data with filtering, sorting, pricing, and CSV export — no authentication required.

**Target users:** Azure infrastructure administrators who need to understand what VM sizes and disk SKUs are available in specific regions before deploying.

**Live app:** [vmsku.djtools.co.nz](https://vmsku.djtools.co.nz)

## 2. Architecture

- **Type**: Single-file HTML web application (`index.html`) with static JSON data files
- **Frameworks**: None — pure HTML/CSS/JavaScript (inline)
- **Dependencies**: Zero external dependencies (no CDN, no npm packages)
- **Data source**: Pre-fetched from Azure Resource SKUs API (`az vm list-skus`) and Azure Retail Prices API
- **Data refresh**: Monthly via GitHub Actions scheduled workflow
- **Authentication**: None required — all data is pre-fetched
- **Hosting**: Azure Static Web Apps (SWA)
- **CI/CD**: GitHub Actions → SWA CLI deploy on push to main
- **Custom domain**: `vmsku.djtools.co.nz`

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

### Disk SKU Data (per-region, embedded in region JSON)

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Disk SKU name (e.g., `Premium_LRS`) |
| `tier` | string | Disk tier (Premium, Standard, Ultra) |
| `size` | string | Disk size identifier |
| `maxSizeGB` | number | Maximum disk size in GB |
| `maxIOPS` | number | Maximum IOPS |
| `maxThroughputMBps` | number | Maximum throughput in MB/s |
| `zones` | string[] | Available availability zones |

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

### Metadata (`data/metadata.json`)

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

All UI sections use a consistent collapsible header pattern with toggle arrow (left), title (center, flex), and badge (right, outlined pill).

### Region Selector & Freshness Status
- Single region dropdown (default: New Zealand North)
- Regions grouped by geography in the dropdown
- Sticky header with data freshness badge (color-coded green/yellow/red)
- Freshness shows "Updated {Month} {Year}" (e.g., "Updated April 2026")
- No-data fallback shows CLI command for regions without pre-fetched data

### Summary Dashboard (KPI Cards)
- Cards showing Total SKUs, vCPU Range, Memory Range, Families, Architecture split
- Data freshness badge with staleness thresholds (≤30d green, ≤60d yellow, >60d red)

### 📊 What's New (History/Trends)
- Section showing SKUs added/removed since last monthly refresh
- Trend badge displayed on the section header
- Compares current data against archived history snapshots

### 🔍 See What's Available
- **Filters**: Text search, Family, Size, Version, Architecture, vCPU Range dropdowns, Reset button
- **SKU Table**: Results grouped by family with collapsible letter sections
  - Sortable by clicking column headers
  - Column Chooser (⚙️ Columns) lets users show/hide columns; Pin and Size columns always visible
  - Feature indicators: AccelNet, PremIO, EphOS, EncHost, Spot
  - ⚠️ Retiring badge on SKUs from families being retired
  - Expand All / Collapse All / Clear All Pins action buttons
- **CSV export** of currently filtered results (filename includes region and date)
- **Region proximity suggestions**: When filters return 0 results, suggests nearby regions with matching SKUs

### 🎯 Find a Match (Deployment Checker)
- Users specify requirements: min vCPUs, min memory, min data disks, min NICs
- Checkboxes for features (accelerated networking, premium IO, etc.)
- Finds and ranks matching SKUs with percentage match scores
- Expand All / Collapse All / Clear All Pins action buttons
- Export matching results to CSV

### 📌 Pinned Shortlist
- Pin individual SKUs from the table or deployment checker
- Pinned SKUs show as chips with key specs and pricing (Pay-As-You-Go)
- Section auto-expands on first pin
- Export shortlist to CSV
- Clear all pins button
- **Pricing comparison**: Fetches live pricing from Azure Retail Prices API, cached per region
- **Multi-Region Compare**: Select up to 5 other regions, shows ✅/❌ availability matrix for pinned SKUs

### 💿 Disk SKUs
- Displays managed disk SKUs available in the selected region
- Filters: Tier (Premium/Standard/Ultra), Redundancy, Zone support, IOPS range
- Table with sortable columns: Name, Tier, Max Size, Max IOPS, Max Throughput, Zones
- CSV export

### Workload Recommendations
- Cards for each workload type (general purpose, compute-optimized, memory-optimized, GPU, HPC, etc.)
- Shows which VM series are available in the selected region with badges

### 🔤 Azure VM Naming Convention
- Interactive decoder showing the naming structure of Azure VM sizes
- Breaks down family, sub-family, vCPUs, features, version segments
- Helps users understand what a SKU name means

### Snippet Modal
- Click any SKU size name to open a modal
- Provides Azure CLI, PowerShell, and Bicep deployment code snippets for that SKU
- Copy-to-clipboard buttons

### 🛠️ CLI Guidance
- Collapsible section with `az vm list-skus` command
- Updates dynamically based on selected region
- Links to Azure CLI installation docs

### Welcome Modal
- Feature overview shown on first visit
- Dismissable, won't show again

### Guided Tips
- 3-step walkthrough shown after welcome modal dismissal
- Highlights key features: region selector, filters, pinning

### First-Pin Flyout
- One-time notification when user pins their first SKU
- Points to the Pinned Shortlist section

## 6. Theme
- Light and dark mode with system detection
- Toggle via header button (☀️/🌙)
- Preference saved to localStorage
- Consistent Fluent-inspired design language

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

- **Hosting**: Azure Static Web Apps (SWA)
- **Custom domain**: `vmsku.djtools.co.nz`
- **CI/CD**: GitHub Actions workflow on push to `main` (triggers on `index.html`, `data/**`, `config.json`)
- **Deploy tool**: `@azure/static-web-apps-cli` with `SWA_DEPLOYMENT_TOKEN`
- **Runner**: Self-hosted runner
- **Environment**: `production` (enables GitHub deployment tracking)
- **Staged deploy**: Only `index.html`, `config.json`, and `data/` are deployed (not scripts, docs, etc.)
