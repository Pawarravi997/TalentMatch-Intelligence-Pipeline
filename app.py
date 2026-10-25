import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
import parser_utils
import ai_engine
import urllib.parse  # Ensures special characters like '@' are safely encoded

# Database configurations variables
db_username = "root"
raw_password = "Ravi@1618" 
db_host = "localhost"
db_port = "3306"
db_name = "talentmatch_analytics_db"

# FIX: URL-encode the password to securely mask the '@' character into '%40'
db_password = urllib.parse.quote_plus(raw_password)

# Compile connection configurations safely
base_url = f"mysql+pymysql://{db_username}:{db_password}@{db_host}:{db_port}/"
base_engine = create_engine(base_url)

with base_engine.connect() as conn:
    conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {db_name}"))
    conn.commit()

engine_url = f"mysql+pymysql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}"
db_engine = create_engine(engine_url)

with db_engine.connect() as conn:
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS scan_logs (
            id INT AUTO_INCREMENT PRIMARY KEY,
            candidate_name VARCHAR(255),
            ats_score FLOAT,
            missing_skills TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """))
    conn.commit()


st.title("🚀 TalentMatch Intelligence Pipeline")
st.subheader("Enterprise Multi-Format ATS Optimization & Analytics Platform")

with st.sidebar:
    st.header("🔑 Configurations")
    api_key = st.text_input("Gemini API Key", type="password")
    
    st.markdown("---")
    st.header("📊 Database Historical Audits")
    if st.button("🔄 Fetch Pipeline History"):
        query = "SELECT candidate_name, ats_score, missing_skills, timestamp FROM scan_logs ORDER BY timestamp DESC"
        df_history = pd.read_sql(query, con=db_engine)
        if not df_history.empty:
            st.dataframe(df_history, use_container_width=True)
            st.line_chart(df_history.set_index('timestamp')['ats_score'])
        else:
            st.info("No historical analytics logged inside database.")

app_mode = st.tabs(["🚀 Individual Analyzer & Live Editor", "📦 Batch Processing Platform"])

with app_mode[0]:
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("📋 Target Job Specification")
        jd_mode = st.radio("JD Input Vector:", ("Raw Paste", "Direct URL Scraping"))
        jd_input = ""
        
        if jd_mode == "Direct URL Scraping":
            jd_url = st.text_input("Paste LinkedIn/Indeed Job Posting URL:")
            if st.button("🌐 Fetch & Scrape Website Text"):
                with st.spinner("Scraping portal data..."):
                    jd_input = parser_utils.scrape_jd_from_url(jd_url)
                    st.session_state['scraped_jd'] = jd_input
                    st.success("Web payload successfully parsed.")
            
            jd_input = st.text_area("Extracted Web Text Box", value=st.session_state.get('scraped_jd', ''), height=200)
        else:
            jd_input = st.text_area("Paste Target Job Description (JD) Here...", height=250)

    with col2:
        st.header("📄 Candidate Resume Panel")
        input_mode = st.radio("Resume Ingestion Route:", ("Artifact Upload (PDF / Image)", "Paste Profile Text"))
        
        resume_input_text = ""
        if input_mode == "Artifact Upload (PDF / Image)":
            uploaded_file = st.file_uploader("Drop Document System Base:", type=["pdf", "png", "jpg"])
            if uploaded_file is not None:
                file_bytes = uploaded_file.read()
                if uploaded_file.name.endswith('.pdf'):
                    resume_input_text = parser_utils.extract_text_from_pdf(file_bytes)
                else:
                    resume_input_text = parser_utils.extract_text_from_image(file_bytes)
                st.session_state['parsed_resume'] = resume_input_text
            
            resume_input_text = st.text_area("✍️ Live Resume Editor (Modify text here to watch ATS update)", value=st.session_state.get('parsed_resume', ''), height=200)
        else:
            resume_input_text = st.text_area("Paste Profile Text Character Arrays Here...", height=250)

    st.markdown("---")
    if st.button("🔍 Execute Strategic Gap Tracking", type="primary"):
        if not api_key:
            st.error("Authentication Token Missing.")
        elif not jd_input or not resume_input_text:
            st.warning("Context buffers empty.")
        else:
            with st.spinner("Processing analysis nodes..."):
                result = ai_engine.analyze_resume_vs_jd(resume_input_text, jd_input, api_key)
                
                if "error" in result:
                    st.error(result["error"])
                else:
                    st.success("Analysis sequence executed.")
                    score = result.get("ats_score", 0)
                    cand_name = result.get("candidate_name", "Unknown")
                    missing_str = ", ".join(result.get("missing_skills", []))
                    
                    with db_engine.connect() as conn:
                        conn.execute(
                            text("INSERT INTO scan_logs (candidate_name, ats_score, missing_skills) VALUES (:name, :score, :skills)"),
                            {"name": cand_name, "score": score, "skills": missing_str}
                        )
                        conn.commit()
                    
                    st.metric(label="📊 Calculated ATS Match Index", value=f"{score}%")
                    
                    tab1, tab2, tab3 = st.tabs(["🎯 Skill Badges", "🛠️ Improvements", "📝 Sample Layout"])
                    with tab1:
                        st.write("**Core Proficiencies:**")
                        p_html = " ".join([f"<span style='background-color:#d4edda; color:#155724; padding:5px 10px; margin:4px; border-radius:4px; display:inline-block;'><b>{s}</b></span>" for s in result.get("present_skills", [])])
                        st.markdown(p_html, unsafe_allow_html=True)
                        
                        st.write("\n**Unresolved Prerequisite Gaps:**")
                        m_html = " ".join([f"<span style='background-color:#f8d7da; color:#721c24; padding:5px 10px; margin:4px; border-radius:4px; display:inline-block;'><b>{s}</b></span>" for s in result.get("missing_skills", [])])
                        st.markdown(m_html, unsafe_allow_html=True)
                        
                    with tab2:
                        for idx, point in enumerate(result.get("improvement_points", []), 1):
                            st.write(f"{idx}. {point}")
                    with tab3:
                        st.code(result.get("sample_ats_resume", ""), language="markdown")

with app_mode[1]:
    st.header("📦 Batch Candidate Parsing & Structural Ranking")
    batch_jd = st.text_area("Paste Base Target JD for Evaluation Framework:", height=150, key="batch_jd_key")
    uploaded_files = st.file_uploader("Drop Multiple Candidate Profiles:", type=["pdf", "png", "jpg"], accept_multiple_files=True)
    
    if st.button("📊 Launch Automated Pipeline Ranking", type="primary"):
        if not api_key or not batch_jd or not uploaded_files:
            st.warning("Ensure requirements parameters are loaded.")
        else:
            ranking_data = []
            progress_bar = st.progress(0)
            
            for index, file in enumerate(uploaded_files):
                file_bytes = file.read()
                if file.name.endswith('.pdf'):
                    text_extracted = parser_utils.extract_text_from_pdf(file_bytes)
                else:
                    text_extracted = parser_utils.extract_text_from_image(file_bytes)
                
                res = ai_engine.analyze_resume_vs_jd(text_extracted, batch_jd, api_key)
                
                if "error" not in res:
                    ranking_data.append({
                        "File Name": file.name,
                        "Candidate Name": res.get("candidate_name", "Unknown"),
                        "ATS Score (%)": res.get("ats_score", 0),
                        "Missing Key Skills": ", ".join(res.get("missing_skills", []))
                    })
                
                progress_bar.progress((index + 1) / len(uploaded_files))
                
            df_ranks = pd.DataFrame(ranking_data)
            if not df_ranks.empty:
                df_ranks = df_ranks.sort_values(by="ATS Score (%)", ascending=False)
                st.success("Batch evaluation arrays completed successfully.")
                st.dataframe(df_ranks, use_container_width=True)
            else:
                st.error("Failed to parse clean attributes from files stack.")
