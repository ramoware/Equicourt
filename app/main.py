from flask import Blueprint, render_template, request, jsonify
from app.services.incident_service import IncidentService
from app.services.precedent_service import PrecedentService

bp = Blueprint('main', __name__)
incident_service = IncidentService()
precedent_service = PrecedentService()

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/analyze', methods=['POST'])
def analyze_incident():
    try:
        incident_data = {
            'description': request.form.get('description', ''),
            'incident_type': request.form.get('incident_type', ''),
            'severity': request.form.get('severity', 'medium'),
            'jurisdiction': request.form.get('jurisdiction', '')
        }
        
        analysis = incident_service.analyze_incident(incident_data)
        precedents = precedent_service.find_relevant_precedents(analysis)
        
        return render_template('results.html', 
                             analysis=analysis, 
                             precedents=precedents)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/api/analyze', methods=['POST'])
def api_analyze():
    data = request.get_json()
    analysis = incident_service.analyze_incident(data)
    precedents = precedent_service.find_relevant_precedents(analysis)
    
    return jsonify({
        'analysis': analysis,
        'precedents': precedents
    })
