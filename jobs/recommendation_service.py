from collections import Counter

from .neo4j_db import get_driver, COGNODB_DATABASE


RELATED_WEIGHT = 0.5


def normalize_skill(skill):
    """Normalize a skill for comparison."""
    if not skill:
        return ""

    return " ".join(
        str(skill).strip().lower().split()
    )


def get_job_recommendations(candidate_name):

    driver = get_driver()

    query = """
    MATCH (c:Candidate {name: $candidate_name})
          -[:HAS_SKILL]->(cs:Skill)

    WITH
        c,
        collect(DISTINCT cs) AS candidate_skill_nodes

    WITH
        c,
        candidate_skill_nodes,
        [s IN candidate_skill_nodes |
            toLower(trim(s.name))
        ] AS candidate_skills

    MATCH (company:Company)
          -[offers:OFFERS]->(j:Job)

    OPTIONAL MATCH (j)-[:REQUIRES]->(required:Skill)

    WITH
        company,
        offers,
        j,
        candidate_skills,
        collect(DISTINCT required) AS required_nodes

    WITH
        company,
        offers,
        j,
        candidate_skills,

        [
            skill IN required_nodes
            WHERE skill IS NOT NULL |
            toLower(trim(skill.name))
        ] AS required_skills

    RETURN
        company.name AS company,
        offers.application_url AS application_url,
        j.title AS job,
        candidate_skills,
        required_skills
    """

    try:

        with driver.session(
            database=COGNODB_DATABASE
        ) as session:

            result = session.run(
                query,
                candidate_name=candidate_name
            )

            recommendations = []

            for record in result:

                company = record["company"]
                application_url = record["application_url"]
                job_title = record["job"]

                candidate_skills = set(
                    normalize_skill(skill)
                    for skill in record["candidate_skills"]
                    if normalize_skill(skill)
                )

                required_skills = list(
                    dict.fromkeys(
                        normalize_skill(skill)
                        for skill in record["required_skills"]
                        if normalize_skill(skill)
                    )
                )

                matched_skills = []
                related_skills = []
                missing_skills = []

                # ==================================================
                # CHECK EACH REQUIRED SKILL
                # ==================================================

                for required_skill in required_skills:

                    # ------------------------------------------------
                    # EXACT MATCH
                    # ------------------------------------------------

                    if required_skill in candidate_skills:

                        matched_skills.append(
                            required_skill
                        )

                        continue

                    # ------------------------------------------------
                    # RELATED MATCH
                    # ------------------------------------------------

                    related_query = """
                    MATCH (candidate_skill:Skill)
                    MATCH (required_skill:Skill)

                    WHERE
                        toLower(trim(candidate_skill.name))
                            IN $candidate_skills

                    AND
                        toLower(trim(required_skill.name))
                            = $required_skill

                    MATCH (candidate_skill)-[:RELATED_TO]-
                          (required_skill)

                    RETURN DISTINCT
                        candidate_skill.name AS candidate_skill

                    LIMIT 1
                    """

                    related_result = session.run(
                        related_query,
                        candidate_skills=list(
                            candidate_skills
                        ),
                        required_skill=required_skill
                    )

                    related_record = (
                        related_result.single()
                    )

                    if related_record:

                        related_skills.append(
                            required_skill
                        )

                    else:

                        missing_skills.append(
                            required_skill
                        )

                # ==================================================
                # SCORE
                # ==================================================

                total_required = len(
                    required_skills
                )

                exact_count = len(
                    matched_skills
                )

                related_count = len(
                    related_skills
                )

                if total_required == 0:

                    match_percentage = 0.0

                else:

                    weighted_score = (
                        exact_count
                        +
                        (
                            related_count
                            * RELATED_WEIGHT
                        )
                    )

                    match_percentage = round(
                        (
                            weighted_score
                            /
                            total_required
                        )
                        * 100,
                        2
                    )

                # ==================================================
                # SKILL GAP
                # ==================================================

                skill_gap = list(
                    dict.fromkeys(
                        missing_skills
                        +
                        related_skills
                    )
                )

                # ==================================================
                # WHY THIS JOB
                # ==================================================

                why_this_job = []

                if exact_count:

                    why_this_job.append(
                        f"{exact_count} of "
                        f"{total_required} required "
                        f"skills matched exactly"
                    )

                if related_count:

                    why_this_job.append(
                        f"{related_count} related "
                        f"skill"
                        f"{'s' if related_count != 1 else ''} "
                        f"found"
                    )

                if not skill_gap:

                    why_this_job.append(
                        "No skill gaps detected"
                    )

                else:

                    why_this_job.append(
                        "Improve: "
                        +
                        ", ".join(skill_gap)
                    )

                why_this_job.append(
                    f"{match_percentage}% "
                    f"overall match"
                )

                # ==================================================
                # RESULT
                # ==================================================

                recommendations.append({

                    "company":
                        company,

                    "job":
                        job_title,

                    "application_url":
                        application_url,

                    "required_skills":
                        required_skills,

                    "matched_skills":
                        matched_skills,

                    "related_skills":
                        related_skills,

                    "missing_skills":
                        missing_skills,

                    "skill_gap":
                        skill_gap,

                    "match_percentage":
                        match_percentage,

                    "why_this_job":
                        why_this_job
                })

            # ======================================================
            # SORT
            # ======================================================

            recommendations.sort(
                key=lambda item: (
                    item["match_percentage"],
                    len(item["matched_skills"]),
                    -len(item["skill_gap"])
                ),
                reverse=True
            )

            # ======================================================
            # GLOBAL SKILLS TO LEARN
            # ======================================================

            skill_counter = Counter()

            for job in recommendations:

                for skill in job["skill_gap"]:

                    skill_counter[skill] += 1

            skills_to_learn = []

            for skill, job_count in (
                skill_counter.most_common()
            ):

                skills_to_learn.append({

                    "skill":
                        skill,

                    "job_count":
                        job_count
                })

            return {

                "recommendations":
                    recommendations,

                "skills_to_learn":
                    skills_to_learn
            }

    finally:

        driver.close()