import csv
import os
from datetime import datetime
from state import AgentState

ESCALATION_LOG = "escalation_log.csv"

def ensure_csv_header():
    """Ensure CSV file has proper headers"""
    if not os.path.exists(ESCALATION_LOG):
        with open(ESCALATION_LOG, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([
                "timestamp", 
                "subject", 
                "description", 
                "attempts", 
                "feedback", 
                "failed_drafts"
            ])

def escalate(state: AgentState) -> AgentState:
    ensure_csv_header()
    
    with open(ESCALATION_LOG, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            datetime.now().isoformat(),
            state["subject"],
            state["description"],
            state["attempts"],
            state["reviewer_feedback"],
            "; ".join(state["failed_drafts"])  # Join multiple drafts with semicolon
        ])
    
    print("🚨 Escalated and logged to CSV")
    return state