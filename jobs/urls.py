# from django.urls import path
# from .views import health_check

# urlpatterns = [
#     path("health/", health_check, name="health-check"),
# ]

from django.urls import path
from .views import health_check,create_job,list_jobs, jobs_by_skill, job_details, match_job, upload_resume, job_recommendations

# from .views import create_job

urlpatterns = [
    path("health/", health_check, name="health-check"),
    path("jobs/", create_job, name="createjob"),
    path("jobs/list/", list_jobs, name="list-jobs"),
    path("skills/<str:skill_name>/", jobs_by_skill, name="jobs-by-skill"),
    path("jobs/details/<str:job_title>/",job_details,name="job-details"),
    path("match/", match_job, name="match-job"),
    path("resume/upload/", upload_resume, name="upload-resume"),
    path(
    "candidates/<str:candidate_name>/recommendations/",
    job_recommendations,
    ),


    



]