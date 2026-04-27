# Talk Track — Azure VM SKU by Region Demo

> Duration: ~20 minutes

🔗 **[vmsku.djtools.co.nz](https://vmsku.djtools.co.nz)**

## Opening (2 min)

**"Today I'll show you Azure VM SKU by Region — a comprehensive VM and disk planning tool for Azure. It lets you browse, filter, match, and compare VM and disk SKUs across any Azure region — all without logging in or running CLI commands."**

## The Problem (2 min)

**"If you're an Azure VM admin and need to know what VM sizes or disk types are available in a specific region, your options today are:**
- **Azure Portal** — requires login, navigation through multiple blades
- **Azure CLI** — requires setup, authentication, outputs raw data
- **Azure docs** — generic, doesn't show region-specific availability

**This tool gives you instant, searchable access to VM and disk SKU availability — plus matching, comparing, pricing, and deployment-ready code."**

## Live Demo (13 min)

### Region Selection (1 min)

**"Let's start by picking a region."**

- Default region is New Zealand North
- Show the region dropdown — regions are grouped by geography
- Point out the KPI dashboard cards: **Total SKUs**, **vCPU Range**, **Memory Range**, **Intel/AMD/ARM counts**
- Call out the **Data Freshness** badge — color-coded green/yellow/red

### Browse VM SKUs — "See What's Available" (2 min)

**"Now let's see what's actually available."**

- Expand the **Browse SKUs** section
- Show the full table — results are letter-grouped
- Demo the filters: **text search**, **family type**, **vCPU range**, **processor type** (Intel/AMD/ARM)
- Click **⚙️ Columns** to customize visible columns
- Click a SKU name for the **Snippet Modal** — CLI, PowerShell, and Bicep code ready to copy
- Point out **retirement badges** on affected SKUs

**"So you can go from browsing to deploying in seconds."**

### Find a Match (2 min)

**"What if you don't know which SKU you need?"**

- Set requirements: **4 vCPUs**, **16 GB memory**, **AMD processor**
- Check **Accelerated Networking** and **Premium IO**
- Click **Find a Match**
- Show ranked results with **percentage match scores**

**"100% means it meets everything. Lower scores show where a SKU falls short."**

### Pin & Compare (2 min)

**"Let's pin a few candidates and compare across regions."**

- Pin 2–3 SKUs from the table or checker results
- Show the **Pinned Shortlist** with spec chips
- Demo **Multi-Region Compare**: select Australia East and Southeast Asia
- Show the **✅/❌ availability matrix**
- Click **Export CSV** to download

**"Perfect for planning multi-region deployments."**

### Disk SKUs (2 min)

**"We also have managed disk information."**

- Scroll to the **💿 Managed Disks** section
- Show tier summary cards: Premium SSD, Standard SSD, Standard HDD, Ultra
- Expand a disk group — show IOPS, throughput, burst capabilities
- Demo filters: disk type, redundancy (LRS/ZRS), IOPS range
- Export disk data to CSV

**"Same region-specific data, but for disks — IOPS, throughput, burst, zone support."**

### What's New & Workloads (2 min)

- Show **What's New** — SKUs added/removed since last refresh
- Show **Workload Recommendations** — cards showing which VM series suit each workload type
- Point out series availability badges for the selected region

### Quick Hits (2 min)

- **Dark mode** — press **T** to toggle
- **Keyboard shortcuts** — press **?** for the full list
- **Region proximity** — suggests nearby regions when no results found
- **Data Refresh Summary** — click ℹ️ to see all data sets and their sources

## How It Was Built (3 min)

**"This entire app was built using GitHub Copilot CLI in my terminal."**

### Key Points
- **Single-file architecture** — one HTML file, no frameworks, no build tools, zero dependencies
- **Pre-fetched data** — monthly refresh via GitHub Actions, no user authentication required
- **Four data sources** — VM SKUs, disk SKUs, pricing, and retirement dates
- **AI-assisted development** — Copilot CLI wrote the code, created the repo, set up CI/CD
- **Hosted on Azure Static Web Apps** — free tier with custom domain and managed SSL

### Data Pipeline
- Manual or monthly trigger on a self-hosted runner
- Fetches VM SKUs, disk SKUs, pricing, and retirement data
- Normalizes and deploys to Azure Static Web Apps
- Commits updated data to the repo

## Wrap Up (2 min)

**"Azure VM SKU by Region is a full VM and disk planning toolkit. Browse and filter SKUs, check retirement status, match against requirements, compare across regions, review disk options — all without logging in. Data refreshes monthly from Azure APIs, and deployment snippets are ready to copy."**

### Links
- 🔗 [vmsku.djtools.co.nz](https://vmsku.djtools.co.nz)
- [GitHub Copilot CLI](https://github.com/features/copilot/cli/)
- [Azure VM Sizes](https://learn.microsoft.com/en-us/azure/virtual-machines/sizes/overview)
