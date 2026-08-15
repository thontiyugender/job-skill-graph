from .neo4j_db import (
    get_driver,
    COGNODB_DATABASE,
)


def match_candidate_with_job(
    job_title,
    candidate_skills
):
    driver = get_driver()

    query = """
    MATCH (j:Job)

    WHERE toLower(j.title) =
          toLower($job_title)

    OPTIONAL MATCH
        (j)-[:REQUIRES]->(s:Skill)

    WITH
        j,
        collect(
            DISTINCT toLower(trim(s.name))
        ) AS required_skills

    WITH
        j,
        required_skills,

        [
            skill IN $candidate_skills
            WHERE toLower(trim(skill))
                  IN required_skills
        ] AS matched_skills

    WITH
        j,
        required_skills,
        matched_skills,

        [
            skill IN required_skills
            WHERE NOT skill IN
                [
                    x IN matched_skills |
                    toLower(trim(x))
                ]
        ] AS missing_skills

    RETURN
        j.title AS job,
        required_skills,
        matched_skills,
        missing_skills
    """

    try:

        with driver.session(
            database=COGNODB_DATABASE
        ) as session:

            result = session.run(
                query,
                job_title=job_title,
                candidate_skills=candidate_skills,
            )

            record = result.single()

            if not record:
                return None

            data = record.data()

            required = data[
                "required_skills"
            ]

            matched = data[
                "matched_skills"
            ]

            # =================================================
            # MATCH PERCENTAGE
            # =================================================

            match_percentage = (

                round(
                    (
                        len(matched)
                        / len(required)
                    ) * 100,
                    2
                )

                if required

                else 0.0
            )

            data[
                "match_percentage"
            ] = match_percentage

            return data

    finally:

        driver.close()