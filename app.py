from __future__ import annotations

from flask import Flask, jsonify, render_template, request

from backend.analysis import build_response
from backend.knowledge_base import get_knowledge_base
from backend.preprocessing import build_user_profile
from config import APP_NAME, MAX_RESULTS

app = Flask(__name__)
app.config['APP_NAME'] = APP_NAME
kb = get_knowledge_base()


@app.route('/', methods=['GET'])
def home():
    return render_template('home.html', app_name=APP_NAME)


@app.route('/form', methods=['GET'])
def index():
    return render_template('index.html', app_name=APP_NAME)


@app.route('/recommend', methods=['POST'])
def recommend():
    form = request.form
    profile = build_user_profile(
        concern=form.get('concern'),
        symptoms=form.get('symptoms'),
        season=form.get('season'),
        digestion_strength=form.get('digestion_strength'),
        meal_consistency=form.get('meal_consistency'),
        age=form.get('age'),
        gender=form.get('gender'),
        allergies=form.get('allergies'),
        medical_history=form.get('medical_history'),
        current_medications=form.get('current_medications'),
        stress_level=form.get('stress_level'),
        sleep_pattern=form.get('sleep_pattern'),
        physical_activity=form.get('physical_activity'),
        dietary_habits=form.get('dietary_habits'),
        available_ingredients=form.get('available_ingredients'),
        family_history=form.get('family_history'),
    )
    result = build_response(kb, profile, limit=MAX_RESULTS)
    return render_template('results.html', app_name=APP_NAME, **result)


@app.route('/api/recommend', methods=['POST'])
def api_recommend():
    payload = request.get_json(silent=True) or {}
    profile = build_user_profile(**payload)
    result = build_response(kb, profile, limit=int(payload.get('limit', MAX_RESULTS)))
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)
