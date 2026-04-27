<div align="center">
  <img src="djtools.png" alt="DJ Tools — Built with GitHub Copilot CLI, deployed to Azure" width="700">
</div>

# 🖥️ Azure VM SKU by Region

![Azure](https://img.shields.io/badge/Azure-Tool-0078D4)
![License](https://img.shields.io/badge/license-MIT-blue)
![Dependencies](https://img.shields.io/badge/dependencies-zero-brightgreen)

> **Browse Azure virtual machine and managed disk SKU availability across regions — no login required.**

🔗 **[vmsku.djtools.co.nz](https://vmsku.djtools.co.nz)**

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

### 🛠️ General

| Feature | Description |
|---------|-------------|
| **Export to CSV** | Download any filtered table or your pinned shortlist |
| **Column Chooser** | Show/hide table columns via the ⚙️ Columns button |
| **Dark/Light Mode** | Toggle theme or auto-detect from your system preference |
| **Keyboard Shortcuts** | `T` theme, `F` search, `C` clear, `X` export, `?` help |
| **Region Proximity** | Suggests nearby regions when no results are found |

## 🚀 How to Use

1. **Select a region** — Choose an Azure region from the dropdown or click on the map
2. **Browse VM SKUs** — View the sortable, filterable table of available VM sizes
3. **Filter** — Narrow results by name, family, processor, vCPU range, or features
4. **Find a Match** — Set your requirements and get ranked results with match scores
5. **Pin & Compare** — Pin SKUs to your shortlist, then compare across regions
6. **View Disks** — Scroll to the Managed Disks section to browse available disk sizes
7. **Export** — Download filtered results or your pinned shortlist as CSV

## 📊 Data Freshness

All data is refreshed **monthly** from Azure APIs. Check the Data Refresh Summary (ℹ️ in the header) for the last update date.

| Data Set | Source |
|----------|--------|
| VM SKUs | Azure Resource SKU API |
| Managed Disk SKUs | Azure Resource SKU API |
| VM Pricing | Azure Retail Prices API |
| VM Retirement Dates | Azure Updates page |

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

<div align="center">
  <strong>DJ Tools</strong> — Built with <a href="https://github.com/features/copilot/cli/">GitHub Copilot CLI</a>
</div>
