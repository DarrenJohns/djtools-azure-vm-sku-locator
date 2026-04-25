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
3. Runs `az vm list-skus` for each region
4. Normalizes raw capabilities into flat fields
5. Saves per-region JSON to `data/` directory
6. Updates `metadata.json` with refresh timestamp
7. Commits and pushes (triggers deploy)

### Family Display Names
SKU family names (e.g., `standardDSv5Family`) are mapped to user-friendly names (e.g., `Dsv5`) and Azure documentation URLs. This mapping is best-effort — unknown families fall back to the general sizes overview page.

## 5. User Interface

### Region Selector
- Dropdown of all Azure regions
- "Add Region" button to add to selection
- Region chips showing selected regions with remove button
- Maximum 5 regions selectable simultaneously

### Filters
- Text search (SKU name)
- Family dropdown
- Architecture dropdown (x64 / Arm64)
- vCPU count filter
- Reset button

### SKU Table
- Sortable by clicking column headers
- Columns: SKU Name, Family, vCPUs, Memory, Architecture, Zones, Data Disks, Features, Region, Docs link
- Feature indicators: AccelNet, PremIO, EphOS, EncHost, Spot
- Capped at 500 rows for performance

### Export
- CSV download of currently filtered results
- Includes all fields (not just visible columns)
- Filename includes region names and date

### CLI Guidance
- Collapsible section with `az vm list-skus` command
- Updates dynamically based on selected region
- Links to Azure CLI installation docs

## 6. Theme
- Light and dark mode with system detection
- Toggle via header button
- Preference saved to localStorage

## 7. Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+F` | Focus search input |
| `Enter` | Add region (when region dropdown focused) |

## 8. Deployment

- **Hosting**: Azure Blob Storage `$web` container
- **CI/CD**: GitHub Actions workflow on push to `main`
- **Runner**: Self-hosted runner at `C:\actions-runner`
- **Data files**: Deployed alongside `index.html` in `data/` directory
