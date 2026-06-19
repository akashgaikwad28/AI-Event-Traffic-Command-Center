# System Capabilities

GridWise AI is not a dashboard; it is a deployable AI-powered traffic operations platform. It features several core capabilities designed specifically for command center use.

## 1. Congestion Forecasting
Using historical incident data, the Prediction Engine forecasts how quickly congestion will spread (velocity) and its ultimate impact radius (GORI score).

## 2. Hotspot Reconstruction
Instead of relying on hardcoded map zones, GridWise dynamically reconstructs risk zones using DBSCAN clustering over historical incident coordinates, adapting to shifting city infrastructure.

## 3. Manpower Optimization
Recommends exact deployments of Police Officers, Patrol Vehicles, and Barricades based on minimizing the "Cost of Inaction" (e.g., secondary collisions and corridor spillover).

## 4. AI Copilot Explanations
Utilizes LLM orchestration to explicitly justify *why* a specific operational plan was chosen, fostering trust with dispatchers.

## 5. Post-Event Learning
Tracks prediction accuracy after an event concludes. Evaluates the Return on Investment (ROI) of deployed officers and triggers model retraining if traffic patterns drift.

## 6. Real-Time Replay Simulation
Ingests large-scale traffic events and plays them back in real-time over WebSocket streams to evaluate how effectively the AI responds under stress (e.g., Stadium Egress).
