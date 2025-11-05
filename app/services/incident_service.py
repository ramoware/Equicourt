import uuid
from datetime import datetime
from app.models.incident_model import IncidentAnalysis
from app.models.nlp_processor import NLPProcessor

class IncidentService:
    def __init__(self):
        self.nlp_processor = NLPProcessor()
    
    def analyze_incident(self, incident_data: dict) -> IncidentAnalysis:
        description = incident_data.get('description', '')
        incident_type = incident_data.get('incident_type', '')
        severity = incident_data.get('severity', 'medium')
        jurisdiction = incident_data.get('jurisdiction', 'general')
        
        # Extract legal issues using NLP
        identified_issues = self.nlp_processor.extract_legal_issues(description)
        
        # If no specific type provided, infer from issues
        if not incident_type and identified_issues:
            incident_type = identified_issues[0]
        
        # Generate recommendations
        recommended_actions = self.nlp_processor.generate_recommendations(
            identified_issues, jurisdiction
        )
        
        # Calculate risk level
        risk_level = self.nlp_processor.calculate_risk_level(identified_issues, severity)
        
        # Generate legal basis
        legal_basis = self._generate_legal_basis(identified_issues, jurisdiction)
        
        # Calculate confidence score (simplified)
        confidence_score = min(0.95, len(identified_issues) * 0.2 + 0.3)
        
        return IncidentAnalysis(
            incident_id=str(uuid.uuid4())[:8],
            description=description,
            incident_type=incident_type,
            severity=severity,
            jurisdiction=jurisdiction,
            identified_issues=identified_issues,
            recommended_actions=recommended_actions,
            legal_basis=legal_basis,
            confidence_score=confidence_score,
            timestamp=datetime.now(),
            risk_level=risk_level
        )
    
    def _generate_legal_basis(self, issues: list, jurisdiction: str) -> list:
        legal_basis = []
        
        legal_frameworks = {
            'data_breach': ["GDPR Article 33", "CCPA Section 1798.82", "Data Protection Act 2018"],
            'privacy_violation': ["GDPR Articles 5-7", "ePrivacy Directive", "Constitutional Privacy Rights"],
            'cyber_attack': ["Computer Fraud and Abuse Act", "NIS Directive", "Cybercrime Convention"],
            'unauthorized_access': ["Computer Misuse Act", "CFAA Section 1030", "Unauthorized Access Laws"]
        }
        
        for issue in issues:
            if issue in legal_frameworks:
                legal_basis.extend(legal_frameworks[issue])
        
        return list(set(legal_basis))
