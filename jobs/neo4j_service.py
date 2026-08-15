from .neo4j_db import get_driver, COGNODB_DATABASE
from .neo4j_db import get_driver, COGNODB_DATABASE


# ============================================================
# CREATE JOB
# ============================================================

def create_job_graph(
    company_name,
    job_title,
    skills,
    application_url=None
):
    driver = get_driver()

    query = """
    MERGE (c:Company {name: $company_name})

    MERGE (j:Job {title: $job_title})

    MERGE (c)-[offers:OFFERS]->(j)

    SET offers.application_url = $application_url

    WITH c, j

    UNWIND $skills AS skill_name

    MERGE (s:Skill {name: skill_name})

    MERGE (j)-[:REQUIRES]->(s)

    WITH c, j, collect(DISTINCT s.name) AS skill_names

    MATCH (c)-[offers:OFFERS]->(j)

    RETURN
        c.name AS company,
        j.title AS job,
        offers.application_url AS application_url,
        skill_names AS skills
    """

    try:
        with driver.session(
            database=COGNODB_DATABASE
        ) as session:

            result = session.run(
                query,
                company_name=company_name,
                job_title=job_title,
                skills=skills,
                application_url=application_url
            )

            return result.single()

    finally:
        driver.close()


# ============================================================
# GET ALL JOBS
# ============================================================

def get_all_jobs():
    driver = get_driver()

    query = """
    MATCH (c:Company)-[offers:OFFERS]->(j:Job)

    OPTIONAL MATCH (j)-[:REQUIRES]->(s:Skill)

    RETURN
        c.name AS company,
        j.title AS job,
        offers.application_url AS application_url,
        collect(DISTINCT s.name) AS skills

    ORDER BY company, job
    """

    try:
        with driver.session(
            database=COGNODB_DATABASE
        ) as session:

            result = session.run(query)

            return [
                record.data()
                for record in result
            ]

    finally:
        driver.close()


# ============================================================
# GET JOBS BY SKILL
# ============================================================

def get_jobs_by_skill(skill_name):
    driver = get_driver()

    query = """
    MATCH
        (c:Company)-[offers:OFFERS]->(j:Job)
        -[:REQUIRES]->(s:Skill)

    WHERE toLower(s.name) =
          toLower($skill_name)

    RETURN
        c.name AS company,
        j.title AS job,
        offers.application_url AS application_url

    ORDER BY company, job
    """

    try:
        with driver.session(
            database=COGNODB_DATABASE
        ) as session:

            result = session.run(
                query,
                skill_name=skill_name
            )

            return [
                record.data()
                for record in result
            ]

    finally:
        driver.close()


# ============================================================
# GET JOB DETAILS
# ============================================================

def get_job_details(job_title):
    driver = get_driver()

    query = """
    MATCH
        (c:Company)-[offers:OFFERS]->(j:Job)

    WHERE toLower(j.title) =
          toLower($job_title)

    OPTIONAL MATCH
        (j)-[:REQUIRES]->(s:Skill)

    RETURN
        j.title AS job,

        collect(
            DISTINCT {
                company: c.name,
                application_url:
                    offers.application_url
            }
        ) AS company_details,

        collect(DISTINCT s.name) AS skills
    """

    try:
        with driver.session(
            database=COGNODB_DATABASE
        ) as session:

            result = session.run(
                query,
                job_title=job_title
            )

            record = result.single()

            if record:
                return record.data()

            return None

    finally:
        driver.close()


# ============================================================
# CREATE CANDIDATE GRAPH
# ============================================================
# ============================================================
# CREATE CANDIDATE GRAPH
# ============================================================

def create_candidate_graph(candidate_name, skills):

    driver = get_driver()

    try:

        with driver.session(database=COGNODB_DATABASE) as session:

            # ------------------------------------------------
            # STEP 1: CREATE / FIND CANDIDATE
            # ------------------------------------------------

            session.run(
                """
                MERGE (c:Candidate {name: $candidate_name})
                """,
                candidate_name=candidate_name
            )

            # ------------------------------------------------
            # STEP 2: REMOVE OLD SKILLS
            # ------------------------------------------------

            session.run(
                """
                MATCH (c:Candidate {name: $candidate_name})
                OPTIONAL MATCH
                    (c)-[r:HAS_SKILL]->(:Skill)
                DELETE r
                """,
                candidate_name=candidate_name
            )

            # ------------------------------------------------
            # STEP 3: ADD CURRENT RESUME SKILLS
            # ------------------------------------------------

            session.run(
                """
                MATCH (c:Candidate {name: $candidate_name})

                UNWIND $skills AS skill_name

                MERGE (s:Skill {name: skill_name})

                MERGE (c)-[:HAS_SKILL]->(s)
                """,
                candidate_name=candidate_name,
                skills=skills
            )

            # ------------------------------------------------
            # STEP 4: READ CANDIDATE GRAPH
            # ------------------------------------------------

            result = session.run(
                """
                MATCH (c:Candidate {name: $candidate_name})

                OPTIONAL MATCH
                    (c)-[:HAS_SKILL]->(s:Skill)

                RETURN
                    c.name AS candidate,
                    collect(DISTINCT s.name) AS skills
                """,
                candidate_name=candidate_name
            )

            record = result.single()

            if not record:

                return {
                    "candidate": candidate_name,
                    "skills": list(
                        dict.fromkeys(skills)
                    )
                }

            return {
                "candidate": record["candidate"],
                "skills": record["skills"]
            }

    finally:

        driver.close()


# ============================================================
# CREATE SKILL RELATIONSHIPS
# ============================================================

def create_skill_relationships():
    driver = get_driver()

    query = """
    UNWIND [
        ["Django REST Framework", "Django"],
        ["MySQL", "SQL"],
        ["GitHub", "Git"]
    ] AS relation

    MATCH
        (skill1:Skill {name: relation[0]})

    MATCH
        (skill2:Skill {name: relation[1]})

    MERGE
        (skill1)-[:RELATED_TO]->(skill2)

    RETURN
        skill1.name AS skill,
        skill2.name AS related_skill
    """

    try:
        with driver.session(
            database=COGNODB_DATABASE
        ) as session:

            result = session.run(query)

            return [
                record.data()
                for record in result
            ]

    finally:
        driver.close()



