
import streamlit as st
import PyPDF2
import google.generativeai as genai

# Configure the generative AI model
genai.configure(api_key="AIzaSyB_ZwnVAVGk_KneM2Qr8xUQztbbMoLnEVs")
model = genai.GenerativeModel("gemini-2.0-flash-exp")

# Function to extract text from the uploaded file
def extract_text_from_file(file):
    try:
        if file.type == "application/pdf":
            pdf_reader = PyPDF2.PdfReader(file)
            return "\n".join([page.extract_text() for page in pdf_reader.pages])
        elif file.type in ["text/plain", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
            return file.read().decode("utf-8")
        else:
            raise ValueError("Unsupported file type. Please upload a PDF or TXT file.")
    except Exception as e:
        st.error("Error extracting text from file: " + str(e))
        return None

# Function to generate resume suggestions using the AI model
def get_resume_suggestions(resume_text, job_description):
    try:
        prompt = (
            f"Here is a resume:\n{resume_text}\n\n"
            f"Here is a job description:\n{job_description}\n\n"
            "Provide detailed suggestions to tailor the resume for the job description."
        )
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error("Error generating suggestions: " + str(e))
        return None

# Main application
st.set_page_config(page_title="Resume Tailoring Assistant", page_icon="📄", layout="centered")

def main():
    st.title("📄 Resume Tailoring Assistant")
    st.markdown(
        """
        Upload your resume and paste the job description to receive actionable suggestions 
        on how to tailor your resume for the job.
        """
    )

    # Upload resume file
    uploaded_resume = st.file_uploader("Upload Your Resume (PDF or TXT)", type=["txt", "pdf"])

    # Input job description
    uploaded_job_description = st.text_area(
        "Paste the Job Description", placeholder="Copy and paste the job description here..."
    )

    # New feature: Display extracted resume content
    if uploaded_resume:
        resume_text = extract_text_from_file(uploaded_resume)
        if resume_text:
            st.subheader("📜 Extracted Resume Content")
            st.text_area("Your Resume Content", resume_text, height=200, disabled=True)

    # New feature: Skill matching
    if st.checkbox("Show Skill Matching"):
        if uploaded_resume and uploaded_job_description.strip():
            resume_text = extract_text_from_file(uploaded_resume)
            if resume_text:
                prompt = (
                    f"Resume Text:\n{resume_text}\n\n"
                    f"Job Description:\n{uploaded_job_description.strip()}\n\n"
                    "List key skills in the resume that match the job description, and suggest additional skills to add."
                )
                skill_response = model.generate_content(prompt)
                if skill_response:
                    st.subheader("🔑 Skill Matching Results")
                    st.write(skill_response.text)

    # New feature: Resume scoring
    if st.checkbox("Score My Resume"):
        if uploaded_resume and uploaded_job_description.strip():
            resume_text = extract_text_from_file(uploaded_resume)
            if resume_text:
                prompt = (
                    f"Resume Text:\n{resume_text}\n\n"
                    f"Job Description:\n{uploaded_job_description.strip()}\n\n"
                    "Evaluate the resume's relevance and alignment with the job description on a scale from 1 to 10. Provide reasoning for the score and areas for improvement."
                )
                score_response = model.generate_content(prompt)
                if score_response:
                    st.subheader("📊 Resume Scoring")
                    st.write(score_response.text)

    # Process inputs and generate suggestions
    if st.button("Generate Suggestions"):
        if uploaded_resume and uploaded_job_description.strip():
            resume_text = extract_text_from_file(uploaded_resume)
            if resume_text:
                suggestions = get_resume_suggestions(resume_text, uploaded_job_description.strip())
                if suggestions:
                    st.subheader("🔄 Suggestions for Your Resume")
                    st.write(suggestions)
        else:
            st.warning("Please upload a resume and provide a job description.")

    # New feature: Download tailored resume suggestions
    if uploaded_resume and uploaded_job_description.strip():
        resume_text = extract_text_from_file(uploaded_resume)
        if resume_text:
            suggestions = get_resume_suggestions(resume_text, uploaded_job_description.strip())
            if suggestions:
                tailored_resume = f"Original Resume:\n{resume_text}\n\nSuggestions:\n{suggestions}"
                st.download_button(
                    label="Download Tailored Resume Suggestions",
                    data=tailored_resume,
                    file_name="tailored_resume_suggestions.txt",
                    mime="text/plain"
                )

# Run the app
if __name__ == "__main__":
    main()
