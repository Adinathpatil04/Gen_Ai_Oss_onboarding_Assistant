def estimate_difficulty(issue, related_code):
    labels = issue["labels"]

    if "good first issue" in labels or "beginner" in labels:
        return "Beginner"

    if len(related_code) <= 2:
        return "Beginner"

    if len(related_code) <= 5:
        return "Intermediate"

    return "Advanced"


def extract_skills(related_code):
    skills = set()

    for r in related_code:
        file = r["meta"]["file"]
        if "auth" in file.lower():
            skills.add("Authentication")
        if "db" in file.lower():
            skills.add("Databases")
        if "api" in file.lower():
            skills.add("API Design")

    if not skills:
        skills.add("Python")

    return list(skills)
