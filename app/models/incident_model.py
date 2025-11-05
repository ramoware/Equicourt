from dataclasses import dataclass
from typing import List, Dict, Any
from datetime import datetime

@dataclass
class IncidentAnalysis:
    incident_id: str
    description: str
    incident_type: str
    severity: str
    jurisdiction: str
    identified_issues: List[str]
    recommended_actions: List[str]
    legal_basis: List[str]
    confidence_score: float
    timestamp: datetime
    risk_level: str
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'incident_id': self.incident_id,
            'description': self.description,
            'incident_type': self.incident_type,
            'severity': self.severity,
            'jurisdiction': self.jurisdiction,
            'identified_issues': self.identified_issues,
            'recommended_actions': self.recommended_actions,
            'legal_basis': self.legal_basis,
            'confidence_score': self.confidence_score,
            'timestamp': self.timestamp.isoformat(),
            'risk_level': self.risk_level
        }
