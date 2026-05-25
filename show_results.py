import json

with open("targets.json") as f:
    data = json.load(f)

profs = data["professors"]
print(f"Total: {len(profs)} professors discovered\n")
print(f"{'#':<3} {'Name':<28} {'University':<32} {'Country':<14} {'Score':>6} {'h-idx':>6}")
print("-" * 95)
for i, p in enumerate(profs, 1):
    name = p.get("name", "?")
    uni = p.get("university", "?")[:31]
    country = p.get("country", "?")
    score = p.get("match_score", p.get("relevance_score", 0))
    hidx = p.get("h_index", p.get("hIndex", 0))
    email = p.get("email", "[FILL IN]")
    has_email = "✓" if email and "[FILL" not in email else "✗"
    print(f"{i:<3} {name:<28} {uni:<32} {country:<14} {score:>6} {hidx:>6}  email:{has_email}")
