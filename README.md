# CosmoSeer

> A Kardashev Scale simulator that converts civilization-scale energy infrastructure into raw power metrics and an indexed K-score, powered by NVIDIA NIM and Streamlit.

---

## What it does

CosmoSeer models energy output across three civilization tiers — planetary, stellar, and galactic — using physically grounded inputs. It computes a continuous Kardashev Index (K-score) from total wattage and generates a tactical advisory report via a large language model tuned to the civilization's current tier.

**K-score formula:**

```
K = (log10(P) − 6) / 10
```

Where `P` is total power output in Watts.

| K-score range | Classification        |
|:--------------|:----------------------|
| < 1.0         | Type 0 — Sub-Planetary |
| 1.0 – 2.0     | Type I — Planetary     |
| 2.0 – 3.0     | Type II — Stellar      |
| ≥ 3.0         | Type III — Galactic    |

---

## Architecture

```
cosmoseer/
├── app.py              # Entry point — wires all modules, manages session state
├── requirements.txt
└── Scripts/
    ├── logic.py        # Kardashev math engine
    ├── ai.py           # NVIDIA NIM integration (Llama 3.3 70B)
    └── ui.py           # CSS, layout components, rendering helpers
```

**Data flow:**

```
User inputs (sliders)
    └──▶  logic.py  →  (total_watts, k_score)
               └──▶  ai.py  →  advisory report (NVIDIA NIM)
                         └──▶  ui.py  →  rendered Streamlit output
```

---

## Energy model

### Type I — Planetary

| Input             | Contribution                   |
|:------------------|:-------------------------------|
| Baseline output   | 1.8 × 10¹³ W (fixed)           |
| Solar coverage    | up to 1 × 10¹⁴ W (per unit)   |
| Fusion plants     | 1 × 10⁹ W per plant            |
| AI optimization   | multiplicative boost (%)        |

### Type II — Stellar

| Input                | Contribution                     |
|:---------------------|:---------------------------------|
| Dyson swarm coverage | up to 3.86 × 10²⁶ W (100%)      |
| Stellar harvesters   | 1 × 10²⁴ W each                 |

### Type III — Galactic

| Input                | Contribution                     |
|:---------------------|:---------------------------------|
| Colonized stars      | 1 × 10²⁶ W per star             |
| Black hole tapping   | up to 1 × 10³⁶ W (100%)         |

---

## Setup

**Requirements:** Python 3.9+

```bash
pip install -r requirements.txt
```

**Set your NVIDIA NIM API key** (PowerShell):

```powershell
$env:NVIDIA_API_KEY = "nvapi-your-key-here"
```

The key must be set in the same terminal session used to run the app.

**Run:**

```bash
streamlit run app.py
```

---

## NVIDIA NIM integration

CosmoSeer calls `meta/llama-3.3-70b-instruct` via the NVIDIA NIM API endpoint at `https://integrate.api.nvidia.com/v1`. The model generates a two-sentence tactical advisory report scoped to the civilization's current K-tier.

**Required parameters** (deviating from these causes silent hangs):

```python
model="meta/llama-3.3-70b-instruct"
temperature=0.7
max_tokens=150
```

**Demo mode:** If `NVIDIA_API_KEY` equals the placeholder string `"nvapi-YOUR_NVIDIA_API_KEY"`, `ai.py` returns a pre-written tier-matched response without making any API call. Useful for UI development and testing without a key.

---

## Session state

Advisor responses are stored in `st.session_state["advisor_response"]` and rendered with a standalone `if` block — not chained as `elif` — to avoid a display bug where the response disappears after the button interaction resolves.

---

## Notes

- Setting AI boost to 0% disables the multiplicative amplifier on Type I output.
- Black hole tapping is the dominant term at high percentages — it overshadows all other contributions combined.
- The app uses `st.components.v1.html` for the animated canvas orb on the advisor page; `st.markdown` sandboxes JavaScript and cannot run it.

---

## License

MIT