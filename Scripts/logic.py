import math

def calculate_kardashev(
    solar_coverage, fusion_plants, ai_boost,
    dyson_coverage, stellar_harvesters,
    colonized_stars, blackhole_harvesters
):
    # Type I: Planetary
    baseline_watts = 1.8e13
    solar_watts = solar_coverage * 1e14
    fusion_watts = fusion_plants * 1e9
    type_1_total = (baseline_watts + solar_watts + fusion_watts) * (1 + (ai_boost / 100.0))

    # Type II: Stellar
    dyson_watts = (dyson_coverage / 100.0) * 3.86e26
    stellar_watts = stellar_harvesters * 1e24
    type_2_total = dyson_watts + stellar_watts

    # Type III: Galactic
    galactic_star_watts = colonized_stars * 1e26
    blackhole_watts = (blackhole_harvesters / 100.0) * 1e36
    type_3_total = galactic_star_watts + blackhole_watts

    total_watts = type_1_total + type_2_total + type_3_total
    k_score = (math.log10(total_watts) - 6) / 10 if total_watts > 0 else 0.0

    return total_watts, k_score