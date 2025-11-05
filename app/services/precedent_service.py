import json
from pathlib import Path
from typing import List, Dict, Any

class PrecedentService:
    def __init__(self):
        self.precedents = self._load_precedents()
    
    def _load_precedents(self) -> List[Dict[str, Any]]:
        precedents_path = Path('data/precedents.json')
        with open(precedents_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def find_relevant_precedents(self, analysis: Any, max_results: int = 3) -> List[Dict[str, Any]]:
        relevant_precedents = []
        
        for precedent in self.precedents:
            score = self._calculate_relevance_score(precedent, analysis)
            if score > 0:
                precedent['relevance_score'] = score
                relevant_precedents.append(precedent)
        
        # Sort by relevance score and return top results
        relevant_precedents.sort(key=lambda x: x['relevance_score'], reverse=True)
        return relevant_precedents[:max_results]
    
    def _calculate_relevance_score(self, precedent: Dict[str, Any], analysis: Any) -> float:
        score = 0
        
        # Match incident types
        if precedent['incident_type'] in analysis.identified_issues:
            score += 3
        
        # Match severity
        if precedent['severity'] == analysis.severity:
            score += 2
        
        # Match jurisdiction
        if precedent['jurisdiction'] == analysis.jurisdiction:
            score += 2
        
        # Keyword matching in description
        description_keywords = set(analysis.description.lower().split())
        precedent_keywords = set(precedent['description'].lower().split())
        common_keywords = description_keywords.intersection(precedent_keywords)
        score += len(common_keywords) * 0.1
        
        return score
