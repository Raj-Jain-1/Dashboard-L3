# AI Smart Hospital Analytics Platform

This plan outlines the architecture and implementation strategy for the highly advanced AI Smart Hospital Analytics Platform. The application will be a full-stack platform featuring a premium, futuristic "cyberpunk" design with glassmorphism, advanced animations, and holographic UI elements.

## User Review Required

> [!IMPORTANT]
> **Tech Stack Selection**: I propose using **Flask** (Python) for the backend, **SQLite** (via SQLAlchemy) for the database, and **Vanilla HTML/CSS/JS** with a library like **Chart.js or ECharts** for the frontend. While Streamlit is an option, it is very rigid regarding custom CSS, animations, and complex UI layouts. Flask will give us the maximum control needed to create the ultra-modern, interactive, glassmorphism-heavy cyberpunk dashboard you requested. Please confirm if this approach works for you!
> 
> **Mock ML Models**: For the AI features (predictive analytics, disease outbreak, demand forecasting), I plan to implement mock Python machine learning models (e.g., using scikit-learn or basic statistical algorithms with dummy data) to demonstrate the functionality. Is this acceptable for the initial build?

## Open Questions

> [!WARNING]
> 1. Do you have a specific color palette in mind for the "cyberpunk" theme (e.g., neon blue and purple, or toxic green and dark grey)? By default, I will go with a deep dark background (#0a0a12) with neon cyan, bright magenta, and electric purple accents.
> 2. Should the initial data be populated with a mock dataset for patients, doctors, and resources?

## Proposed Changes

We will create a structured Flask project in `e:\Projects\Web\Task Level 3`.

### Backend (Python/Flask)

#### [NEW] `app.py`
The main Flask application entry point. It will handle routing, initialize the database, and serve API endpoints for the dashboard data and chatbot.

#### [NEW] `models.py`
SQLAlchemy database models for Patients, Doctors, ICU Beds, Appointments, and System Resources.

#### [NEW] `ai_engine.py`
A module containing Python classes/functions to simulate the AI insights:
- `predict_bed_occupancy()`
- `forecast_medicine_demand()`
- `detect_outbreaks()`
- `chatbot_response()`

#### [NEW] `requirements.txt`
Dependencies: `Flask`, `Flask-SQLAlchemy`, `pandas`, `scikit-learn`, `numpy`.

---

### Frontend (HTML/Templates)

#### [NEW] `templates/base.html`
The master layout containing the sidebar, top navigation, and AI voice assistant/chatbot toggle. Includes the core cyberpunk aesthetic structure.

#### [NEW] `templates/dashboard.html`
The main real-time monitoring dashboard with live KPI cards, interactive charts, and heatmaps.

#### [NEW] `templates/analytics.html`
Dedicated page for deeper predictive analytics, doctor performance, and resource optimization.

#### [NEW] `templates/data_upload.html`
A dedicated page for uploading raw data (CSV) and automatically generating beautiful, interactive charts (via ECharts) matching the cyberpunk theme.

#### [NEW] `templates/login.html`
A futuristic authentication page with glowing inputs and a holographic login card.

---

### Static Assets (CSS/JS)

#### [NEW] `static/css/style.css`
The core styling file. It will contain:
- CSS variables for neon colors and dark mode backgrounds.
- Glassmorphism utility classes (blur, translucent backgrounds, glowing borders).
- Keyframe animations for holographic effects, pulsing notifications, and smooth transitions.

#### [NEW] `static/js/main.js`
Global JavaScript for sidebar toggling, UI interactions, and managing the AI chatbot widget.

#### [NEW] `static/js/charts.js`
Logic for rendering and updating the real-time graphs and heatmaps (using a library like ECharts or Chart.js) by fetching data from the Flask API.

## Verification Plan

### Automated Tests
- Run `python app.py` to ensure the Flask server starts without errors.
- Verify API endpoints return valid JSON data for the charts and AI predictions.

### Manual Verification
- Navigate through all pages (Login -> Dashboard -> Analytics) in the browser to ensure routing works.
- Visually inspect the UI to ensure the cyberpunk theme, glassmorphism, and animations meet the "ultra-modern" standard.
- Test the interactive charts and ensure they display mock data correctly.
- Test the AI chatbot interface for symptom guidance.
