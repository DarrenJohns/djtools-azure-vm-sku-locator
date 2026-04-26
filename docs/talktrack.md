# Talk Track — VM SKU Per Region Demo

> Version: v0.2.0
> Duration: ~20 minutes

## Opening (2 min)

**"Today I'll show you VM SKU Per Region — what started as a simple SKU browser has grown into a comprehensive VM planning tool for Azure. It lets you browse, filter, match, compare, and plan VM deployments across any Azure region — all without logging in or running CLI commands."**

## The Problem (2 min)

**"If you're an Azure VM admin and need to know what VM sizes are available in a specific region, your options today are:**
- **Run `az vm list-skus --location <region>`** — requires CLI setup, authentication, and outputs raw data
- **Check the Azure Portal** — requires login, navigation through multiple blades
- **Read Azure docs** — generic, doesn't show region-specific availability

**This tool gives you instant, searchable access to VM SKU availability across regions — plus matching, comparing, and deployment-ready code snippets."**

## Live Demo (13 min)

### Region Selection (1 min)

**"Let's start by picking a region."**

- Default region is New Zealand North (my home region!)
- Show the region dropdown — regions are grouped by geography for easy navigation
- Point out the summary dashboard cards at the top: **Total SKUs**, **vCPU Range**, **Memory Range**
- Call out the **Data Freshness** badge — it's color-coded green/yellow/red so you know how current the data is

### Browse SKUs — "See What's Available" (2 min)

**"Now let's see what's actually available in this region."**

- Expand the collapsible **Browse SKUs** section
- Show the full SKU table — results are letter-grouped for easy scanning
- Type in the search box to filter (e.g., "D4" to find all D4-series VMs)
- Show the filter dropdowns: **Size**, **Version**, **Family Type**, **vCPU Range**
- Click the **⚙️ Columns** button to open the Column Chooser — customize which columns are visible
- Click a SKU size name to pop open the **Snippet Modal** — ready-to-paste code for CLI, PowerShell, and Bicep

**"So you can go from browsing to deploying in seconds."**

### Retirement Badges (1 min)

**"One thing to watch for — see these ⚠️ Retiring badges?"**

- Point out the retirement warning badges on affected SKUs
- Explain that retirement data is refreshed monthly from official Azure announcements
- **"This saves you from accidentally planning a deployment on a SKU that's being retired."**

### Find a Match — Deployment Checker (2 min)

**"What if you don't know which SKU you need? Let's say you have requirements and want the tool to find the best fit."**

- Set requirements: e.g., minimum **4 vCPUs**, **16 GB memory**
- Check **Accelerated Networking** and **Premium IO**
- Click **Find a Match**
- Show the ranked results with **percentage match scores**
- **"The checker scores each SKU against your requirements and ranks them — 100% means it meets everything you asked for. Lower scores show where a SKU falls short."**

### Pin & Compare (3 min)

**"Now here's where it gets really useful for planning. Let's pin a few candidates."**

- Pin 2–3 SKUs from the table or the checker results
- Show the **Pinned Shortlist** section auto-expanding at the bottom
- Point out the SKU chips showing key specs at a glance
- Demo **Multi-Region Compare**: select 2–3 regions (e.g., New Zealand North, Australia East, Southeast Asia)
- Show the **✅/❌ availability matrix** — instantly see which SKUs are available where
- Click **Export CSV** to download the pinned shortlist

**"So if you're planning a multi-region deployment, you can see availability side by side and export the shortlist for your team."**

### What's New (1 min)

**"The data refreshes monthly, and we track what changed."**

- Show the **What's New** section — SKUs added and removed since the last refresh
- Point out the **trend badge** on the dashboard card

**"This is great for staying on top of new SKU launches or quiet deprecations."**

### Workload Recommendations (1 min)

**"We also have workload-based recommendations."**

- Show the workload cards (e.g., general purpose, memory-optimized, compute-optimized)
- Point out the **series availability badges** showing which families are available in the selected region

### Quick Hits (2 min)

**"A few more things worth showing quickly."**

- **Dark mode** — press **T** to toggle (great for demos in dim rooms!)
- **Keyboard shortcuts** — press **?** to see the full list
- **Region proximity suggestions** — filter to something with 0 results and show the suggested nearby regions
- **Welcome modal and guided tips** — mention these appear for first-time users to help them get oriented

## How It Was Built (3 min)

**"This entire app was built using GitHub Copilot CLI in my terminal."**

### Key Points
- **Single-file architecture** — One HTML file, no frameworks, no build tools
- **Pre-fetched data** — Monthly refresh via GitHub Actions, no user authentication
- **Zero dependencies** — Nothing to install or update
- **AI-assisted development** — Copilot CLI wrote the code, created the repo, set up CI/CD

### Configuration & Scripts
- **`config.json`** — controls which regions are included and app settings
- **`scripts/normalize-skus.py`** — transforms raw `az vm list-skus` output into clean, flat JSON
- **`scripts/update-retirements.py`** — pulls retirement dates from Azure announcements
- **History archiving** — previous data snapshots are archived so the What's New feature can diff them

### Data Pipeline
- Monthly cron trigger on a **self-hosted runner** at `C:\actions-runner-vmsku`
- Archive previous data snapshot
- Run `az vm list-skus` for all configured regions
- Normalize raw data to clean JSON via `normalize-skus.py`
- Update retirement info via `update-retirements.py`
- Commit updated data and deploy to GitHub Pages

## Wrap Up (2 min)

**"VM SKU Per Region has grown from a simple browser into a full VM planning toolkit. You can browse and filter SKUs, check retirement status, match against your requirements, pin and compare across regions, and export everything — all without logging in. Data refreshes monthly, and the CLI guidance is right there for when you need real-time subscription-specific data."**

### Links
- [GitHub Copilot CLI](https://github.com/features/copilot/cli/)
- [Azure VM Sizes](https://learn.microsoft.com/en-us/azure/virtual-machines/sizes/overview)
- [Azure CLI — az vm list-skus](https://learn.microsoft.com/en-us/cli/azure/vm#az-vm-list-skus)
