from flask import Flask, render_template, request, jsonify
from models import db, Patient, Doctor, Resource, Appointment
import ai_engine
import os
import csv
import io

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

@app.route('/data_upload')
def data_upload():
    return render_template('data_upload.html')

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

@app.route('/api/upload_data', methods=['POST'])
def upload_data():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file:
        try:
            # Read CSV file using standard csv module
            stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
            csv_input = csv.reader(stream)
            
            rows = list(csv_input)
            if not rows or len(rows) < 2:
                return jsonify({'error': 'No data found in the file to plot.'}), 400
                
            headers = rows[0]
            data_rows = rows[1:]
            
            # Find numeric columns
            numeric_cols_indices = []
            categorical_cols_indices = []
            
            for i in range(len(headers)):
                # Check first data row to determine type
                val = data_rows[0][i].strip() if len(data_rows[0]) > i else ""
                try:
                    float(val)
                    numeric_cols_indices.append(i)
                except ValueError:
                    categorical_cols_indices.append(i)
            
            if not numeric_cols_indices:
                return jsonify({'error': 'No numeric data found in the file to plot.'}), 400
                
            # If there's a string column, use the first one as labels, else use index
            if categorical_cols_indices:
                label_idx = categorical_cols_indices[0]
                labels = [row[label_idx] if len(row) > label_idx else "Unknown" for row in data_rows]
            else:
                labels = [str(i) for i in range(len(data_rows))]
                
            # Prepare datasets for all numeric columns (limit to first 3 for visual clarity)
            datasets = []
            for idx in numeric_cols_indices[:3]:
                col_data = []
                for row in data_rows:
                    val = row[idx] if len(row) > idx else 0
                    try:
                        col_data.append(float(val))
                    except ValueError:
                        col_data.append(0)
                        
                datasets.append({
                    'name': headers[idx],
                    'data': col_data
                })
                
            return jsonify({
                'success': True,
                'labels': labels,
                'datasets': datasets,
                'filename': file.filename
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
