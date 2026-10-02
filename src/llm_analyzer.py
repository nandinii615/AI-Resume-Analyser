import json
from google import genai
from google.genai import types
from src.config import GEMINI_API_KEY


# ---------------------------------------------------------
# Gemini Client
# ---------------------------------------------------------

client = genai.Client(api_key=GEMINI_API_KEY)


# ---------------------------------------------------------
# Local fallback analysis
# ---------------------------------------------------------

def local_fallback_analysis(resume_text, job_description):
    """
    Local ATS analysis used when Gemini is temporarily unavailable.
    """

    resume_lower = resume_text.lower()
    job_lower = job_description.lower()

    skills = [
        "python",
        "java",
        "c++",
        "c",
        "javascript",
        "typescript",
        "html",
        "css",
        "react",
        "angular",
        "node.js",
        "django",
        "flask",
        "sql",
        "mysql",
        "postgresql",
        "mongodb",
        "git",
        "github",
        "docker",
        "aws",
        "azure",
        "gcp",
        "rest api",
        "api",
        "machine learning",
        "deep learning",
        "artificial intelligence",
        "pandas",
        "numpy",
        "tensorflow",
        "pytorch",
        "streamlit",
    ]

    matched_skills = []
    missing_skills = []

    for skill in skills:

        if skill in job_lower:

            if skill in resume_lower:
                matched_skills.append(skill.title())

            else:
                missing_skills.append(skill.title())

    # Remove duplicates while preserving order
    matched_skills = list(dict.fromkeys(matched_skills))
    missing_skills = list(dict.fromkeys(missing_skills))

    # -----------------------------------------------------
    # Match percentage
    # -----------------------------------------------------

    total_required = len(matched_skills) + len(missing_skills)

    if total_required > 0:

        match_percentage = round(
            (len(matched_skills) / total_required) * 100
        )

    else:

        match_percentage = 50

    # -----------------------------------------------------
    # Strengths
    # -----------------------------------------------------

    strengths = []

    if matched_skills:

        strengths.append(
            "The resume contains relevant skills required for "
            "the job, including "
            + ", ".join(matched_skills[:5])
            + "."
        )

    if "b.tech" in resume_lower or "bachelor" in resume_lower:

        strengths.append(
            "The resume contains a relevant bachelor's-level "
            "educational background."
        )

    if "project" in resume_lower:

        strengths.append(
            "The resume includes project experience."
        )

    if not strengths:

        strengths.append(
            "The resume contains information that can be "
            "evaluated against the job requirements."
        )

    # -----------------------------------------------------
    # Improvements
    # -----------------------------------------------------

    improvements = []

    for skill in missing_skills[:5]:

        improvements.append(
            f"Consider gaining or highlighting experience with {skill}."
        )

    if "project" not in resume_lower:

        improvements.append(
            "Add relevant projects with specific technologies "
            "and measurable results."
        )

    if not improvements:

        improvements.append(
            "Add specific achievements, project details, "
            "and measurable results to strengthen the resume."
        )

    # -----------------------------------------------------
    # Final feedback
    # -----------------------------------------------------

    if missing_skills:

        feedback = (
            "The resume matches some of the required skills, "
            "but additional job-specific skills should be "
            "highlighted to improve the match."
        )

    else:

        feedback = (
            "The resume contains the main skills identified "
            "in the job description."
        )

    return {
        "match_percentage": match_percentage,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "strengths": strengths,
        "improvements": improvements,
        "final_feedback": feedback,
    }


# ---------------------------------------------------------
# Gemini Resume Analysis
# ---------------------------------------------------------

def analyze_resume(resume_text, job_description):

    # -----------------------------------------------------
    # Load prompt from external file
    # -----------------------------------------------------

    with open(
        "prompts/resume_prompt.txt",
        "r",
        encoding="utf-8"
    ) as f:

        system_prompt = f.read()

    # -----------------------------------------------------
    # Prepare input
    # -----------------------------------------------------

    user_prompt = f"""
Resume:

{resume_text}


Job Description:

{job_description}
"""

    try:

        # -------------------------------------------------
        # Gemini API call
        # -------------------------------------------------

        response = client.models.generate_content(

            model="gemini-3.5-flash",

            contents=user_prompt,

            config=types.GenerateContentConfig(

                system_instruction=system_prompt,

                response_mime_type="application/json",

                temperature=0.2,

            ),
        )

        # -------------------------------------------------
        # Parse Gemini JSON response
        # -------------------------------------------------

        result = response.text.strip()

        return json.loads(result)

    except Exception as e:

        # -------------------------------------------------
        # Gemini failure → Local fallback
        # -------------------------------------------------

        print(
            "Gemini unavailable. "
            "Using local ATS fallback."
        )

        print(
            "Gemini error:",
            e
        )

        return local_fallback_analysis(
            resume_text,
            job_description
        )