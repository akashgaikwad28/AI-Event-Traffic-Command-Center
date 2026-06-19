from pathlib import Path

tests_dir = Path("tests")

structure = {
    "unit/ai": [
        "test_feature_pipeline.py",
        "test_time_features.py",
        "test_geo_features.py",
        "test_traffic_features.py",
        "test_encoders.py",
        "test_model_loader.py",
        "test_prediction_engine.py",
        "test_confidence_engine.py",
        "test_gori_engine.py",
    ],
    "unit/analytics": [
        "test_congestion_analytics.py",
        "test_response_time_analytics.py",
        "test_incident_patterns.py",
        "test_geo_analytics.py",
        "test_operational_kpis.py",
        "test_trend_analysis.py",
        "test_analytics_engine.py",
    ],
    "unit/resource_optimization": [
        "test_police_allocator.py",
        "test_barricade_optimizer.py",
        "test_diversion_engine.py",
        "test_deployment_planner.py",
        "test_resource_engine.py",
    ],
    "unit/stream": [
        "test_websocket_manager.py",
        "test_event_broadcaster.py",
        "test_stream_engine.py",
        "test_alert_dispatcher.py",
        "test_ingestion_simulator.py",
    ],
    "unit/genai": [
        "test_provider_router.py",
        "test_context_builder.py",
        "test_prompt_guard.py",
        "test_hallucination_guard.py",
        "test_output_validator.py",
        "test_summary_service.py",
        "test_report_service.py",
        "test_alert_service.py",
        "test_copilot_service.py",
    ],
    "unit/simulation": [
        "test_simulation_engine.py",
        "test_congestion_spread_simulator.py",
        "test_intervention_simulator.py",
        "test_impact_estimator.py",
        "test_scenario_builder.py",
    ],
    "unit/observability": [
        "test_structured_logger.py",
        "test_metrics_registry.py",
        "test_failure_tracker.py",
        "test_health_monitor.py",
        "test_request_timing.py",
    ],
    "integration": [
        "test_ai_pipeline.py",
        "test_analytics_pipeline.py",
        "test_optimization_pipeline.py",
        "test_simulation_pipeline.py",
        "test_streaming_pipeline.py",
        "test_genai_pipeline.py",
    ],
    "integration/api": [
        "test_predictions_api.py",
        "test_analytics_api.py",
        "test_optimization_api.py",
        "test_simulation_api.py",
        "test_genai_api.py",
        "test_stream_api.py",
        "test_observability_api.py",
    ],
    "e2e": ["test_executive_demo.py", "test_command_center_flow.py"],
    "performance": [
        "test_model_latency.py",
        "test_api_latency.py",
        "test_stream_performance.py",
    ],
    "fixtures": [
        "sample_incident.json",
        "sample_prediction.json",
        "sample_simulation.json",
        "sample_gori.json",
        "sample_analytics.json",
        "sample_report.json",
    ],
    "mocks": [
        "mock_gemini.py",
        "mock_groq.py",
        "mock_models.py",
        "mock_stream.py",
        "mock_analytics.py",
    ],
}

boilerplate_test = '''import pytest

@pytest.mark.asyncio
async def test_placeholder():
    """Auto-generated placeholder test. To be filled during testing iterations."""
    assert True
'''

boilerplate_json = '{\n  "status": "sample"\n}'
boilerplate_mock = "# Mock implementation placeholder\n\nclass MockHelper:\n    pass\n"

for d, files in structure.items():
    dir_path = tests_dir / d
    dir_path.mkdir(parents=True, exist_ok=True)

    for file in files:
        file_path = dir_path / file
        if not file_path.exists():
            with open(file_path, "w") as f:
                if file.endswith(".py"):
                    if "mocks/" in d:
                        f.write(boilerplate_mock)
                    else:
                        f.write(boilerplate_test)
                elif file.endswith(".json"):
                    f.write(boilerplate_json)

print("Scaffolding complete.")
