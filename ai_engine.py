import random
from datetime import datetime, timedelta

def get_bed_occupancy_prediction():
    """Simulates predicting ICU and General bed occupancy."""
    base_icu = random.randint(70, 95)
    base_general = random.randint(60, 85)
    return {
        "icu_current_occupancy": base_icu,
        "icu_predicted_next_48h": min(100, base_icu + random.randint(-10, 15)),
        "general_current_occupancy": base_general,
        "general_predicted_next_48h": min(100, base_general + random.randint(-5, 10))
    }

def get_medicine_demand_forecast():
    """Simulates forecasting demand for key medicines."""
    medicines = ["Antibiotics", "Painkillers", "Anesthetics", "IV Fluids", "Vaccines"]
    forecast = []
    for med in medicines:
        forecast.append({
            "name": med,
            "current_stock": random.randint(100, 1000),
            "predicted_demand_next_7d": random.randint(200, 800),
            "status": "Adequate" if random.random() > 0.3 else "Low Stock Warning"
        })
    return forecast

def detect_disease_outbreaks():
    """Simulates detecting localized disease outbreaks based on symptoms."""
    diseases = ["Influenza A", "COVID-19 Variant", "Dengue", "Gastroenteritis"]
    outbreaks = []
    for _ in range(random.randint(0, 2)):
        disease = random.choice(diseases)
        outbreaks.append({
            "disease": disease,
            "severity": random.choice(["Low", "Medium", "High"]),
            "cases_last_24h": random.randint(10, 50),
            "trend": "Increasing"
        })
    return outbreaks

def get_smart_queue_prediction():
    """Simulates wait time prediction in ER and OPD."""
    return {
        "emergency_room_wait_mins": random.randint(5, 45),
        "opd_average_wait_mins": random.randint(15, 120),
        "active_doctors_er": random.randint(3, 8),
        "active_doctors_opd": random.randint(10, 25)
    }

def process_chatbot_query(query):
    """A simple mock logic for the AI Symptom & Guidance Chatbot."""
    query = query.lower()

    # 0. Greetings
    if any(word in query for word in ["hello", "hi", "hey", "greetings", "good morning", "good evening"]):
        return "Hello! I am the NeuroMed AI Assistant. I can help you with symptom analysis, ICU bed status, medicine inventory, doctor schedules, emergency wait times, and disease outbreak alerts. How can I assist you today?"

    # 1. Symptom Analysis
    if "fever" in query or "headache" in query:
        return "Based on your symptoms, it could be a viral infection. Please monitor your temperature. If it exceeds 102F or lasts more than 2 days, consult a doctor immediately."
    elif "chest pain" in query or "heart" in query:
        return "URGENT: Chest pain can be a sign of a severe cardiovascular event. Please proceed to the Emergency Room immediately or call an ambulance."
    elif "cough" in query or "breathe" in query:
        return "Respiratory symptoms detected. If you are experiencing shortness of breath, seek emergency care. Otherwise, isolate and monitor."
        
    # 2. Appointment Booking
    elif "appointment" in query or "book" in query:
        return "I can help you book an appointment. Would you like to see a General Physician, Neurologist, or Cardiologist?"
        
    # 3. Hospital Wait Times & Queue
    elif "wait time" in query or "queue" in query or "er" in query or "emergency" in query:
        wait_times = get_smart_queue_prediction()
        return f"Currently, the ER wait time is approx {wait_times['emergency_room_wait_mins']} mins, and OPD wait time is {wait_times['opd_average_wait_mins']} mins."
        
    # 4. Hospital Inventory / Supplies
    elif "supply" in query or "medicine" in query or "stock" in query or "antibiotics" in query:
        return "Checking real-time inventory... Our predictive AI indicates adequate supply of core medicines, but Anesthetics may run low within 48 hours. Manage this in the Medicine Forecast module."
        
    # 5. Doctor / Staff Info
    elif "doctor" in query or "staff" in query or "on call" in query:
        return "Currently, Dr. Vance is on call in the ER. Dr. Chen is leading Neurology. You can view full staff performance in the Doctor Performance Matrix."
        
    # 6. ICU / Bed availability
    elif "icu" in query or "bed" in query or "admit" in query:
        beds = get_bed_occupancy_prediction()
        return f"Current ICU occupancy is at {beds['icu_current_occupancy']}%. General ward occupancy is {beds['general_current_occupancy']}%. We have beds available."
        
    # 7. Outbreaks
    elif "outbreak" in query or "virus" in query or "disease" in query:
        return "Scanning local health data... Minor localized cases of Influenza A detected. No severe outbreaks requiring quarantine at this moment."
        
    else:
        return "I am the NeuroMed AI. I can assist with symptom checking, live wait times, ICU occupancy, inventory forecasting, and staff information. How can I help you today?"
