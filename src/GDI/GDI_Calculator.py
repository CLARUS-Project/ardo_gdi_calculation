from collections import defaultdict
import json

"""
Definition of a function to calculate the GDI
"""

import json
from collections import defaultdict

def calculate_green_deal_index(data):
    Hierarchy_level_scores = defaultdict(float)
    hierarchy_weights = data["hierarchy_weights"]

    for indicator in data["gdi_indicators"]:
        current = indicator["current_value"]
        target = indicator["target_value"]
        weight = indicator["indicator_weight"]
        level = indicator["hierarchy_level"]
        impact_type = indicator["impact_type"]

        if impact_type == "positive":
            normalized = current / target if target else 0
        elif impact_type == "negative":
            normalized = target / current if current else 0
        else:
            raise ValueError(f"Invalid impact_type: {impact_type}")

        contribution = normalized * weight
        indicator["contribution"] = contribution  # Añadir al JSON

        Hierarchy_level_scores[level] += contribution

    gdi = sum(
        Hierarchy_level_scores[level] * hierarchy_weights.get(level, 0)
        for level in Hierarchy_level_scores
    )

    data["gdi"] = gdi  # Añadir GDI al JSON principal

    return data


with open('GDI/gdi_data_mock.json', 'r') as file:
    data = json.load(file)

gdi = calculate_green_deal_index(data)
print(f"Green Deal Index: {json.dumps(gdi, indent=4)}")

# Save the updated JSON with contributions and GDI
with open('gdi_data_with_contributions.json', 'w') as file:
    json.dump(gdi, file, indent=4)