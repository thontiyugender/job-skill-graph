// import { useState } from "react";
// import "./App.css";

// import { useState } from "react";
// import "./App.css";

// const API_URL =
//   import.meta.env.VITE_API_URL ||
//   "https://job-skill-graph-megi.onrender.com";


// const API_URL =
//   import.meta.env.VITE_API_URL ||
//   "https://job-skill-graph-megi.onrender.com";


import { useState } from "react";
import "./App.css";

const API_URL =
  import.meta.env.VITE_API_URL ||
  "https://job-skill-graph-megi.onrender.com";

function App() {
  const [resume, setResume] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const [selectedJob, setSelectedJob] = useState(null);
  const [detailsLoading, setDetailsLoading] = useState(false);
  const [detailsError, setDetailsError] = useState("");

  // =========================================================
  // UPLOAD RESUME
  // =========================================================

  const uploadResume = async () => {
    if (!resume) {
      setError("Please select a PDF resume.");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);
    setSelectedJob(null);
    setDetailsError("");

    const formData = new FormData();
    formData.append("resume", resume);

    try {
      const response = await fetch(
        `${API_URL}/api/resume/upload/`,
        {
          method: "POST",
          body: formData,
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.message || "Resume upload failed."
        );
      }

      setResult(data);
    } catch (err) {
      console.error("Resume upload error:", err);

      setError(
        err.message ||
          "Failed to connect to backend."
      );
    } finally {
      setLoading(false);
    }
  };

  // =========================================================
  // VIEW JOB DETAILS
  // =========================================================

  const viewJobDetails = async (jobTitle) => {
    setDetailsLoading(true);
    setDetailsError("");
    setSelectedJob(null);

    try {
      const response = await fetch(
        `${API_URL}/api/jobs/details/${encodeURIComponent(
          jobTitle
        )}/`
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.message ||
            "Failed to load job details."
        );
      }

      setSelectedJob(data.data);

      setTimeout(() => {
        document
          .getElementById("job-details")
          ?.scrollIntoView({
            behavior: "smooth",
            block: "start",
          });
      }, 100);
    } catch (err) {
      console.error("Job details error:", err);

      setDetailsError(
        err.message ||
          "Failed to load job details."
      );
    } finally {
      setDetailsLoading(false);
    }
  };

  // =========================================================
  // CLOSE JOB DETAILS
  // =========================================================

  const closeJobDetails = () => {
    setSelectedJob(null);
    setDetailsError("");
  };

  // =========================================================
  // SCORE CLASS
  // =========================================================

  const getScoreClass = (score) => {
    if (score >= 90) return "score-excellent";
    if (score >= 75) return "score-good";
    if (score >= 50) return "score-average";

    return "score-low";
  };

  // =========================================================
  // RANK LABEL
  // =========================================================

  const getRankLabel = (index) => {
    if (index === 0) return "🥇 TOP MATCH";
    if (index === 1) return "🥈 #2 MATCH";
    if (index === 2) return "🥉 #3 MATCH";

    return `#${index + 1} MATCH`;
  };

  // =========================================================
  // RENDER
  // =========================================================

  return (
    <div className="app">

      {/* =====================================================
          HEADER
      ====================================================== */}

      <header className="header">
        <div className="header-content">
          <h1>Job Skill Graph</h1>

          <p>
            AI-Powered Job Recommendation System
          </p>
        </div>
      </header>

      <main className="container">

        {/* ===================================================
            UPLOAD RESUME
        ==================================================== */}

        <section className="upload-card">

          <div className="upload-icon">
            📄
          </div>

          <h2>
            Upload Your Resume
          </h2>

          <p className="upload-description">
            Upload your PDF resume to analyze your
            skills and discover suitable job
            opportunities.
          </p>

          <input
            id="resume-upload"
            type="file"
            accept=".pdf"
            onChange={(event) => {
              const file =
                event.target.files?.[0];

              setResume(file || null);
              setError("");
              setResult(null);
              setSelectedJob(null);
            }}
          />

          {resume && (
            <div className="selected-file">
              📎 {resume.name}
            </div>
          )}

          <button
            className="analyze-button"
            onClick={uploadResume}
            disabled={loading}
          >
            {loading
              ? "Analyzing Resume..."
              : "Analyze Resume"}
          </button>

          {error && (
            <div className="error">
              {error}
            </div>
          )}

        </section>

        {/* ===================================================
            RESULTS
        ==================================================== */}

        {result && (
          <section className="results">

            {/* =================================================
                CANDIDATE
            ================================================== */}

            <div className="candidate-card">

              <div className="candidate-icon">
                👤
              </div>

              <div>
                <p className="small-title">
                  Candidate
                </p>

                <h2>
                  {result.candidate ||
                    "Candidate"}
                </h2>
              </div>

            </div>

            {/* =================================================
                YOUR SKILLS
            ================================================== */}

            <div className="section-card">

              <h2>
                Your Skills
              </h2>

              <p className="section-description">
                Skills detected from your resume.
              </p>

              <div className="skills">

                {result.skills?.length > 0 ? (

                  result.skills.map(
                    (skill, index) => (
                      <span
                        className="skill-badge"
                        key={`${skill}-${index}`}
                      >
                        {skill}
                      </span>
                    )
                  )

                ) : (

                  <p className="no-results">
                    No skills detected.
                  </p>

                )}

              </div>

            </div>

            {/* =================================================
                RECOMMENDED JOBS
            ================================================== */}

            <div className="section-card">

              <div className="recommendation-heading">

                <div>
                  <h2>
                    Recommended Jobs
                  </h2>

                  <p className="section-description">
                    Jobs ranked according to
                    your skills.
                  </p>
                </div>

                <div className="job-count">
                  {result.recommendations?.length ||
                    0}{" "}
                  {result.recommendations?.length ===
                  1
                    ? "Job"
                    : "Jobs"}
                </div>

              </div>

              {result.recommendations?.length > 0 ? (

                result.recommendations.map(
                  (job, index) => {

                    const score =
                      Number(
                        job.match_percentage
                      ) || 0;

                    return (

                      <div
                        className={`job-card ${
                          index === 0
                            ? "top-job"
                            : ""
                        }`}
                        key={`${job.company || "company"}-${job.job}-${index}`}
                      >

                        {/* RANK */}

                        <div
                          className={`rank-badge ${
                            index === 0
                              ? "top-rank"
                              : ""
                          }`}
                        >
                          {getRankLabel(index)}
                        </div>

                        {/* JOB HEADER */}

                        <div className="job-header">

                          <div>

                            <p className="job-label">
                              Recommended Role
                            </p>

                            <h2>
                              {job.job}
                            </h2>

                            {job.company && (
                              <p className="company-name">
                                🏢 {job.company}
                              </p>
                            )}

                          </div>

                          <div
                            className={`match-score ${getScoreClass(
                              score
                            )}`}
                          >

                            <span>
                              Match
                            </span>

                            <strong>
                              {score}%
                            </strong>

                          </div>

                        </div>

                        {/* MATCH BAR */}

                        <div className="match-section">

                          <div className="match-header">

                            <span>
                              Match Score
                            </span>

                            <strong>
                              {score}%
                            </strong>

                          </div>

                          <div className="match-bar">

                            <div
                              className="match-fill"
                              style={{
                                width: `${Math.min(
                                  score,
                                  100
                                )}%`,
                              }}
                            />

                          </div>

                        </div>

                        {/* EXACT MATCHES */}

                        <div className="skill-group">

                          <h4>
                            <span className="section-dot exact-dot" />
                            Exact Matches
                          </h4>

                          <div className="skills exact-skills">

                            {job.matched_skills?.length >
                            0 ? (

                              job.matched_skills.map(
                                (
                                  skill,
                                  skillIndex
                                ) => (

                                  <span
                                    key={`${skill}-${skillIndex}`}
                                  >
                                    ✓ {skill}
                                  </span>

                                )
                              )

                            ) : (

                              <span>
                                No exact matches
                              </span>

                            )}

                          </div>

                        </div>

                        {/* RELATED SKILLS */}

                        <div className="skill-group">

                          <h4>
                            <span className="section-dot related-dot" />
                            Related Skills
                          </h4>

                          <div className="skills related-skills">

                            {job.related_skills?.length >
                            0 ? (

                              job.related_skills.map(
                                (
                                  skill,
                                  skillIndex
                                ) => (

                                  <span
                                    key={`${skill}-${skillIndex}`}
                                  >
                                    ↗ {skill}
                                  </span>

                                )
                              )

                            ) : (

                              <span>
                                No related skills
                              </span>

                            )}

                          </div>

                        </div>

                        {/* MISSING SKILLS */}

                        <div className="skill-group">

                          <h4>
                            <span className="section-dot missing-dot" />
                            Missing Skills
                          </h4>

                          <div className="skills missing-skills">

                            {job.missing_skills?.length >
                            0 ? (

                              job.missing_skills.map(
                                (
                                  skill,
                                  skillIndex
                                ) => (

                                  <span
                                    key={`${skill}-${skillIndex}`}
                                  >
                                    ✗ {skill}
                                  </span>

                                )
                              )

                            ) : (

                              <span className="no-missing">
                                ✓ No missing skills
                              </span>

                            )}

                          </div>

                        </div>

                        {/* SKILL GAP */}

                        <div className="skill-gap">

                          <div className="skill-gap-header">

                            <h4>
                              🎯 Skills to Improve
                            </h4>

                            <p>
                              Skills that can improve
                              your eligibility for
                              this role.
                            </p>

                          </div>

                          {job.skill_gap?.length > 0 ? (

                            <div className="skill-gap-list">

                              {job.skill_gap.map(
                                (
                                  skill,
                                  skillIndex
                                ) => (

                                  <div
                                    className="skill-gap-item"
                                    key={`${skill}-${skillIndex}`}
                                  >

                                    <span className="gap-icon">
                                      ↑
                                    </span>

                                    <span>
                                      {skill}
                                    </span>

                                  </div>

                                )
                              )}

                            </div>

                          ) : (

                            <div className="skill-gap-success">
                              ✓ You already have
                              all the required
                              skills for this role.
                            </div>

                          )}

                        </div>

                        {/* WHY THIS JOB */}

                        {job.why_this_job?.length >
                          0 && (

                          <div className="why-job">

                            <h4>
                              💡 Why This Job?
                            </h4>

                            <div className="why-job-list">

                              {job.why_this_job.map(
                                (
                                  reason,
                                  reasonIndex
                                ) => (

                                  <div
                                    className="why-job-item"
                                    key={reasonIndex}
                                  >

                                    <span className="why-job-icon">
                                      ✓
                                    </span>

                                    <span>
                                      {reason}
                                    </span>

                                  </div>

                                )
                              )}

                            </div>

                          </div>

                        )}

                        {/* ACTION BUTTONS */}

                        <div className="job-actions">

                          <button
                            className="details-button"
                            onClick={() =>
                              viewJobDetails(job.job)
                            }
                          >
                            🔍 View Job Details
                          </button>

                          {job.application_url ? (

                            <a
                              className="apply-button"
                              href={
                                job.application_url
                              }
                              target="_blank"
                              rel="noopener noreferrer"
                            >
                              🚀 Apply Now
                            </a>

                          ) : (

                            <div className="no-application">
                              Application link unavailable
                            </div>

                          )}

                        </div>

                      </div>

                    );
                  }
                )

              ) : (

                <div className="no-results">
                  No suitable jobs found.
                </div>

              )}

            </div>

            {/* =================================================
                JOB DETAILS LOADING
            ================================================== */}

            {detailsLoading && (

              <div className="job-details-card">

                <div className="details-loading">

                  <div className="loading-spinner"></div>

                  <h2>
                    Loading Job Details...
                  </h2>

                  <p>
                    Fetching company and skill
                    information.
                  </p>

                </div>

              </div>

            )}

            {/* =================================================
                JOB DETAILS ERROR
            ================================================== */}

            {detailsError && (

              <div className="job-details-card details-error">

                <div className="details-error-icon">
                  ⚠️
                </div>

                <h2>
                  Unable to Load Job Details
                </h2>

                <p>
                  {detailsError}
                </p>

                <button
                  className="close-details"
                  onClick={() =>
                    setDetailsError("")
                  }
                >
                  Close
                </button>

              </div>

            )}

            {/* =================================================
                JOB DETAILS
            ================================================== */}

            {selectedJob && (

              <div
                id="job-details"
                className="job-details-card"
              >

                <div className="details-header">

                  <div>

                    <p className="job-label">
                      Job Details
                    </p>

                    <h2>
                      {selectedJob.job}
                    </h2>

                  </div>

                  <button
                    className="close-details"
                    onClick={closeJobDetails}
                  >
                    ✕
                  </button>

                </div>

                {/* COMPANY DETAILS */}

                <div className="company-details-list">

                  <h3>
                    🏢 Companies
                  </h3>

                  {selectedJob.company_details?.length >
                  0 ? (

                    selectedJob.company_details.map(
                      (companyInfo, index) => (

                        <div
                          className="company-detail-item"
                          key={`${companyInfo.company}-${index}`}
                        >

                          <div>

                            <p className="details-label">
                              Company
                            </p>

                            <strong>
                              {companyInfo.company}
                            </strong>

                          </div>

                          {companyInfo.application_url ? (

                            <a
                              className="small-apply-button"
                              href={
                                companyInfo.application_url
                              }
                              target="_blank"
                              rel="noopener noreferrer"
                            >
                              🚀 Apply
                            </a>

                          ) : (

                            <span className="small-no-link">
                              No application link
                            </span>

                          )}

                        </div>

                      )
                    )

                  ) : (

                    <p className="no-results">
                      Company information unavailable.
                    </p>

                  )}

                </div>

                {/* REQUIRED SKILLS */}

                <div className="details-section">

                  <h3>
                    🛠 Required Skills
                  </h3>

                  <p className="details-description">
                    Skills required for this job.
                  </p>

                  <div className="skills">

                    {selectedJob.skills?.length > 0 ? (

                      selectedJob.skills.map(
                        (skill, index) => (

                          <span
                            className="skill-badge"
                            key={`${skill}-${index}`}
                          >
                            {skill}
                          </span>

                        )
                      )

                    ) : (

                      <p className="no-results">
                        No required skills available.
                      </p>

                    )}

                  </div>

                </div>

                <button
                  className="details-close-button"
                  onClick={closeJobDetails}
                >
                  Close Details
                </button>

              </div>

            )}

            {/* =================================================
                SKILLS TO LEARN
            ================================================== */}

            {result.skills_to_learn?.length > 0 && (

              <div className="section-card learning-card">

                <div className="learning-heading">

                  <div>

                    <h2>
                      🎯 Skills to Learn
                    </h2>

                    <p className="section-description">
                      These skills can improve
                      your eligibility across
                      multiple recommended jobs.
                    </p>

                  </div>

                  <div className="learning-count">

                    {result.skills_to_learn.length}{" "}

                    {result.skills_to_learn.length === 1
                      ? "Skill"
                      : "Skills"}

                  </div>

                </div>

                <div className="learning-list">

                  {result.skills_to_learn.map(
                    (item, index) => (

                      <div
                        className="learning-item"
                        key={`${item.skill}-${index}`}
                      >

                        <div className="learning-rank">
                          {index + 1}
                        </div>

                        <div className="learning-info">

                          <h3>
                            {item.skill}
                          </h3>

                          <p>
                            Helps improve your
                            match for{" "}
                            <strong>
                              {item.job_count}
                            </strong>{" "}
                            {item.job_count === 1
                              ? "job"
                              : "jobs"}
                          </p>

                        </div>

                        <div className="learning-arrow">
                          →
                        </div>

                      </div>

                    )
                  )}

                </div>

              </div>

            )}

          </section>
        )}

      </main>

    </div>
  );
}

export default App;

