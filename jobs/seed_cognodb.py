from .neo4j_db import get_driver, COGNODB_DATABASE


JOBS = [

    # ========================================================
    # PYTHON / DJANGO
    # ========================================================

    {
        "company": "Infosys",
        "job": "Python Developer",
        "application_url": "https://www.infosys.com/careers/apply.html",
        "skills": ["python", "django", "sql", "git", "rest api"],
    },

    {
        "company": "TCS",
        "job": "Python Developer",
        "application_url": "https://www.tcs.com/careers/india",
        "skills": ["python", "django", "sql", "git", "rest api"],
    },

    {
        "company": "Tech Solutions",
        "job": "Django Developer",
        "application_url": None,
        "skills": ["python", "django", "sql", "git", "rest api"],
    },

    {
        "company": "Backend Technologies",
        "job": "Backend Developer",
        "application_url": None,
        "skills": ["python", "django", "sql", "git", "rest api"],
    },

    {
        "company": "Python Labs",
        "job": "Junior Python Developer",
        "application_url": None,
        "skills": ["python", "git", "sql", "rest api"],
    },

    # ========================================================
    # FULL STACK
    # ========================================================

    {
        "company": "Digital Systems",
        "job": "Full Stack Developer",
        "application_url": None,
        "skills": [
            "python",
            "django",
            "sql",
            "git",
            "rest api",
            "javascript",
            "react",
            "html",
            "css",
        ],
    },

    {
        "company": "Web Technologies",
        "job": "Junior Full Stack Developer",
        "application_url": None,
        "skills": [
            "python",
            "javascript",
            "react",
            "html",
            "css",
            "git",
            "rest api",
        ],
    },

    {
        "company": "Software Systems",
        "job": "Software Developer",
        "application_url": None,
        "skills": [
            "python",
            "sql",
            "git",
            "rest api",
            "javascript",
        ],
    },

    {
        "company": "Enterprise Apps",
        "job": "Software Engineer",
        "application_url": None,
        "skills": [
            "python",
            "sql",
            "git",
            "javascript",
            "rest api",
        ],
    },

    # ========================================================
    # REACT / FRONTEND
    # ========================================================

    {
        "company": "Frontend Labs",
        "job": "React Developer",
        "application_url": None,
        "skills": [
            "git",
            "rest api",
            "javascript",
            "react",
            "html",
            "css",
        ],
    },

    {
        "company": "UI Technologies",
        "job": "Frontend Developer",
        "application_url": None,
        "skills": [
            "javascript",
            "react",
            "html",
            "css",
            "git",
        ],
    },

    {
        "company": "Modern Web",
        "job": "Web Developer",
        "application_url": None,
        "skills": [
            "javascript",
            "html",
            "css",
            "react",
            "git",
        ],
    },

    {
        "company": "JavaScript Labs",
        "job": "JavaScript Developer",
        "application_url": None,
        "skills": [
            "javascript",
            "html",
            "css",
            "react",
            "git",
        ],
    },

    # ========================================================
    # API / NODE
    # ========================================================

    {
        "company": "API Systems",
        "job": "API Developer",
        "application_url": None,
        "skills": [
            "python",
            "rest api",
            "sql",
            "git",
        ],
    },

    {
        "company": "Cloud Applications",
        "job": "Node.js Developer",
        "application_url": None,
        "skills": [
            "javascript",
            "node.js",
            "rest api",
            "sql",
            "git",
        ],
    },

    # ========================================================
    # DATA / SQL
    # ========================================================

    {
        "company": "Data Systems",
        "job": "SQL Developer",
        "application_url": None,
        "skills": [
            "sql",
            "python",
            "git",
        ],
    },

    {
        "company": "Analytics Technologies",
        "job": "Data Analyst",
        "application_url": None,
        "skills": [
            "python",
            "sql",
            "excel",
        ],
    },

    # ========================================================
    # QA
    # ========================================================

    {
        "company": "Quality Systems",
        "job": "QA Automation Engineer",
        "application_url": None,
        "skills": [
            "python",
            "selenium",
            "sql",
            "git",
        ],
    },

    # ========================================================
    # SUPPORT
    # ========================================================

    {
        "company": "IT Services",
        "job": "Technical Support Engineer",
        "application_url": None,
        "skills": [
            "python",
            "sql",
            "git",
        ],
    },

    {
        "company": "Enterprise Support",
        "job": "Application Support Engineer",
        "application_url": None,
        "skills": [
            "sql",
            "python",
            "rest api",
            "git",
        ],
    },

    {
        "company": "IT Operations",
        "job": "Service Desk Analyst",
        "application_url": None,
        "skills": [
            "sql",
            "git",
        ],
    },
]


# ============================================================
# SEED JOBS
# ============================================================

def seed_jobs():

    driver = get_driver()

    query = """
    MERGE (c:Company {name: $company})

    MERGE (j:Job {title: $job})

    MERGE (c)-[offers:OFFERS]->(j)

    SET offers.application_url = $application_url

    WITH j

    UNWIND $skills AS skill_name

    MERGE (s:Skill {name: skill_name})

    MERGE (j)-[:REQUIRES]->(s)

    RETURN
        j.title AS job,
        count(s) AS skill_count
    """

    try:

        with driver.session(
            database=COGNODB_DATABASE
        ) as session:

            for item in JOBS:

                result = session.run(
                    query,
                    company=item["company"],
                    job=item["job"],
                    application_url=item["application_url"],
                    skills=item["skills"],
                )

                record = result.single()

                print(
                    f"Seeded: {item['company']} - "
                    f"{item['job']} "
                    f"({record['skill_count']} skills)"
                )

    finally:

        driver.close()


# ============================================================
# SKILL RELATIONSHIPS
# ============================================================
def seed_skill_relationships():

    driver = get_driver()

    query = """
    UNWIND [
        ["Django REST Framework", "django"],
        ["MySQL", "sql"],
        ["GitHub", "git"],
        ["REST API", "rest api"],
        ["Python", "python"],
        ["Django", "django"],
        ["SQL", "sql"],
        ["Git", "git"],
        ["JavaScript", "javascript"],
        ["React", "react"],
        ["HTML", "html"],
        ["CSS", "css"],
        ["Node.js", "javascript"]
    ] AS relation

    MATCH (skill1:Skill)
    WHERE toLower(trim(skill1.name))
        = toLower(trim(relation[0]))

    MATCH (skill2:Skill)
    WHERE toLower(trim(skill2.name))
        = toLower(trim(relation[1]))

    WITH skill1, skill2

    WHERE toLower(trim(skill1.name))
        <> toLower(trim(skill2.name))

    MERGE (skill1)-[:RELATED_TO]->(skill2)

    RETURN
        skill1.name AS skill,
        skill2.name AS related_skill
    """

    try:

        with driver.session(
            database=COGNODB_DATABASE
        ) as session:

            result = session.run(query)

            for record in result:

                print(
                    "Relationship:",
                    record["skill"],
                    "->",
                    record["related_skill"]
                )

    finally:

        driver.close()

        
# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("SEEDING COGNODB")
    print("=" * 60)

    seed_jobs()

    print()

    seed_skill_relationships()

    print()

    print("=" * 60)
    print("COGNODB SEED COMPLETE")
    print("=" * 60)