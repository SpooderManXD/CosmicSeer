import os
import concurrent.futures
from openai import OpenAI

NVIDIA_API_KEY = os.environ.get("NVIDIA_API_KEY", "")

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=NVIDIA_API_KEY
)

def _fetch_completion(prompt):
    completion = client.chat.completions.create(
        model="meta/llama-3.2-3b-instruct",
        messages=[
            {"role": "system", "content": "You are CosmoSeer, a concise scientific AI advisor. Be technical and precise."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=150
    )
    return completion.choices[0].message.content

def generate_advisor_response(solar, fusion, ai_boost, dyson, harvesters, stars, blackholes, k_score, total_watts, tier_label):
    prompt = f"""
You are CosmoSeer, an advanced AI cosmic advisor monitoring a civilization's energy infrastructure and development.

Current Metrics:
- Kardashev Index: {k_score:.4f} ({tier_label})
- Total Energy Output: {total_watts:.2e} Watts
- Solar Coverage: {solar}% | Fusion Plants: {fusion} | AI Efficiency Boost: {ai_boost}%
- Dyson Swarm Coverage: {dyson}% | Stellar Harvesters: {harvesters}
- Colonized Stars: {stars} | Black Hole Extraction: {blackholes}%

Provide a concise 2-sentence tactical report.
1. Highlight the primary power milestone achieved at this Kardashev tier.
2. Identify one realistic scientific bottleneck or existential hazard appropriate for a {tier_label} civilization.
3. Suggest one actionable recommendation to mitigate the identified risk.
4. Remember most people do not understand advanced astrophysics, so keep the explanation clear and accessible.

Be specific, simple, and direct. No filler phrases.
"""

    # Force a hard 5-second execution limit using Python threads
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(_fetch_completion, prompt)
        try:
            return future.result(timeout=5.0)  # Kills waiting after exactly 5.0s
        except concurrent.futures.TimeoutError:
            return "CosmoSeer offline: NVIDIA API server queue timed out (5s limit)."
        except Exception as e:
            return f"CosmoSeer offline: {e}"