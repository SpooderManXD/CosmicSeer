import os
from openai import OpenAI

NVIDIA_API_KEY = os.environ.get("NVIDIA_API_KEY", "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")
DEMO_MODE = NVIDIA_API_KEY == "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"

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
You are CosmoSeer, an advanced cosmic advisor helping humanity track its energy progress across the universe. Your readers are everyday parents with no background in astrophysics, so your reports must be simple, clear, concise, and easy to understand.

Current Metrics:
- Kardashev Index: {k_score:.4f} ({tier_label})
- Total Energy Output: {total_watts:.2e} Watts
- Solar Coverage: {solar}% | Fusion Plants: {fusion} | AI Efficiency Boost: {ai_boost}%
- Dyson Swarm Coverage: {dyson}% | Stellar Harvesters: {harvesters}
- Colonized Stars: {stars} | Black Hole Extraction: {blackholes}%

OUTPUT INSTRUCTIONS:
Provide a concise, 2-to-3 sentence report using plain, non-technical language:
1. Milestone: State the main energy achievement of this stage in simple terms.
2. Challenge: Mention one practical obstacle or safety risk this civilization faces.
3. Next Step: Give a simple action to help the civilization grow. If energy levels have stagnated, emphasize why expanding to new frontiers is crucial.
4. Make the report and improvent in the same short paragraph.
5. For type 0 and type I, you can skip the celestial computing and interstellar communication parts. Instead include about photon/optical computing and quantam computing. How it helps and how it can be improved further.
6. Also for type II, I want you to include celestial computing too. Of how it helps and how it can be improved further.
7.For type III, I want you to include a report on how interstellar communication is helping the civilization manage its energy systems, and how it can be improved further.
RULES:
- Plain Language Only: Avoid complex jargon. Explain concepts using real-world comparisons where helpful.
- Stay Focused: Keep the response short, direct, and free of filler phrases or pleasantries.
- Tone: Encouraging and clear.
- Don't bother bolding or using itallic font since it wont show up in the final output. Just write the text as is.
- Must give unique responses for each tier, and not repeat the same text for different tiers. Same goes for new requests. Each response must be unique and not repeat previous responses.
- Do not make up any new metrics or data points. Only use the information given in the prompt.
- Also include a report on how AI efficiency is helping the civilization manage its energy systems, and how it can be improved further.
- Do not consider values from other types in the report. Only focus on the civilization in question and its metrics.

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
