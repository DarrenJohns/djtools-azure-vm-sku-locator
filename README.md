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
| **Browse** | Select up to 5 Azure regions to view available VM SKUs |
| **Search** | Filter by SKU name, family, vCPU count, CPU architecture |
| **Compare** | View SKUs across multiple regions side by side |
| **Details** | vCPUs, memory, data disks, zones, accelerated networking, Premium IO, ephemeral OS disk, Spot eligibility |
| **Docs** | Direct links to Azure VM size documentation for each SKU family |
| **Export** | Download filtered results as CSV |
| **CLI** | Guidance for real-time data via `az vm list-skus` |

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
3. **Filter** — Search by name, filter by family, architecture, or vCPU count
4. **Export** — Download filtered results as CSV
5. **Real-time data** — Use the CLI guidance section for subscription-specific availability

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
| **Data refresh** | Monthly via GitHub Actions scheduled workflow |
| **Authentication** | None required — data is pre-fetched |
| **Build step** | None — file deploys directly |
| **Hosting** | Azure Blob Storage static website |
| **CI/CD** | GitHub Actions with self-hosted runner |

## 📁 Project Structure

```
├── index.html                          # The entire application
├── data/
│   ├── regions.json                    # List of all Azure regions
│   ├── metadata.json                   # Last refresh timestamp
│   ├── newzealandnorth.json            # SKU data for New Zealand North
│   ├── australiaeast.json              # SKU data for Australia East
│   └── eastus.json                     # SKU data for East US
├── README.md                           # This file
├── TEMPLATE-GUIDE.md                   # Setup guide (delete after setup)
├── docs/
│   ├── SPEC.md                         # Application specification
│   ├── howitworks.md                   # Technical deep-dive
│   └── talktrack.md                    # Demo talk track
└── .github/
    ├── copilot-instructions.md         # AI assistant conventions
    ├── pull_request_template.md        # PR checklist
    ├── workflows/
    │   ├── deploy.yml                  # Deploy to Azure on push to main
    │   ├── validate.yml                # HTML validation on PRs
    │   └── refresh-sku-data.yml        # Monthly SKU data refresh
    └── ISSUE_TEMPLATE/
        ├── bug_report.yml
        └── feature_request.yml
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
