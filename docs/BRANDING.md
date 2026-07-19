# LedgerLens brand system

## Brand idea

The mark combines a layered ledger, an integrated `L`, and a focus lens. The repeated page-edge
rhythm represents multiple records and broker sources converging into a clear view. The product
line is: **Many sources. One verified view.**

## Palette

| Token | Hex | Use |
| --- | --- | --- |
| App background | `#08111F` | Main dashboard canvas |
| Icon surface | `#0B1729` | Icon tile and avatar |
| Primary blue | `#4F8CFF` | Primary action and portfolio information |
| Consolidation teal | `#2DD4BF` | Verified and consolidated information |
| Supporting lavender | `#9B87F5` | Source diversity and secondary identity accent |
| Primary text | `#F8FAFC` | Dark-background wordmark and text |

Performance green is excluded from the mark and reserved for positive financial movement.

## Product integration

- `ledgerlens-app-icon-192.png` is loaded through Pillow before Streamlit page configuration.
- `ledgerlens-header-lockup.png` is embedded locally in the application header; accessible
  `LedgerLens` alternative text and a text fallback are retained.
- The README switches between the light and dark lockups according to the viewer's color scheme.
- The Project view uses the lockup with the product story, workflow, safeguards, responsibility
  boundary, limits, disclaimer, and public artifact links.
- No brand asset requires an external request at runtime.

The curated files and usage rules are listed in [`assets/branding/README.md`](../assets/branding/README.md).
