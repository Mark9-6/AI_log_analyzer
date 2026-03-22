import re
import pandas as pd

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    return text

def parse_logs(log_text):
    lines = log_text.strip().split("\n")
    
    pattern = r'(\d{4}-\d{2}-\d{2}.*?)\s+([A-Z]+)\s+(.*)'
    
    parsed = []
    
    for line in lines:
        match = re.match(pattern, line)
        if match:
            timestamp, level, message = match.groups()
        else:
            timestamp = "UNKNOWN"
            level = "UNKNOWN"
            message = line
        
        parsed.append([timestamp, level, message])
    
    df = pd.DataFrame(parsed, columns=["timestamp", "level", "message"])
    df["clean_message"] = df["message"].apply(clean_text)
    
    return df