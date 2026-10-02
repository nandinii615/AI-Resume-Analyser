import streamlit as st

from src.llm_analyzer import analyze_resume
from src.pdf_extractor import extract_text_from_pdf


st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)
# Sidebar
with st.sidebar:
    st.header("📌 About the Project")

    st.write(
        "AI Resume Analyzer is an intelligent resume screening "
        "application that compares a candidate's resume with a "
        "job description."
    )

    st.divider()

    st.subheader("🔧 Technologies Used")

    st.write("• Python")
    st.write("• Streamlit")
    st.write("• NLP")
    st.write("• PDF Text Extraction")
    st.write("• Google Gemini AI")

    st.divider()

    st.caption("AI Resume Analyzer | College Project")
st.title("📄 AI Resume Analyzer")
st.subheader("AI-Powered Resume Screening & Job Matching")

st.write(
    "Upload your resume and compare it with a job description "
    "to identify skill matches, missing skills, strengths, and areas for improvement."
)

st.divider()

# How It Works
st.subheader("⚙️ How It Works")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 1️⃣ Upload Resume")
    st.write("Upload your resume in PDF format.")

with col2:
    st.markdown("### 2️⃣ Add Job Description")
    st.write("Paste the job description you want to compare against.")

with col3:
    st.markdown("### 3️⃣ Get AI Analysis")
    st.write("The system analyzes the resume and provides a match score and recommendations.")

st.divider()

# Upload Resume
st.subheader("📤 Upload Resume")
resume = st.file_uploader(
    "Choose a PDF Resume",
    type=["pdf"]
)

# Job Description
st.subheader("📋 Job Description")

job_description = st.text_area(
    "Paste the Job Description",
    height=200
)

# Analyze Button
col1, col2 = st.columns(2)

with col1:
    analyze_button = st.button("🔍 Analyze Resume")

with col2:
    reset_button = st.button("🔄 Reset")

if reset_button:
    st.rerun()

if analyze_button:

    if resume is None:
        st.warning("Please upload your resume.")

    elif job_description.strip() == "":
        st.warning("Please paste the job description.")

    else:
        st.success("Resume uploaded successfully!")

        # Extract text from PDF
        resume_text = extract_text_from_pdf(resume)

        if not resume_text.strip():
            st.error("Could not extract text from the resume PDF.")

        else:
            st.subheader("📄 Extracted Resume Text")

            st.text_area(
                "Resume Content",
                resume_text,
                height=300
            )

            # Analyze resume using Gemini
            with st.spinner("Analyzing resume with Gemini AI..."):

                result = analyze_resume(
                    resume_text,
                    job_description
                )

            # Results
            st.divider()

            st.subheader("📊 Resume Match Score")

            score = result["match_percentage"]

            st.progress(score / 100)

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    label="Resume Match Score",
                    value=f"{score}%"
                )

            with col2:
                if score >= 75:
                    st.success("Strong Match")
                elif score >= 50:
                    st.warning("Moderate Match")
                else:
                    st.error("Needs Improvement")

            # Matched Skills
            st.subheader("✅ Matched Skills")

            matched_skills = result["matched_skills"]
            if matched_skills:
                  for skill in sorted(matched_skills):
                      st.success(f"✓ {skill}")
            else:
                  st.write("No matched skills found.")

            # Missing Skills
            st.subheader("❌ Missing Skills")

            missing_skills = result["missing_skills"]

            if missing_skills:
                for skill in sorted(missing_skills):
                    st.error(f"✗ {skill}")
            else:
                st.write("No major missing skills identified.")
            # Strengths
                        # Strengths
            st.subheader("💪 Strengths")

            for strength in result["strengths"]:
                st.success(f"✓ {strength}")
            # Improvements
                        # Improvements
            st.subheader("🛠️ Suggested Improvements")

            for improvement in result["improvements"]:
                st.warning(f"💡 {improvement}")
            # Final Feedback
                        # Final Feedback
            st.subheader("📝 Final Feedback")

            st.info(
                f"📌 {result['final_feedback']}"
            )
            # Footer
st.divider()

st.caption(
    "AI Resume Analyzer | Built using Python, Streamlit, NLP & Google Gemini AI"
)