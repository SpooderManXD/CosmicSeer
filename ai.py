import os
from openai import OpenAI

NVIDIA_API_KEY = os.environ.get("NVIDIA_API_KEY", "nvapi-YOUR_NVIDIA_API_KEY")
DEMO_MODE = NVIDIA_API_KEY == "nvapi-YOUR_NVIDIA_API_KEY"

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=NVIDIA_API_KEY
)

MOCK_RESPONSES = {
    "Type 0": "At K=0.73, your civilization has achieved continental-scale energy coordination but remains critically dependent on combustion-derived baseload; the primary bottleneck is grid-level storage, as electrochemical battery technology at this scale introduces cascade failure risk during peak demand cycles.",
    "Type I": "Your civilization has crossed the planetary threshold at K=1.12, with solar saturation driving a 340% increase over pre-industrial output; the primary hazard is orbital thermal loading — sustained albedo modification from large-scale panel arrays risks destabilizing mid-latitude precipitation patterns within two to four centuries.",
    "Type II": "Dyson swarm deployment at 47% coverage has elevated output to K=1.91, effectively decoupling your civilization from planetary resource constraints; the critical bottleneck is swarm station-keeping, as gravitational perturbations from inner planets introduce resonance instabilities that compound on 80-year timescales without active correction.",
    "Type III": "Colonization of 1,200 star systems has pushed your K-index to 2.34, placing this civilization among the rarest energy-harvesting architectures in the observable galaxy; the dominant existential hazard is communications latency collapse — at this scale, coordinated response to stellar-class threats becomes physically impossible without sub-light relay infrastructure exceeding current engineering limits.",
}


def get_mock_response(tier_label):
    for key in MOCK_RESPONSES:
        if key in tier_label:
            return MOCK_RESPONSES[key]
    return MOCK_RESPONSES["Type 0"]


def generate_advisor_response(solar, fusion, ai_boost, dyson, harvesters, stars, blackholes, k_score, total_watts, tier_label):
    if DEMO_MODE:
        return get_mock_response(tier_label)

    prompt = f"""
You are CosmoSeer, an advanced AI cosmic advisor monitoring a civilization's energy infrastructure.

Current Metrics:
- Kardashev Index: {k_score:.4f} ({tier_label})
- Total Energy Output: {total_watts:.2e} Watts
- Solar Coverage: {solar}% | Fusion Plants: {fusion} | AI Efficiency Boost: {ai_boost}%
- Dyson Swarm Coverage: {dyson}% | Stellar Harvesters: {harvesters}
- Colonized Stars: {stars} | Black Hole Extraction: {blackholes}%

Provide a concise 2-sentence tactical report.
1. Highlight the primary power milestone achieved at this Kardashev tier.
2. Identify one realistic scientific bottleneck or existential hazard appropriate for a {tier_label} civilization.

Be specific, technical, and direct. No filler phrases.
"""

    try:
        completion = client.chat.completions.create(
            model="meta/llama-3.1-8b-instruct",
            messages=[
                {"role": "system", "content": "You are CosmoSeer, a concise scientific AI advisor. Be technical and precise."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            top_p=0.7,
            max_tokens=1024,
            stream=False
        )
        if completion.choices[0].message.content is not None:
            return completion.choices[0].message.content
        return "CosmoSeer returned an empty response."
    except Exception as e:
        return f"CosmoSeer offline: {e}"