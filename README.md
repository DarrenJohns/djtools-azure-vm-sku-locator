# 🖥️ VM SKU Per Region

![Deploy](https://img.shields.io/badge/deploy-not_configured-lightgrey)
![License](https://img.shields.io/badge/license-MIT-blue)
![Azure](https://img.shields.io/badge/Azure-Tool-0078D4)
![Version](https://img.shields.io/badge/version-0.0.1--beta-orange)
![Dependencies](https://img.shields.io/badge/dependencies-zero-brightgreen)

> **Browse Azure virtual machine SKU availability across regions — no login required.**

---

## ✨ Features

| Category | Features |
|----------|----------|
| **Browse** | Select an Azure region to view available VM SKUs |
| **Search & Filter** | Filter by SKU name, size, version, family type, vCPU range |
| **Find a Match** | Specify requirements (vCPUs, memory, disks, NICs + feature checkboxes) and get ranked matches with percentage scores |
| **Pinned Shortlist** | Pin SKUs, view as chips with specs, export shortlist to CSV |
| **Multi-Region Compare** | Compare pinned SKU availability across up to 5 other regions |
| **Column Chooser** | Show/hide table columns via ⚙️ Columns button |
| **Snippet Modal** | Click any SKU to see Azure CLI, PowerShell, and Bicep deployment snippets |
| **Workload Recommendations** | Cards with series availability badges per workload type |
| **What's New** | SKUs added/removed since last monthly refresh with trend badges |
| **Retirement Badges** | ⚠️ warnings on SKUs from families being retired |
| **Region Proximity** | Suggests nearby regions when no results found |
| **Export** | Download filtered results or pinned shortlist as CSV |
| **Theme** | Light/dark mode with system detection |
| **Keyboard Shortcuts** | `T` (theme), `F` (focus search), `C` (clear), `X` (export), `?` (shortcuts panel) |

## 🚀 Getting Started

This is a single-file HTML web application with pre-fetched static data — no installation, build tools, login, or dependencies required.

### Run Locally

Serve the project directory with any HTTP server (data files need to be fetched):

```bash
python -m http.server 8090
# Then open http://localhost:8090
```

### How to Use

1. **Select a region** — Choose an Azure region from the dropdown (default: New Zealand North)
2. **Browse SKUs** — View the sortable, filterable table of available VM sizes
3. **Filter** — Search by name, size, version, family type, or vCPU range
4. **Find a Match** — Specify your requirements and get ranked results with percentage scores
5. **Pin & Compare** — Pin SKUs to your shortlist, then compare availability across up to 5 other regions
6. **Snippets** — Click any SKU to see Azure CLI, PowerShell, and Bicep deployment snippets
7. **Export** — Download filtered results or your pinned shortlist as CSV
8. **Real-time data** — For subscription-specific availability, use `az vm list-skus`

### Data Freshness

SKU data is refreshed **monthly**. The app displays "Data current as of: [month]" to indicate freshness. For real-time, subscription-specific availability (including restrictions), use:

```bash
az vm list-skus --location <region> --resource-type virtualMachines -o table
```

This requires Azure CLI and at least **Reader** role on your subscription.

## 🏗️ Architecture

| Aspect | Details |
|--------|---------|
| **Type** | Single-file HTML web application with static JSON data |
| **Frameworks** | None — pure HTML/CSS/JS |
| **Dependencies** | Zero |
| **Data source** | Pre-fetched from `az vm list-skus`, normalized to JSON |
| **Configuration** | `config.json` defines target regions for data refresh |
| **Scripts** | `scripts/normalize-skus.py` and `scripts/update-retirements.py` for data pipeline |
| **Data refresh** | Monthly via GitHub Actions scheduled workflow |
| **Authentication** | None required — data is pre-fetched |
| **Build step** | None — file deploys directly |
| **Hosting** | Azure Blob Storage static website |
| **CI/CD** | GitHub Actions with self-hosted runner |

## 📁 Project Structure

```
├── index.html                          # The entire application
├── config.json                         # Target regions configuration
├── data/
│   ├── regions.json                    # List of all Azure regions
│   ├── metadata.json                   # Last refresh timestamp
│   ├── retirements.json                # VM family retirement data
│   ├── newzealandnorth.json            # SKU data for New Zealand North
│   ├── australiaeast.json              # SKU data for Australia East
│   └── history/                        # Monthly snapshots for trends
│       └── .gitkeep
├── scripts/
│   ├── normalize-skus.py               # Raw SKU data normalizer
│   └── update-retirements.py           # Retirement data scraper
├── README.md
├── TEMPLATE-GUIDE.md
├── docs/
│   ├── SPEC.md                         # Application specification
│   ├── howitworks.md                   # Technical deep-dive
│   └── talktrack.md                    # Demo talk track
└── .github/
    ├── copilot-instructions.md         # AI assistant conventions
    ├── pull_request_template.md        # PR checklist
    └── workflows/
        ├── deploy.yml                  # Deploy to Azure on push to main
        ├── validate.yml                # HTML validation on PRs
        └── refresh-vm-skus.yml         # Monthly SKU data refresh + retirement + history
```

## 📖 Documentation

| Document | Description |
|----------|-------------|
| [SPEC.md](docs/SPEC.md) | Full application specification |
| [How It Works](docs/howitworks.md) | Technical deep-dive |
| [Talk Track](docs/talktrack.md) | Demo presentation notes |
| [Template Guide](TEMPLATE-GUIDE.md) | How to set up from this template |

## 🛠️ Development

This app follows **GitHub Flow**:

1. Create a feature branch: `git checkout -b feature/my-feature`
2. Make changes to `index.html`
3. Push and create a PR
4. Merge to `main` → auto-deploys to Azure

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

<div align="center">
  <strong>DJ Tools</strong> powered by <a href="https://github.com/features/copilot/cli/">GitHub Copilot CLI</a>
</div>
