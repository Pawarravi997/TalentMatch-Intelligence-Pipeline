from google import genai
import json

def analyze_resume_vs_jd(resume_text, jd_text, api_key):
    client = genai.Client(api_key=api_key)
    
    prompt = f"""
    You are a world-class Applicant Tracking System (ATS) expert and recruiter.
    Analyze the provided Resume Text against the Job Description (JD) Text.
    
    Deliver the output strictly in a valid JSON format with the exact keys specified below. 
    Do not include any conversational filler, markdown formatting blocks (like ```json), or extra text outside the JSON.

    Required JSON Structure:
    {{
      "ats_score": 85.5,
      "candidate_name": "Extract Candidate Name or Default to Unknown",
      "present_skills": ["Skill1", "Skill2"],
      "missing_skills": ["Skill3", "Skill4"],
      "improvement_points": [
        "Provide clear evidence of your data cleaning workflows.",
        "Highlight your expertise with relational database queries."
      ],
      "sample_ats_resume": "A clean Markdown-formatted resume layout integrating missing skills realistically."
    }}

    Resume Text:
    {resume_text}

    JD Text:
    {jd_text}
    """
    
    try:
        response = client.models.generate_content(
            model='gemini-3.8-flash',
            contents=prompt,
        )
        
        clean_json_str = response.text.strip()
        if clean_json_str.startswith("```json"):
            clean_json_str = clean_json_str[7:]
        if clean_json_str.endswith("```"):
            clean_json_str = clean_json_str[:-3]
        clean_json_str = clean_json_str.strip()
        
        data = json.loads(clean_json_str)
        return data
    except Exception as e:
        return {
            "error": f"AI Parsing Error: {str(e)}",
            "ats_score": 0,
            "candidate_name": "Unknown",
            "present_skills": [],
            "missing_skills": [],
            "improvement_points": ["Could not process request. Verify structural context."],
            "sample_ats_resume": "N/A"
        }
