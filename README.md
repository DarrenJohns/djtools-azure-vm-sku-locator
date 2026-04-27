# 🖥️ Azure VM SKU by Region

<div align="center">
  <img src="djtools.png" alt="DJ Tools — Built with GitHub Copilot CLI, deployed to Azure" width="700">
</div>

> **Built by an infrastructure solution architect who doesn't write code for a living — this app was vibe-crafted using [GitHub Copilot CLI](https://github.com/features/copilot/cli/) and deployed to [Azure Static Web Apps](https://azure.microsoft.com/products/app-service/static). From idea 💡 to production web app, without writing a single line of code manually.**
>
> **Browse Azure VM and managed disk SKU availability across every region — filter by processor, family, and features, compare across regions, and export deployment-ready code.**

![Version](https://img.shields.io/badge/version-1.0.0--beta-orange)
![Azure](https://img.shields.io/badge/Azure-VM_SKUs-0078D4)
![License](https://img.shields.io/badge/license-MIT-blue)
![Built with](https://img.shields.io/badge/built_with-Copilot_CLI-8957e5)
![Hosted on](https://img.shields.io/badge/hosted_on-Azure_SWA-0078D4)

👉 **Try the live app here → [vmsku.djtools.co.nz](https://vmsku.djtools.co.nz)**

---

## ✨ What You Can Do

### 🖥️ Virtual Machine SKUs

| Feature | Description |
|---------|-------------|
| **Browse by Region** | Select an Azure region to view all available VM sizes |
| **Search & Filter** | Filter by name, family, vCPU range, processor type (Intel/AMD/ARM), and more |
| **Find a Match** | Specify your requirements (vCPUs, memory, disks, NICs, features) and get ranked matches with percentage scores |
| **Pin & Compare** | Pin SKUs to a shortlist, then compare availability across up to 5 other regions |
| **Deployment Snippets** | Click any SKU for ready-to-use Azure CLI, PowerShell, and Bicep code |
| **Retirement Warnings** | SKUs from families being retired are flagged with a warning badge |
| **What's New** | See which SKUs were added or removed since the last monthly refresh |
| **Workload Recommendations** | View which VM series suit different workload types |

### 💿 Managed Disk SKUs

| Feature | Description |
|---------|-------------|
| **Browse Disk Tiers** | View Premium SSD, Standard SSD, Standard HDD, Ultra, and PremiumV2 disks |
| **Filter & Search** | Filter by disk type, redundancy (LRS/ZRS), availability zones, and IOPS range |
| **Performance Details** | See max IOPS, throughput, burst capabilities, and max shares per disk size |
| **Export** | Download disk data as CSV |

### 🎨 General

| Feature | Description |
|---------|-------------|
| **Export to CSV** | Download any filtered table or your pinned shortlist |
| **Column Chooser** | Show/hide table columns via the ⚙️ Columns button |
| **Dark/Light Mode** | Toggle theme or auto-detect from your system preference |
| **Keyboard Shortcuts** | `T` theme, `F` search, `C` clear, `X` export, `?` help |
| **Region Proximity** | Suggests nearby regions when no results are found |
| **Zero Dependencies** | Single HTML file — no frameworks, no build step |

---

## 🚀 How to Use

1. **Select a region** — Choose an Azure region from the dropdown or click on the map
2. **Browse VM SKUs** — View the sortable, filterable table of available VM sizes
3. **Filter** — Narrow results by name, family, processor, vCPU range, or features
4. **Find a Match** — Set your requirements and get ranked results with match scores
5. **Pin & Compare** — Pin SKUs to your shortlist, then compare across regions
6. **View Disks** — Scroll to the Managed Disks section to browse available disk sizes
7. **Export** — Download filtered results or your pinned shortlist as CSV

---

## 📊 Data Freshness

All data is refreshed **monthly** from Azure APIs. Check the Data Refresh Summary (ℹ️ in the header) for the last update date.

| Data Set | Source |
|----------|--------|
| VM SKUs | Azure Resource SKU API |
| Managed Disk SKUs | Azure Resource SKU API |
| VM Pricing | Azure Retail Prices API |
| VM Retirement Dates | Azure Updates page |

---

## 🗂️ Project Structure

```
vm-sku-per-region/
├── index.html                    # The app (single file, zero dependencies)
├── config.json                   # Region configuration
├── README.md                     # This file
├── LICENSE                       # MIT license
├── SECURITY.md                   # Security reporting policy
├── data/
│   ├── regions.json              # Available regions list
│   ├── metadata.json             # Data refresh timestamps
│   ├── retirements.json          # VM family retirement dates
│   ├── <region>.json             # VM SKU data per region
│   ├── <region>-disks.json       # Disk SKU data per region
│   ├── <region>-pricing.json     # Pricing data per region
│   └── history/                  # Monthly SKU snapshots for What's New
├── scripts/
│   ├── normalize-skus.py         # VM SKU data pipeline
│   ├── normalize-disks.py        # Disk SKU data pipeline
│   ├── fetch-pricing.py          # Pricing data fetcher
│   └── update-retirements.py     # Retirement date scraper
├── docs/
│   ├── SPEC.md                   # App specification
│   ├── howitworks.md             # Technical documentation
│   └── talktrack.md              # Demo talk track
├── .github/
│   ├── workflows/
│   │   ├── deploy.yml            # CI/CD: auto-deploy to Azure SWA
│   │   ├── refresh-vm-skus.yml   # Monthly data refresh pipeline
│   │   └── validate.yml          # HTML validation on pull requests
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.yml        # Structured bug report form
│   │   └── feature_request.yml   # Feature request form
│   ├── pull_request_template.md  # PR checklist template
│   └── copilot-instructions.md   # Copilot CLI context
└── .gitignore
```

---

## 🤝 Contributing

Contributions, ideas, and feedback are welcome!

1. Create a branch from `main` (`feature/`, `fix/`, or `docs/` prefix)
2. Make your changes and test locally in the browser
3. Open a Pull Request — the PR template will guide you
4. After review and approval, merge to `main` → auto-deploys to Azure

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

<div align="center">
  <strong>DJ Tools</strong> — Built with <a href="https://github.com/features/copilot/cli/">GitHub Copilot CLI</a>
</div>
