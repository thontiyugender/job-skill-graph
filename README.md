# 🚀 Job Skill Graph

> **Turn your resume into a career roadmap.**

Job Skill Graph is a full-stack application that connects **candidates, skills, jobs, and companies** using a graph database.

The application analyzes a candidate's resume, extracts skills, compares them with job requirements, identifies skill gaps, discovers related skills, and recommends suitable jobs.

---

## 🎯 Project Objective

The goal of this project is to demonstrate how a **graph database** can solve a real-world job-matching problem where relationships between entities are important.

The system answers questions such as:

- Which jobs match a candidate's skills?
- What skills are missing for a particular job?
- Which related skills can improve a candidate's match?
- Which jobs are the best fit?
- What skills should the candidate learn next?

---

## ✨ Features

### 📄 Resume Processing

- Resume PDF upload
- Candidate information extraction
- Technical skill extraction
- Candidate skill graph creation

### 💼 Job Management

- Create jobs
- List jobs
- View job details
- Search jobs by skill
- Company and application URL support

### 🎯 Job Matching

- Candidate-to-job skill matching
- Match percentage calculation
- Exact skill matching
- Related-skill matching
- Missing skill detection
- Skill-gap analysis

### 🧠 Recommendations

- Personalized job recommendations
- Job ranking based on compatibility
- Skills-to-learn recommendations
- Related skill discovery

---

# 🧠 Why a Graph Database?

Job matching is fundamentally a **relationship problem**.

A candidate has skills, jobs require skills, companies offer jobs, and skills can be related to other skills.

A traditional relational database could store these entities in separate tables, but complex matching would require multiple JOIN operations.

A graph database represents these relationships directly.

For example:

```text
Candidate
    ↓ HAS_SKILL
Skill
    ↓ RELATED_TO
Related Skill
    ↓ REQUIRES
Job
    ↓ OFFERS
Company



