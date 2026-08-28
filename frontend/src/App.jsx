import { useEffect, useState } from "react";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";

function App() {
  const [profile, setProfile] = useState(null);
  const [skills, setSkills] = useState([]);
  const [careers, setCareers] = useState([]);
  const [recommendations, setRecommendations] = useState([]);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    loadData();
  }, []);

  async function loadData() {
    try {
      setLoading(true);
      setError("");

      const [
        profileResponse,
        skillsResponse,
        careersResponse,
        recommendationsResponse,
      ] = await Promise.all([
        fetch(`${API_URL}/students/1/profile`),
        fetch(`${API_URL}/skills/`),
        fetch(`${API_URL}/careers/`),
        fetch(`${API_URL}/students/1/career-recommendations`),
      ]);

      if (!profileResponse.ok) {
        throw new Error("Failed to load student profile");
      }

      if (!skillsResponse.ok) {
        throw new Error("Failed to load skills");
      }

      if (!careersResponse.ok) {
        throw new Error("Failed to load careers");
      }

      if (!recommendationsResponse.ok) {
        throw new Error("Failed to load recommendations");
      }

      const profileData = await profileResponse.json();
      const skillsData = await skillsResponse.json();
      const careersData = await careersResponse.json();
      const recommendationsData = await recommendationsResponse.json();

      setProfile(profileData);
      setSkills(skillsData);
      setCareers(careersData);
      setRecommendations(recommendationsData);
    } catch (err) {
      console.error(err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  const bestMatch =
    recommendations.length > 0 ? recommendations[0] : null;

  if (loading) {
    return (
      <div className="loading-screen">
        <div className="loader"></div>
        <h2>Loading your career graph...</h2>
      </div>
    );
  }

  return (
    <div className="app">
      {/* NAVBAR */}
      <nav className="navbar">
        <div className="logo">
          <div className="logo-icon">SC</div>

          <div>
            <h2>SkillCareer</h2>
            <span>Student Skill & Career Graph</span>
          </div>
        </div>

        <div className="nav-links">
          <a href="#profile">Profile</a>
          <a href="#skills">Skills</a>
          <a href="#careers">Careers</a>
          <a href="#recommendations">Recommendations</a>
        </div>
      </nav>

      {/* ERROR */}
      {error && (
        <div className="error-box">
          <strong>Unable to load data</strong>
          <p>{error}</p>

          <button onClick={loadData}>
            Try Again
          </button>
        </div>
      )}

      {/* HERO */}
      <section className="hero-section">
        <div>
          <div className="eyebrow">
            CAREER INTELLIGENCE PLATFORM
          </div>

          <h1>
            Turn your skills into
            <br />
            your <span>career path.</span>
          </h1>

          <p className="hero-text">
            Track your technical skills, explore career paths,
            and discover which careers best match your current
            abilities.
          </p>

          <a
            href="#recommendations"
            className="primary-button"
          >
            View Career Recommendations
          </a>
        </div>

        <div className="hero-card">
          <div className="hero-card-header">
            <span>Career Match</span>

            <span className="live-dot">
              ● Live
            </span>
          </div>

          {bestMatch ? (
            <>
              <h2>{bestMatch.career_title}</h2>

              <div className="match-circle">
                <strong>
                  {bestMatch.match_percentage}%
                </strong>

                <span>Best Match</span>
              </div>

              <p>
                Based on your current skills and their
                importance for the selected career path.
              </p>
            </>
          ) : (
            <p>No career recommendations available.</p>
          )}
        </div>
      </section>

      {/* PROFILE */}
      <section id="profile" className="section">
        <div className="section-heading">
          <h2>Your Profile</h2>
        </div>

        {profile ? (
          <div className="profile-card">
            <div className="avatar">
              {profile.name
                ? profile.name.charAt(0).toUpperCase()
                : "S"}
            </div>

            <div className="profile-info">
              <h3>{profile.name || "Student"}</h3>

              <p>
                {profile.email || "Student Profile"}
              </p>
            </div>

            <div className="profile-details">
              <div>
                <span>Student ID</span>
                <strong>{profile.id || 1}</strong>
              </div>

              <div>
                <span>Skills</span>
                <strong>{skills.length}</strong>
              </div>

              <div>
                <span>Career Paths</span>
                <strong>{careers.length}</strong>
              </div>
            </div>
          </div>
        ) : (
          <div className="profile-card">
            <p>No profile information available.</p>
          </div>
        )}
      </section>

      {/* SKILLS */}
      <section id="skills" className="section">
        <div className="section-heading">
          <div>
            <h2>Your Skills</h2>
          </div>

          <div className="count-badge">
            {skills.length} Skills
          </div>
        </div>

        <div className="skills-grid">
          {skills.map((skill) => (
            <div
              className="skill-card"
              key={skill.id}
            >
              <div className="skill-icon">
                {skill.name
                  ? skill.name.charAt(0).toUpperCase()
                  : "S"}
              </div>

              <div className="skill-content">
                <h3>{skill.name}</h3>

                <p>{skill.category}</p>

                <div className="level-row">
                  <span>Level:</span>

                  <strong>
                    {skill.level || "Beginner"}
                  </strong>
                </div>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* CAREERS */}
      <section id="careers" className="section">
        <div className="section-heading">
          <div>
            <h2>Explore Careers</h2>
          </div>

          <div className="count-badge">
            {careers.length} Careers
          </div>
        </div>

        <div className="careers-grid">
          {careers.map((career, index) => (
            <div
              className="career-card"
              key={career.id}
            >
              <div className="career-number">
                0{index + 1}
              </div>

              <h3>{career.title}</h3>

              <p>{career.description}</p>

              <button>
                Explore Career →
              </button>
            </div>
          ))}
        </div>
      </section>

      {/* RECOMMENDATIONS */}
      <section
        id="recommendations"
        className="section recommendations-section"
      >
        <div className="section-heading">
          <div>
            <h2>Career Recommendations</h2>
          </div>

          <div className="count-badge">
            {recommendations.length} Matches
          </div>
        </div>

        <div className="recommendation-list">
          {recommendations.map(
            (recommendation, index) => (
              <div
                className="recommendation-card"
                key={recommendation.career_id}
              >
                <div className="recommendation-rank">
                  #{index + 1}
                </div>

                <div className="recommendation-main">
                  <div className="recommendation-title">
                    <div>
                      <h3>
                        {recommendation.career_title}
                      </h3>

                      <p>
                        {recommendation.description}
                      </p>
                    </div>

                    <div className="percentage">
                      {recommendation.match_percentage}%

                      <span>Match</span>
                    </div>
                  </div>

                  <div className="progress-bar">
                    <div
                      className="progress"
                      style={{
                        width: `${Math.min(
                          recommendation.match_percentage,
                          100
                        )}%`,
                      }}
                    ></div>
                  </div>

                  <div className="matched-skills">
                    <span>Matched skills:</span>

                    {recommendation.matched_skills &&
                    recommendation.matched_skills.length >
                      0 ? (
                      recommendation.matched_skills.map(
                        (skill) => (
                          <span
                            className="matched-skill"
                            key={skill.skill_id}
                          >
                            {skill.skill_name}

                            <small>
                              Level {skill.student_level}
                            </small>
                          </span>
                        )
                      )
                    ) : (
                      <span className="no-match">
                        No matching skills yet
                      </span>
                    )}
                  </div>
                </div>
              </div>
            )
          )}
        </div>
      </section>

      {/* FOOTER */}
      <footer>
        <div>
          <strong>SkillCareer</strong>
          <span>
            Student Skill & Career Graph
          </span>
        </div>

        <p>
          Powered by FastAPI + React
        </p>
      </footer>
    </div>
  );
}

export default App;