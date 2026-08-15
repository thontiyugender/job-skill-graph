# Job Skill Graph

A full-stack Job Skill Graph application built using Django REST Framework, React, and Neo4j/CognoDB.

## Features

- Job management
- Job listing and job details
- Job search by skill
- Resume PDF upload
- Resume skill extraction
- Candidate skill graph
- Job matching
- Match percentage calculation
- Skill-gap analysis
- Job recommendations
- Skills-to-learn recommendations
- Application URLs

## Tech Stack

### Backend

- Python
- Django
- Django REST Framework
- Neo4j / CognoDB

### Frontend

- React
- Vite
- JavaScript
- CSS

## API

- GET /api/jobs/list/
- GET /api/jobs/details/<job_title>/
- GET /api/skills/<skill_name>/
- POST /api/jobs/
- POST /api/match/
- POST /api/resume/upload/
- GET /api/candidates/<candidate_name>/recommendations/

## Database

The project uses Neo4j/CognoDB to represent relationships between:

- Companies
- Jobs
- Candidates
- Skills

## GitHub

https://github.com/thontiyugender/job-skill-graph
