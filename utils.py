"""
Utilities for handling call summaries and contact management
"""
import csv
import json
import os
from datetime import datetime
from typing import Dict, List, Optional


class CallSummaryManager:
    """Manages call summaries and contact information"""
    
    def __init__(self, summary_dir: str = "call_summaries"):
        self.summary_dir = summary_dir
        os.makedirs(summary_dir, exist_ok=True)
    
    def create_summary(
        self,
        contact_info: Dict[str, str],
        topics: List[str],
        outcome: str,
        follow_up: bool = False,
        notes: str = ""
    ) -> Dict:
        """Create a structured call summary"""
        return {
            "timestamp": datetime.now().isoformat(),
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "contact_info": {
                "name": contact_info.get("name", ""),
                "company": contact_info.get("company", ""),
                "phone": contact_info.get("phone", ""),
                "email": contact_info.get("email", ""),
                "preferred_contact": contact_info.get("preferred_contact", "phone")
            },
            "call_details": {
                "topics_discussed": topics,
                "outcome": outcome,
                "follow_up_required": follow_up,
                "notes": notes
            }
        }
    
    def save_summary(self, summary: Dict) -> str:
        """Save call summary to JSON file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"call_{timestamp}.json"
        filepath = os.path.join(self.summary_dir, filename)
        
        with open(filepath, 'w') as f:
            json.dump(summary, f, indent=2)
        
        return filepath
    
    def get_all_summaries(self) -> List[Dict]:
        """Retrieve all call summaries"""
        summaries = []
        
        for filename in os.listdir(self.summary_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(self.summary_dir, filename)
                with open(filepath, 'r') as f:
                    summaries.append(json.load(f))
        
        return sorted(summaries, key=lambda x: x.get('timestamp', ''), reverse=True)
    
    def get_summary_by_date(self, date: str) -> List[Dict]:
        """Get summaries for a specific date (YYYY-MM-DD)"""
        all_summaries = self.get_all_summaries()
        return [s for s in all_summaries if s.get('timestamp', '').startswith(date)]
    
    def export_contacts_csv(self, output_file: str = "contacts.csv"):
        """Export all contact information to CSV"""
        summaries = self.get_all_summaries()
        
        with open(output_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=[
                'date', 'name', 'company', 'phone', 'email', 
                'preferred_contact', 'outcome', 'follow_up_required'
            ])
            writer.writeheader()
            
            for summary in summaries:
                contact = summary.get('contact_info', {})
                details = summary.get('call_details', {})
                
                writer.writerow({
                    'date': summary.get('date', ''),
                    'name': contact.get('name', ''),
                    'company': contact.get('company', ''),
                    'phone': contact.get('phone', ''),
                    'email': contact.get('email', ''),
                    'preferred_contact': contact.get('preferred_contact', ''),
                    'outcome': details.get('outcome', ''),
                    'follow_up_required': details.get('follow_up_required', False)
                })
        
        return output_file


class LeadQualifier:
    """Handles lead qualification logic"""
    
    def __init__(self, qualification_criteria: Dict):
        self.criteria = qualification_criteria
    
    def score_lead(self, responses: Dict[str, str]) -> Dict:
        """Score a lead based on their responses"""
        score = 0
        max_score = 100
        
        # Basic scoring logic (can be customized)
        if responses.get("budget"):
            score += 25
        if responses.get("timeline"):
            score += 25
        if responses.get("business_type"):
            score += 25
        if responses.get("challenges"):
            score += 25
        
        priority = "high" if score >= 75 else "medium" if score >= 50 else "low"
        
        return {
            "score": score,
            "max_score": max_score,
            "priority": priority,
            "qualified": score >= 50
        }
    
    def get_qualification_questions(self) -> List[str]:
        """Get list of qualification questions"""
        return self.criteria.get("questions", [])


def format_call_summary_email(summary: Dict) -> str:
    """Format call summary as email text"""
    contact = summary.get('contact_info', {})
    details = summary.get('call_details', {})
    
    email_text = f"""
Call Summary - {summary.get('date', 'N/A')}

Contact Information:
- Name: {contact.get('name', 'N/A')}
- Company: {contact.get('company', 'N/A')}
- Phone: {contact.get('phone', 'N/A')}
- Email: {contact.get('email', 'N/A')}
- Preferred Contact: {contact.get('preferred_contact', 'N/A')}

Call Details:
- Topics Discussed: {', '.join(details.get('topics_discussed', []))}
- Outcome: {details.get('outcome', 'N/A')}
- Follow-up Required: {'Yes' if details.get('follow_up_required') else 'No'}
- Notes: {details.get('notes', 'N/A')}

---
Generated by Voice Agent Receptionist
"""
    return email_text.strip()
