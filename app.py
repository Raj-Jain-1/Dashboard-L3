from flask import Flask, render_template, request, jsonify
from models import db, Patient, Doctor, Resource, Appointment
import ai_engine
import os

app = Flask(__name__)
app.secret_key = 'super_secure_cyber_key_2026'
# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hospital.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Create tables before first request if they don't exist
with app.app_context():
    db.create_all()

# ----------------- UI ROUTES -----------------

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'admin' and password == 'admin123':
            return render_template('dashboard.html')
        else:
            error = "Invalid Operator ID or Passcode."
    return render_template('login.html', error=error)

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/analytics')
def analytics():
    return render_template('analytics.html')

@app.route('/icu_occupancy')
def icu_occupancy():
    return render_template('icu_occupancy.html')

@app.route('/emergency_cases')
def emergency_cases():
    return render_template('emergency_cases.html')

@app.route('/doctor_performance')
def doctor_performance():
    return render_template('doctor_performance.html')

@app.route('/medicine_forecast')
def medicine_forecast():
    return render_template('medicine_forecast.html')

# ----------------- API ENDPOINTS -----------------

@app.route('/api/occupancy')
def get_occupancy():
    data = ai_engine.get_bed_occupancy_prediction()
    return jsonify(data)

@app.route('/api/medicine_forecast')
def get_medicine_forecast():
    data = ai_engine.get_medicine_demand_forecast()
    return jsonify(data)

@app.route('/api/outbreaks')
def get_outbreaks():
    data = ai_engine.detect_disease_outbreaks()
    return jsonify(data)

@app.route('/api/queue')
def get_queue():
    data = ai_engine.get_smart_queue_prediction()
    return jsonify(data)

@app.route('/api/chatbot', methods=['POST'])
def chatbot():
    req_data = request.get_json()
    query = req_data.get('query', '')
    response = ai_engine.process_chatbot_query(query)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
