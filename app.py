import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.feature_extraction.text import TfidfVectorizer

from parser import parse_logs
from ai_helper import get_ai_suggestion

##---------------------------------------------------------##
# to upload file

uploaded_file = st.file_uploader("Upload log file", type=["txt", "log"])

if uploaded_file:
    log_input = uploaded_file.read().decode("utf-8")
##---------------------------------------------------------##

st.set_page_config(page_title="Log Analyzer", layout="wide")

st.title("📊 Log Analyzer with AI Suggestions")


log_input = st.text_area("Enter logs", height=250)
search_term = st.text_input("Search logs")
 



if st.button("Analyze Logs"):

    if not log_input.strip():
        st.warning("Please enter logs first!")
    
    else:
        df = parse_logs(log_input)

        if df.empty:
            st.error("Parsing failed")
        
        else:
            if search_term:
                df = df[df["message"].str.contains(search_term, case=False)]
            # Encode levels dynamically
            df["level_encoded"] = df["level"].astype("category").cat.codes

            # TF-IDF features
            vectorizer = TfidfVectorizer()
            text_features = vectorizer.fit_transform(df["clean_message"]).toarray()

            # Frequency feature
            df["message_freq"] = df["message"].map(df["message"].value_counts())

            
            features = np.hstack((
                df[["level_encoded", "message_freq"]].values,
                text_features
            ))

            # Model
            model = IsolationForest(contamination=0.3, random_state=42)
            df["anomaly"] = model.fit_predict(features)

            df["status"] = df["anomaly"].map({
                1: "Normal",
                -1: "Anomaly"
            })

            # ==============================
            # AI Suggestions
            # ==============================

            df["suggestion"] = "Normal log"

            with st.spinner("Generating AI suggestions..."):
                anomaly_indices = df[df["anomaly"] == -1].index
                for i in anomaly_indices:
                    df.at[i, "suggestion"] = get_ai_suggestion(df.at[i, "message"])

            # Output
            st.subheader("📋 Logs")
            st.dataframe(df)

            st.subheader("🚨 Anomalies with AI Suggestions")
            anomalies = df[df["anomaly"] == -1]

            if anomalies.empty:
                st.success("No anomalies found!")
            else:
                st.dataframe(anomalies[["timestamp", "level", "message", "suggestion"]])