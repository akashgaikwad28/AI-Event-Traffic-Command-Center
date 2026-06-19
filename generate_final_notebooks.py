import nbformat as nbf

def create_notebook_15():
    nb = nbf.v4.new_notebook()
    nb.cells = [
        nbf.v4.new_markdown_cell("# ELITE KILLER DEMO\n## 15. Live Incident Simulation\n\nThis notebook demonstrates a live simulation of a high-severity incident triggering the GridWise Operational Risk Index (GORI) escalation protocol."),
        nbf.v4.new_markdown_cell("### Step 1 — Incident Appears\nA Heavy Truck breaks down near a major corridor during rush hour."),
        nbf.v4.new_code_cell("""import pandas as pd\nimport numpy as np\nimport time\n\nincident = {
    'id': 'INC-2026-X99',
    'type': 'Heavy Truck Breakdown',
    'latitude': 12.971598,
    'longitude': 77.594562,
    'priority': 'High',
    'requires_road_closure': True,
    'vehicle_type': 'Multi-Axle Truck',
    'hour': 17 # Rush Hour
}
print(f"🚨 LIVE INCIDENT DETECTED: {incident['id']} | Type: {incident['type']}")
print(f"Location: {incident['latitude']}, {incident['longitude']}")"""),
        nbf.v4.new_markdown_cell("### Step 2 — Spatial Intelligence Activates\nSystem dynamically reconstructs the operational geography using DBSCAN and evaluates historical pressure."),
        nbf.v4.new_code_cell("""# Simulate spatial coordinate-first intelligence
def spatial_intelligence(lat, lon):
    cluster_id = 4 # DBSCAN cluster mapped
    hotspot_severity = "Critical (Top 5% historically)"
    print(f"📍 MAPPED TO DBSCAN CLUSTER {cluster_id}")
    print(f"Historical Pressure: {hotspot_severity}")
    return cluster_id, 18 # returns component score

cluster, hotspot_score = spatial_intelligence(incident['latitude'], incident['longitude'])"""),
        nbf.v4.new_markdown_cell("### Step 3 — AI Prediction Layer Executes\nSimulating inference from LightGBM/XGBoost models for duration, deployment, and congestion."),
        nbf.v4.new_code_cell("""# Simulate Model Inference
predictions = {
    'congestion_severity': 'High Spread Risk',
    'clearance_duration_mins': 95,
    'deployment_load': 'Heavy Tow + 5 Officers',
    'cascading_spread_risk': '88% Probability of Secondary Incidents'
}
for k, v in predictions.items():
    print(f"🤖 {k.upper().replace('_', ' ')}: {v}")"""),
        nbf.v4.new_markdown_cell("### Step 4 — GORI Escalation\nGridWise Operational Risk Index synthesized from all predictive components."),
        nbf.v4.new_code_cell("""# GORI Component Breakdown
gori_components = {
    'Congestion Risk': 22,
    'Hotspot Severity': 18,
    'Rush Hour Stress': 14,
    'Cascading Spread': 20,
    'Deployment Pressure': 13
}
gori_score = sum(gori_components.values())

print(f"🔥 GORI SCORE SPIKED TO: {gori_score}")
print("--- GORI COMPONENT BREAKDOWN ---")
for comp, score in gori_components.items():
    print(f"{comp}: +{score}")"""),
        nbf.v4.new_markdown_cell("### Step 5 — Recommendation Engine\nSystem triggers human-readable operational actions."),
        nbf.v4.new_code_cell("""def trigger_recommendation(gori):
    print("⚡ AI DISPATCH RECOMMENDATIONS ⚡")
    print("1. IMMEDIATE DIVERSION on adjacent corridors.")
    print("2. DEPLOY HEAVY TOW UNIT.")
    print("3. ESCALATE 5 OFFICERS for traffic control.")

trigger_recommendation(gori_score)"""),
        nbf.v4.new_markdown_cell("### Step 6 — Dashboard Update\nLive rendering of the event on the operational map."),
        nbf.v4.new_code_cell("""import folium\nm = folium.Map(location=[incident['latitude'], incident['longitude']], zoom_start=15, tiles='CartoDB dark_matter')
folium.CircleMarker(
    location=[incident['latitude'], incident['longitude']],
    radius=15, color='red', fill=True, fill_color='red', fill_opacity=0.6,
    popup=f"GORI: {gori_score} | {incident['type']}"
).add_to(m)
# Simulate cascade spread zone
folium.Circle(
    location=[incident['latitude'], incident['longitude']],
    radius=800, color='orange', fill=True, fill_opacity=0.2, popup="Cascading Risk Zone"
).add_to(m)
m""")
    ]
    with open('notebooks/production/15_live_incident_simulation.ipynb', 'w', encoding='utf-8') as f:
        nbf.write(nb, f)
    print("Generated 15_live_incident_simulation.ipynb")

def create_notebook_16():
    nb = nbf.v4.new_notebook()
    nb.cells = [
        nbf.v4.new_markdown_cell("# 16. Advanced Model Failure Analysis\n\nAnalyzing robust prediction reliability, sparse geo regions, and outlier events."),
        nbf.v4.new_code_cell("""import pandas as pd\nimport numpy as np\nimport matplotlib.pyplot as plt\nimport seaborn as sns\n"""),
        nbf.v4.new_markdown_cell("### 1. Generating Prediction Reliability Score\nWe calculate a statistical trust score for every inference."),
        nbf.v4.new_code_cell("""# Simulate validation data with errors and reliability scores
np.random.seed(42)
df_fail = pd.DataFrame({
    'geo_cluster_id': np.random.choice([-1, 1, 2, 3], size=1000, p=[0.15, 0.4, 0.3, 0.15]),
    'vehicle_type': np.random.choice(['Car', 'Truck', 'Heavy Trailer', 'Unknown'], size=1000),
    'absolute_error_mins': np.random.exponential(scale=15, size=1000)
})

# Inject deliberate failures in sparse zones (-1) and rare vehicles
df_fail.loc[(df_fail['geo_cluster_id'] == -1), 'absolute_error_mins'] += 20
df_fail.loc[(df_fail['vehicle_type'] == 'Heavy Trailer'), 'absolute_error_mins'] += 25

# Model Trust Score calculation
# Higher error variance in similar historical segments = lower reliability
df_fail['prediction_reliability_score'] = 100 - (df_fail['absolute_error_mins'] / df_fail['absolute_error_mins'].max() * 100)
df_fail['prediction_reliability_score'] = df_fail['prediction_reliability_score'].clip(lower=0, upper=100)

print("Average Prediction Reliability by Geo Cluster:")
print(df_fail.groupby('geo_cluster_id')['prediction_reliability_score'].mean().round(1))"""),
        nbf.v4.new_markdown_cell("### 2. Identifying Blind Spots\nPlotting error rates by geography and heavy vehicle presence."),
        nbf.v4.new_code_cell("""plt.figure(figsize=(10,6))
sns.boxplot(data=df_fail, x='vehicle_type', y='prediction_reliability_score', hue='geo_cluster_id')
plt.title("Model Trust Score Breakdown")
plt.show()""")
    ]
    with open('notebooks/production/16_model_failure_analysis.ipynb', 'w', encoding='utf-8') as f:
        nbf.write(nb, f)
    print("Generated 16_model_failure_analysis.ipynb")

if __name__ == "__main__":
    create_notebook_15()
    create_notebook_16()
