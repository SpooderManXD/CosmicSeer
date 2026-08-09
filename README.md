# CosmoSeer

A Kardashev Scale simulator that converts planetary, stellar, and galactic energy infrastructure into raw power metrics and computes a civilization's K-score. Uses NVIDIA NIM (Llama 3.3 70B) to generate tactical advisor reports.

## Setup

```bash
pip install -r requirements.txt
```

Set your NVIDIA NIM API key:

```bash
$env:NVIDIA_API_KEY="nvapi-your-key-here"
```

## Run

```bash
streamlit run app.py
```

## Architecture

```
cosmoseer/
├── app.py              # Main entry point, wires all modules together
├── requirements.txt
└── Scripts/
    ├── logic.py        # Kardashev math engine
    ├── ai.py           # NVIDIA NIM integration
    └── ui.py           # CSS, layout components, rendering helpers
```

## How the K-score is computed

```
K = (log10(P) - 6) / 10
```

Where P is total power output in Watts across all three civilization tiers.