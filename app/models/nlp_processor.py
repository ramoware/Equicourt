import re
import json
from typing import List, Dict, Any
from pathlib import Path

class NLPProcessor:
    def __init__(self):
        self.legal_keywords = self._load_legal_keywords()
        self.patterns = self._initialize_patterns()
    
    def _load_legal_keywords(self) -> Dict[str, List[str]]:
        keywords_path = Path('data/legal_keywords.json')
        with open(keywords_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _initialize_patterns(self) -> Dict[str, re.Pattern]:
        return {
            'data_breach': re.compile(r'data.*breach|breach.*data|hack|leak', re.IGNORECASE),
            'privacy_violation': re.compile(r'privacy|gdpr|ccpa|personal.*data', re.IGNORECASE),
            'cyber_attack': re.compile(r'cyber.*attack|malware|ransomware|phishing', re.IGNORECASE),
            'unauthorized_access': re.compile(r'unauthorized.*access|access.*without|illegal.*entry', re.IGNORECASE),
            'intellectual_property': re.compile(r'copyright|patent|trademark|intellectual.*property', re.IGNORECASE)
        }
    
    def extract_legal_issues(self, text: str) -> List[str]:
        issues = []
        
        for issue_type, pattern in self.patterns.items():
            if pattern.search(text):
                issues.append(issue_type)
        
        # Check for legal keywords
        for category, keywords in self.legal_keywords.items():
            for keyword in keywords:
                if keyword.lower() in text.lower():
                    if category not in issues:
                        issues.append(category)
        
        return list(set(issues))
    
    def calculate_risk_level(self, issues: List[str], severity: str) -> str:
        risk_score = 0
        
        # Base score from issues
        risk_weights = {
            'data_breach': 3,
            'cyber_attack': 3,
            'privacy_violation': 2,
            'unauthorized_access': 2,
            'intellectual_property': 1
        }
        
        for issue in issues:
            risk_score += risk_weights.get(issue, 1)
        
        # Adjust by severity
        severity_weights = {'low': 0.5, 'medium': 1, 'high': 2}
        risk_score *= severity_weights.get(severity, 1)
        
        if risk_score >= 6:
            return 'High'
        elif risk_score >= 3:
            return 'Medium'
        else:
            return 'Low'
    
    def generate_recommendations(self, issues: List[str], jurisdiction: str) -> List[str]:
        recommendations = []
        
        action_map = {
            'data_breach': [
                "Immediately contain the breach",
                "Notify affected individuals and authorities",
                "Preserve evidence for investigation",
                "Conduct forensic analysis",
                "Review and update security measures"
            ],
            'privacy_violation': [
                "Conduct privacy impact assessment",
                "Review data processing activities",
                "Implement privacy by design",
                "Update privacy policies",
                "Train staff on privacy compliance"
            ],
            'cyber_attack': [
                "Isolate affected systems",
                "Activate incident response team",
                "Preserve logs and evidence",
                "Contact law enforcement if necessary",
                "Implement additional security controls"
            ],
            'unauthorized_access': [
                "Revoke unauthorized access immediately",
                "Conduct access rights review",
                "Implement multi-factor authentication",
                "Monitor for suspicious activities",
                "Update access control policies"
            ]
        }
        
        for issue in issues:
            if issue in action_map:
                recommendations.extend(action_map[issue])
        
        # Add jurisdiction-specific recommendations
        if jurisdiction.lower() == 'eu':
            recommendations.append("Ensure GDPR compliance in all actions")
        elif jurisdiction.lower() == 'us':
            recommendations.append("Review state-specific breach notification laws")
        
        return list(set(recommendations))  # Remove duplicates
