from flask import Flask, jsonify
from flask_cors import CORS
import json
from collections import Counter
import os

app = Flask(__name__)
CORS(app)
def load_data():
    data_path = os.path.join(os.path.dirname(__file__), 'data.json')
    with open(data_path, 'r', encoding='utf-8') as f:
        return json.load(f).get('vacancies', [])

@app.route('/api/stats')
def get_stats():
    vacancies = load_data()
    
    skills = Counter()
    experience = Counter()
    schedule = Counter()
    
    for vac in vacancies:
        skills.update(vac.get('skills', []))
        experience[vac.get('experience', 'Не указан')] += 1
        schedule[vac.get('schedule', 'Не указан')] += 1
    
    return jsonify({
        'skills': dict(skills.most_common(10)),
        'experience': dict(experience),
        'schedule': dict(schedule),
        'total': len(vacancies)
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)