KNOWN_SKILLS = [
    "Django REST Framework",
    "Python",
    "JavaScript",
    "GitHub",
    "REST API",
    "MySQL",
    "Angular",
    "React",
    "Django",
    "Flask",
    "HTML",
    "CSS",
    "SQL",
    "Git",
    "NumPy",
    "Pandas",
    "AWS",
    "Redis",
]


SKILL_ALIASES = {
    "DRF": "Django REST Framework",
    "Django Rest Framework": "Django REST Framework",
    "ReactJS": "React",
    "AngularJS": "Angular",
}


def extract_skills(text):
    text_lower = text.lower()

    found_skills = []
    matched_ranges = []

    # Check longer skills first
    skills_sorted = sorted(
        KNOWN_SKILLS,
        key=len,
        reverse=True
    )

    for skill in skills_sorted:
        skill_lower = skill.lower()
        start = 0

        while True:
            position = text_lower.find(skill_lower, start)

            if position == -1:
                break

            end = position + len(skill_lower)

            overlaps = any(
                position < existing_end
                and end > existing_start
                for existing_start, existing_end in matched_ranges
            )

            if not overlaps:
                found_skills.append(skill)
                matched_ranges.append((position, end))

            start = end

    found_skills = normalize_skills(found_skills)

    # Django is already represented by Django REST Framework
    if "Django REST Framework" in found_skills:
        found_skills = [
            skill
            for skill in found_skills
            if skill != "Django"
        ]

    return found_skills


def normalize_skills(skills):
    normalized = []

    for skill in skills:
        canonical_skill = SKILL_ALIASES.get(skill, skill)

        if canonical_skill not in normalized:
            normalized.append(canonical_skill)

    return normalized



def normalize_skills(skills):
    normalized = []

    for skill in skills:
        canonical_skill = SKILL_ALIASES.get(skill, skill)

        # If this skill is already covered by a more specific skill,
        # don't add it separately.
        if canonical_skill == "Django" and "Django REST Framework" in normalized:
            continue

        if canonical_skill not in normalized:
            normalized.append(canonical_skill)

    return normalized