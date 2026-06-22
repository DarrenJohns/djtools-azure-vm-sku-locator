# How It Works — Azure VM SKU by Region

> Technical deep-dive into the application architecture and implementation.

## Architecture

This is a **single-file HTML web application** with **static JSON data files** — all HTML, CSS, and JavaScript live in one `index.html` file, and pre-fetched data is stored as JSON in the `data/` directory. There are no frameworks, no build tools, and no external dependencies.

🔗 **Live at [vmsku.djtools.co.nz](https://vmsku.djtools.co.nz)**

### Why This Approach?
- **No authentication needed**: Data is pre-fetched, so users don't need to log in
- **Zero setup**: Just visit the URL
- **No dependencies**: Nothing to install, update, or break
- **Fast**: Static JSON loads instantly, no API calls at runtime

## Data Pipeline

### Sources

| Data Set | Source | Script |
|----------|--------|--------|
| VM SKUs | Azure Resource SKU API | `scripts/normalize-skus.py` |
| Managed Disk SKUs | Azure Resource SKU API | `scripts/normalize-disks.py` |
| VM Pricing | Azure Retail Prices API (17 currencies, PAYG + RI) | `scripts/fetch-pricing.py --currency <CODE>` |
| Retirement Dates | Azure Updates page | `scripts/update-retirements.py` |

The list of regions to fetch is configured in `config.json`.

### VM SKU Normalization
Raw SKU data has capabilities buried in a `capabilities[]` array of `{name, value}` pairs. The normalize script flattens these into clean fields:

```
Raw: capabilities: [{name: "vCPUs", value: "4"}, {name: "MemoryGB", value: "16"}, ...]
Normalized: { vCPUs: 4, memoryGB: 16, ... }
```

### Key normalized VM fields
- `vCPUs`, `memoryGB`, `maxDataDisks`, `maxNICs`
- `cpuArchitecture` (x64 or Arm64)
- `acceleratedNetworking`, `premiumIO`, `ephemeralOSDisk`, `encryptionAtHost`
- `spotEligible`, `zones`, `restrictions`

### Disk SKU Normalization
Raw disk data is filtered (type-level entries removed) and normalized to include:
- `maxIOPS`, `maxThroughputMBps`, `burstIOPS`, `burstThroughputMBps`
- `maxSizeGiB`, `maxShares`, `zones`
- Tier labels: Premium SSD, Standard SSD, Standard HDD, Ultra, PremiumV2

### Processor Detection
The `getProcessorType(size)` helper parses SKU name suffixes to identify processor type:
- `a` suffix → AMD
- `p` suffix → ARM (Ampere)
- Otherwise → Intel

### History Archiving
Before each data refresh, previous data files are archived to `data/history/` with timestamps. This enables the What's New feature to compare current data against the previous month and surface added/removed SKUs.

### Schedule
Data is refreshed monthly via the `refresh-vm-skus.yml` GitHub Actions workflow on a self-hosted runner. The workflow also supports manual dispatch via the GitHub Actions UI.

## Data Loading

### Lazy Loading
The app loads region data on demand — when a user selects a region, it fetches `data/{regionName}.json` and `data/{regionName}-disks.json`. Data is cached in memory for the session.

### Startup Data
On initialization, the app loads:
- `data/regions.json` — all available Azure regions
- `data/metadata.json` — last refresh timestamp and region availability
- `data/retirements.json` — VM family retirement data

## Sections & Features

### Tab Layout
The app uses a **tabbed interface** with 6 tabs in a sticky tab strip:
1. **📊 Overview** — Summary KPI cards, What's New (month-over-month SKU changes), Workload Recommendations
2. **🔍 Browse SKUs** — Filterable SKU table with search, filters, column chooser
3. **🎯 Find a Match** — Deployment requirements checker with ranked results
4. **📌 Pinned** — Shortlist, pricing comparison, multi-region availability compare
5. **💿 Disk SKUs** — Managed disk browser with tier filters and collapsible groups
6. **📖 Reference** — VM naming convention guide, CLI guidance, deployment snippets

Tabs support keyboard shortcuts (1–6), URL hash routing, and dynamic badge counts.

### Browse SKUs (See What's Available)
- Filterable, sortable table grouped alphabetically by first letter
- Filters: text search, size, version, family type, vCPU range, processor type
- Column chooser to show/hide columns
- Click any SKU for deployment snippet modal (CLI, PowerShell, Bicep)
- Retirement badges on SKUs from families being retired

### Find a Match (Deployment Checker)
Users specify minimum requirements (vCPUs, memory, disks, NICs, processor, features) and get ranked matches with percentage scores. Results can be pinned or exported to CSV.

### Pinned Shortlist & Multi-Region Compare
- Pin SKUs from browse table or checker results
- Chips display key specs at a glance
- Compare pinned SKU availability across up to 5 additional regions
- Export pinned shortlist to CSV

### Disk SKUs
- Summary cards showing disk count by tier
- Collapsible groups by disk tier with expand/collapse all
- Filters: disk type, redundancy (LRS/ZRS), availability zones, IOPS range
- Performance details: IOPS, throughput, burst, max shares

### KPI Dashboard
Summary cards showing: Total SKUs, vCPU Range, Memory Range, Unique Families, Intel count, AMD/ARM count, plus data freshness indicator.

## Theme System

### CSS Custom Properties
```css
:root {
  --brand-primary: #0f6cbd;
  --bg-base: #fafafa;
  --text-primary: #242424;
}
```

### Dark Mode
- Toggled via header button or `T` keyboard shortcut
- System preference detected on first visit via `prefers-color-scheme`
- Preference saved to `localStorage`

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `T` | Toggle light/dark theme |
| `F` | Focus search input |
| `C` | Clear all filters |
| `X` | Export to CSV |
| `?` | Show keyboard shortcuts panel |
| `Esc` | Close modals/panels |

## Deployment

### Azure Static Web Apps
The app is hosted on Azure Static Web Apps (Free tier) with a custom domain and managed SSL.

### CI/CD Pipeline
```
Push to main → GitHub Actions → swa deploy (staging folder) → Live
```

Only web-servable files are deployed (`index.html`, `toptrumps.html`, `toptrumps-webgl.html`, `config.json`, `data/`, `vendor/`). Scripts and docs are excluded.

### Data Refresh Pipeline
```
Monthly trigger → fetch VM/disk/pricing (×17 currencies)/retirement data → swa deploy → git commit → push
```

The refresh pipeline runs on a self-hosted runner with Azure CLI access.

## Experimental WebGL Top Trumps Build

`toptrumps-webgl.html` is an experimental WebGL fork of the Top Trumps companion. It ships alongside `toptrumps.html` and is intentionally a separate file so the stable build stays at zero JS dependencies.

### Dependency
- **Three.js r170 ES module**, vendored locally at `vendor/three.module.min.js` (MIT, ~675 KB).
- Loaded via a native browser **import map** — no CDN, no build step, no npm.
  ```html
  <script type="importmap">
    { "imports": { "three": "./vendor/three.module.min.js" } }
  </script>
  <script type="module">
    import * as THREE from 'three';
    // ...
  </script>
  ```

### What WebGL adds
1. **3D globe background** — replaces the Canvas2D `GlobeBg` IIFE with a Three.js `SphereGeometry` + custom `ShaderMaterial`. Procedural dot grid via `fract(lonBand)/fract(latBand) + smoothstep`, fresnel rim via `pow(1 - dot(N, V), 2.2)`, additive halo on a `BackSide` shell. 32 Azure region nodes as pulsing `Points`. Great-circle arcs rendered as `LineBasicMaterial` with vertex-color trails fading per frame. Auto-rotates at `0.06 rad/s`.
2. **Holographic foil overlay** on rare/epic/legendary cards — per-card mini `WebGLRenderer` + `ShaderMaterial` on a `PlaneGeometry(2,2)` quad. Pointer-driven hue band (`sin(t * 14)`), rainbow shimmer (RGB sinusoids out of phase), specular hot-spot (`exp(-dist² * 16) * uHover`), edge fade. Smoothed hover transition `cur + (target - cur) * min(1, dt * 8)`. Auto-tilts via `sin(now * 0.0007) * 0.3` when idle.
3. **GPU confetti** on win — Three.js `Points` system (~1400 particles) with vertex-shader physics. Each particle has `position`, `aVelocity`, `aColor`, `aSize`, `aFlutter` (freq + phase), `aDelay`. Vertex shader integrates: `x = pos.x + vx*t + sin(t * freq + phase) * 0.04; y = pos.y + vy*t - 0.5 * gravity * t²`. Maps `0..1 → -1..1` clip space directly with an identity `THREE.Camera`. Discards via `gl_PointSize = 0` when life exceeds limit or below screen.

### Fallbacks
- If `new THREE.WebGLRenderer()` throws on load, `markFallback(reason)` is called: the BETA chip switches to "BETA · 2D fallback" and `runCanvas2DGlobe()` is invoked. Cards render without the foil overlay; confetti uses the CSS implementation.
- `prefers-reduced-motion` stops the globe RAF after one frame, skips foil RAF loops, and bypasses the confetti burst entirely.

### Global contracts preserved
- `window.globeBurst(n)` — arc cascade trigger (matches the Canvas2D API).
- `window.runCanvas2DGlobe()` — fallback init.
- `window.__attachFoilOverlay(cardEl)` — attached to `mountFlipCard`'s post-build hook.
- `window.__webglConfetti({count})` — called from `triggerVictoryFx`.

### Discovery
A small "✨ WebGL beta" chip in `toptrumps.html`'s topbar links to `toptrumps-webgl.html`; the WebGL build has a reciprocal "← Stable" chip linking back.
