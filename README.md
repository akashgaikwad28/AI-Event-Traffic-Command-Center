# 🌐 GridWise AI: Traffic Operations Command Center

![Status](https://img.shields.io/badge/Status-Production%20Ready-success)
![Version](https://img.shields.io/badge/Version-1.0.0-blue)
![Python](https://img.shields.io/badge/Backend-Python%20%7C%20FastAPI-3776AB?logo=python&logoColor=white)
![React](https://img.shields.io/badge/Frontend-React%20%7C%20TypeScript-61DAFB?logo=react&logoColor=black)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)

**GridWise AI** is an open-source, enterprise-grade, real-time AI Traffic Operations Command Center.

Moving beyond traditional dashboards and ML notebooks, GridWise AI is a complete operational intelligence platform. It ingests live event metadata, runs multi-model inference pipelines to calculate cascading congestion risks, and utilizes Generative AI to recommend dynamic manpower deployments, barricading strategies, and optimal diversion plans.

---

## 🎯 Executive Summary & Problem Solved

GridWise AI forecasts event-related traffic impact and recommends optimal manpower, barricading, and diversion plans using historical and real-time intelligence.

It solves this through the **GORI (GridWise Operational Risk Index)** Engine. By assessing precise geographic coordinates, event severity, rush-hour status, and vehicle counts, the system actively simulates congestion spreads and provides immediate, actionable mitigation plans to city planners, dispatchers, and executive leadership.

---

## ✨ Key Features

- **🔴 Real-Time GORI Scoring**: Computes complex risk tiers dynamically based on Congestion Risk, Hotspot Severity, Deployment Pressure, Cascading Spread, and Rush-Hour Stress.
- **👮 Resource Optimization Engine**: Calculates the exact number of officers required, ideal deployment zones, and barricade requirements.
- **🗺️ Simulation Engine (What-If Scenarios)**: Proves mitigation impact by modeling traffic spread *before* and *after* GridWise interventions.
- **🤖 Tactical AI Copilot**: Translates raw predictive data into audience-specific narratives (`EXECUTIVE`, `DISPATCHER`, `ANALYST`) using real-time generative AI.
- **📊 Intelligence Reporting**: Generates downloadable PDF/Markdown executive shift handovers and daily operational summaries.
- **⚡ Real-Time Streaming**: High-throughput WebSocket architecture ensuring sub-100ms latency for live alerts and UI updates.

---

## 🏗️ Architecture & Technology Stack

### **Backend Stack**
- **Framework**: FastAPI (Python)
- **AI/ML**: Scikit-Learn, XGBoost, Pandas, Numpy, Joblib
- **Generative AI**: Groq / Gemini via LangChain
- **Real-time**: FastAPI WebSockets

### **Frontend Stack**
- **Framework**: React 18, TypeScript, Vite
- **State Management**: Zustand
- **Styling**: TailwindCSS
- **Data Visualization**: ECharts, Leaflet

---

## 🚀 Getting Started

### Prerequisites
- Node.js (v18+)
- Python (3.10+)

### 1. Backend Setup

1. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Fetch data and model artifacts using DVC (if applicable):
   ```bash
   dvc pull
   ```
4. Start the server:
   ```bash
   python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

### 2. Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install dependencies & run:
   ```bash
   npm install
   npm run dev
   ```

---

## 🤝 Contributing to GridWise AI

GridWise AI is an open-source project and we welcome contributions! 

Please refer to the following documents for more details:
- [Contributing Guidelines](CONTRIBUTING.md)
- [Code of Conduct](CODE_OF_CONDUCT.md)
- [Project Structure](docs/PROJECT_STRUCTURE.md)
- [Development Guidelines](docs/DEVELOPMENT_GUIDELINES.md)

---

## 📄 License

This project is licensed under the MIT License.
