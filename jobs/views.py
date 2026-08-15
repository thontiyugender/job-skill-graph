from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


from .neo4j_service import (
    create_job_graph,
    get_all_jobs,
    get_jobs_by_skill,
    get_job_details,
    create_candidate_graph,
)

from .matching_service import match_candidate_with_job
from .resume_service import (
    extract_resume_text,
    extract_candidate_name,
)
from .skill_extractor import extract_skills
from .recommendation_service import get_job_recommendations


# ============================================================
# HEALTH CHECK
# ============================================================

@api_view(["GET"])
def health_check(request):

    return Response({
        "status": "success",
        "message": "Job Skill Graph API is working"
    })


# ============================================================
# CREATE JOB
# ============================================================

@api_view(["POST"])
def create_job(request):

    company = request.data.get("company")
    job_title = request.data.get("job_title")
    skills = request.data.get("skills")
    application_url = request.data.get("application_url")

    # --------------------------------------------------------
    # VALIDATION
    # --------------------------------------------------------

    if not company or not job_title or not skills:

        return Response(
            {
                "status": "error",
                "message":
                    "company, job_title and skills are required"
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # --------------------------------------------------------
    # NORMALIZE SKILLS
    # --------------------------------------------------------

    if isinstance(skills, str):

        skills = [
            skill.strip()
            for skill in skills.split(",")
            if skill.strip()
        ]

    if not isinstance(skills, list) or not skills:

        return Response(
            {
                "status": "error",
                "message":
                    "skills must be a non-empty list"
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # --------------------------------------------------------
    # CREATE JOB GRAPH
    # --------------------------------------------------------

    result = create_job_graph(
        company_name=company,
        job_title=job_title,
        skills=skills,
        application_url=application_url
    )

    # --------------------------------------------------------
    # RESPONSE
    # --------------------------------------------------------

    return Response(
        {
            "status": "success",
            "data": result.data()
            if result
            else None
        },
        status=status.HTTP_201_CREATED
    )


# ============================================================
# LIST ALL JOBS
# ============================================================

@api_view(["GET"])
def list_jobs(request):

    jobs = get_all_jobs()

    return Response({
        "status": "success",
        "count": len(jobs),
        "data": jobs
    })


# ============================================================
# JOBS BY SKILL
# ============================================================

@api_view(["GET"])
def jobs_by_skill(request, skill_name):

    jobs = get_jobs_by_skill(skill_name)

    return Response({
        "status": "success",
        "skill": skill_name,
        "count": len(jobs),
        "jobs": jobs
    })


# ============================================================
# JOB DETAILS
# ============================================================

@api_view(["GET"])
def job_details(request, job_title):

    job = get_job_details(job_title)

    if not job:

        return Response(
            {
                "status": "error",
                "message": "Job not found"
            },
            status=status.HTTP_404_NOT_FOUND
        )

    return Response({
        "status": "success",
        "data": job
    })


# ============================================================
# MANUAL JOB MATCHING
# ============================================================

@api_view(["POST"])
def match_job(request):

    job_title = request.data.get("job_title")
    candidate_skills = request.data.get(
        "candidate_skills"
    )

    # --------------------------------------------------------
    # VALIDATION
    # --------------------------------------------------------

    if not job_title or not candidate_skills:

        return Response(
            {
                "status": "error",
                "message":
                    "job_title and candidate_skills are required"
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # --------------------------------------------------------
    # MATCH JOB
    # --------------------------------------------------------

    result = match_candidate_with_job(
        job_title,
        candidate_skills
    )

    # --------------------------------------------------------
    # JOB NOT FOUND
    # --------------------------------------------------------

    if not result:

        return Response(
            {
                "status": "error",
                "message": "Job not found"
            },
            status=status.HTTP_404_NOT_FOUND
        )

    # --------------------------------------------------------
    # RESPONSE
    # --------------------------------------------------------

    return Response({
        "status": "success",
        "data": result
    })


# ============================================================
# RESUME UPLOAD
# ============================================================

@api_view(["POST"])
def upload_resume(request):

    # --------------------------------------------------------
    # GET RESUME
    # --------------------------------------------------------

    resume = request.FILES.get("resume")

    if not resume:

        return Response(
            {
                "status": "error",
                "message": "Resume file is required"
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # --------------------------------------------------------
    # CHECK PDF
    # --------------------------------------------------------

    if not resume.name.lower().endswith(".pdf"):

        return Response(
            {
                "status": "error",
                "message": "Only PDF files are supported"
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # --------------------------------------------------------
    # EXTRACT RESUME TEXT
    # --------------------------------------------------------

    text = extract_resume_text(resume)

    if not text or not text.strip():

        return Response(
            {
                "status": "error",
                "message":
                    "Could not extract text from the resume."
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # --------------------------------------------------------
    # EXTRACT SKILLS
    # --------------------------------------------------------

    skills = extract_skills(text)

    # --------------------------------------------------------
    # EXTRACT CANDIDATE NAME
    # --------------------------------------------------------

    candidate_name = extract_candidate_name(text)

    if not candidate_name:

        candidate_name = (
            resume.name.rsplit(".", 1)[0]
        )

    # --------------------------------------------------------
    # CREATE CANDIDATE GRAPH
    # --------------------------------------------------------

    candidate_result = create_candidate_graph(
        candidate_name,
        skills
    )

    # --------------------------------------------------------
    # GENERATE RECOMMENDATIONS
    # --------------------------------------------------------

    recommendation_result = get_job_recommendations(
        candidate_name
    )

    # --------------------------------------------------------
    # SEPARATE RESULTS
    # --------------------------------------------------------

    recommendations = recommendation_result.get(
        "recommendations",
        []
    )

    skills_to_learn = recommendation_result.get(
        "skills_to_learn",
        []
    )

    # --------------------------------------------------------
    # RESPONSE
    # --------------------------------------------------------

    return Response({

        "status": "success",

        "filename": resume.name,

        "candidate": candidate_name,

        "skills": skills,

        "candidate_graph": candidate_result,

        "recommendations": recommendations,

        "skills_to_learn": skills_to_learn

    })


# ============================================================
# JOB RECOMMENDATIONS
# ============================================================

@api_view(["GET"])
def job_recommendations(request, candidate_name):

    result = get_job_recommendations(
        candidate_name
    )

    recommendations = result.get(
        "recommendations",
        []
    )

    skills_to_learn = result.get(
        "skills_to_learn",
        []
    )

    return Response({

        "status": "success",

        "candidate": candidate_name,

        "count": len(recommendations),

        "recommendations": recommendations,

        "skills_to_learn": skills_to_learn

    })



