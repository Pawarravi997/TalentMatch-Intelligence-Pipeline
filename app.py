import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
import parser_utils
import ai_engine
import os

st.set_page_config(page_title="TalentMatch Intelligence Pipeline", layout="wide")

# AUTOMATIC ENVIRONMENT DETECTION
IS_CLOUD = os.environ.get("HOME") == "/mount/src" or "STREAMLIT_SERVER_PORT" in os.environ

if not IS_CLOUD:
    # 💻 Local PC Setup: Routes data cleanly through your local MySQL instance
    import urllib.parse
    db_username = "root"
    raw_password = "Ravi@1618" 
    db_host = "localhost"
    db_port = "3306"
    db_name = "talentmatch_analytics_db"

    db_password = urllib.parse.quote_plus(raw_password)
    base_url = f"mysql+pymysql://{db_username}:{db_password}@{db_host}:{db_port}/"
    base_engine = create_engine(base_url)
    with base_engine.connect() as conn:
        conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {db_name}"))
        conn.commit()

    engine_url = f"mysql+pymysql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}"
    db_engine = create_engine(engine_url)
else:
    # ☁️ Streamlit Cloud Setup: Routes data through a serverless SQLite data layer to bypass network blocks
    db_engine = create_engine("sqlite:///talentmatch_cloud.db")

# DYNAMIC TABLE RENDERING CROSS-PLATFORM
with db_engine.connect() as conn:
    if not IS_CLOUD:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS scan_logs (
                id INT AUTO_INCREMENT PRIMARY KEY,
                candidate_name VARCHAR(255),
                ats_score FLOAT,
                missing_skills TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """))
    else:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS scan_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                candidate_name TEXT,
                ats_score REAL,
                missing_skills TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """))
    conn.commit()
