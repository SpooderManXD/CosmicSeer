import os
from openai import OpenAI

NVIDIA_API_KEY = os.environ.get("NVIDIA_API_KEY", "nvapi-YOUR_NVIDIA_API_KEY")

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=NVIDIA_API_KEY
)

def generate_advisor_response(solar, fusion, ai_boost, dyson, harvesters, stars, blackholes, k_score, total_watts):
    if k_score < 1.0:
        tier_label = "Type 0 (Sub-Planetary)"
    elif k_score < 2.0:
        tier_label = "Type I (Planetary)"
    elif k_score < 3.0:
        tier_label = "Type II (Stellar)"
    else:
        tier_label = "Type III (Galactic)"

    prompt = f"""
    You are CosmoSeer, an advanced AI cosmic advisor monitoring a civilization.

    Current Metrics:
    - Kardashev Index: {k_score:.4f} ({tier_label})
    - Total Energy Output: {total_watts:.2e} Watts
    - Solar Coverage: {solar}% | Fusion Output: {fusion} GW | AI Boost: {ai_boost}%
    - Dyson Swarm: {dyson}% | Stellar Harvesters: {harvesters}
    - Colonized Stars: {stars} | Black Hole Tapping: {blackholes}%

    Task:
    Provide a concise 2-sentence tactical report in a scientific advisor tone.
    1. Highlight the primary power milestone achieved.
    2. Identify one realistic scientific bottleneck or hazard suitable for a {tier_label} civilization.
    """

    try:
        completion = client.chat.completions.create(
            model="meta/llama-3.3-70b-instruct",
            messages=[
                {"role": "system", "content": "You are CosmoSeer, a concise scientific AI advisor."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=150
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"CosmoSeer API Error: {e}"