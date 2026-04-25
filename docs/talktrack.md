# Talk Track — VM SKU Per Region Demo

> Version: v0.0.1-beta
> Duration: ~15 minutes

## Opening (2 min)

**"Today I'll show you VM SKU Per Region, a tool that helps Azure VM administrators quickly see what virtual machine sizes are available in any Azure region — without needing to log in or run CLI commands."**

## The Problem (2 min)

**"If you're an Azure VM admin and need to know what VM sizes are available in a specific region, your options today are:**
- **Run `az vm list-skus --location <region>`** — requires CLI setup, authentication, and outputs raw data
- **Check the Azure Portal** — requires login, navigation through multiple blades
- **Read Azure docs** — generic, doesn't show region-specific availability

**This tool gives you instant, searchable access to VM SKU availability across regions."**

## Live Demo (8 min)

### Region Selection
- Default region is New Zealand North (my home region!)
- Show the region dropdown with 100+ Azure regions
- Add a region, show the chip appearing
- Add a second region to compare (e.g., Australia East)

### Filtering & Search
- Type "D4" to find all D4-series VMs
- Filter by Arm64 architecture
- Filter by 8 vCPUs
- Show the result count updating in real time

### Table Features
- Click column headers to sort (by vCPUs, memory, name)
- Point out the feature indicators (AccelNet, PremIO, Spot)
- Show availability zones column
- Click a docs link to open Azure documentation

### Export
- Filter to a specific family
- Click Export CSV
- Show the downloaded file

### Real-Time Data
- Expand the CLI guidance section
- Show the `az vm list-skus` command
- Explain when real-time data matters (subscription restrictions)

## How It Was Built (3 min)

**"This entire app was built using GitHub Copilot CLI in my terminal."**

### Key Points
- **Single-file architecture** — One HTML file, no frameworks, no build tools
- **Pre-fetched data** — Monthly refresh via GitHub Actions, no user authentication
- **Zero dependencies** — Nothing to install or update
- **AI-assisted development** — Copilot CLI wrote the code, created the repo, set up CI/CD

### Data Pipeline
- Monthly GitHub Actions workflow runs `az vm list-skus` for all regions
- Raw data normalized to clean JSON with flat fields
- Deployed alongside the app as static files

## Wrap Up (2 min)

**"VM SKU Per Region turns a CLI command into an instant, searchable web experience. No login needed, data refreshed monthly, and the CLI guidance is right there for when you need real-time subscription-specific data."**

### Links
- [GitHub Copilot CLI](https://github.com/features/copilot/cli/)
- [Azure VM Sizes](https://learn.microsoft.com/en-us/azure/virtual-machines/sizes/overview)
- [Azure CLI — az vm list-skus](https://learn.microsoft.com/en-us/cli/azure/vm#az-vm-list-skus)
