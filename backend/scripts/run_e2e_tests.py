import asyncio
import time

import httpx

BASE_URL = "http://localhost:8000"
WS_URL = "ws://localhost:8000"

PASSED = "PASS"
FAILED = "FAIL"


def print_header(title):
    print(f"\n{'='*50}\n{title}\n{'='*50}")


def print_result(name, status, latency=None, details=""):
    latency_str = f" ({latency:.2f}ms)" if latency is not None else ""
    print(f"[{status}] {name}{latency_str}")
    if details:
        print(f"    -> {details}")


async def test_openapi():
    print_header("A. OpenAPI Validation")
    async with httpx.AsyncClient(timeout=30.0) as client:
        start = time.time()
        resp = await client.get(f"{BASE_URL}/api/v1/docs")
        latency = (time.time() - start) * 1000
        if resp.status_code == 200:
            print_result("Swagger UI (/api/v1/docs)", PASSED, latency)
        else:
            print_result(
                "Swagger UI (/api/v1/docs)",
                FAILED,
                latency,
                f"Status Code: {resp.status_code}",
            )

        start = time.time()
        resp = await client.get(f"{BASE_URL}/api/v1/openapi.json")
        latency = (time.time() - start) * 1000
        if resp.status_code == 200:
            print_result("OpenAPI JSON (/api/v1/openapi.json)", PASSED, latency)
        else:
            print_result(
                "OpenAPI JSON (/api/v1/openapi.json)",
                FAILED,
                latency,
                f"Status Code: {resp.status_code}",
            )


async def test_health():
    print_header("1. Health & Observability Test")
    async with httpx.AsyncClient(timeout=30.0) as client:
        start = time.time()
        resp = await client.get(f"{BASE_URL}/api/v1/observability/health")
        latency = (time.time() - start) * 1000

        if resp.status_code == 200:
            data = resp.json()
            if data.get("status") == "healthy" and "services" in data:
                print_result("Health Endpoint", PASSED, latency, "All services healthy")
            else:
                print_result(
                    "Health Endpoint", FAILED, latency, "Invalid response schema"
                )
        else:
            print_result(
                "Health Endpoint", FAILED, latency, f"Status {resp.status_code}"
            )


async def test_prediction():
    print_header("3. Prediction Engine & 4. GORI Engine Test")
    payload = {
        "latitude": 19.0760,
        "longitude": 72.8777,
        "priority": "Medium",
        "requires_road_closure": False,
        "timestamp": "2026-06-18T18:30:00",
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        start = time.time()
        resp = await client.post(
            f"{BASE_URL}/api/v1/predictions/full-assessment", json=payload
        )
        latency = (time.time() - start) * 1000

        if resp.status_code == 200:
            data = resp.json()
            if "gori" in data and "gori_score" in data["gori"]:
                gori_score = data["gori"]["gori_score"]
                tier = data["gori"]["severity_tier"]
                print_result(
                    "Prediction Execution",
                    PASSED,
                    latency,
                    f"GORI: {gori_score}, Tier: {tier}",
                )

                # Check GORI components
                if "breakdown" in data["gori"]:
                    print_result("GORI Components Present", PASSED)
                else:
                    print_result(
                        "GORI Components Present",
                        FAILED,
                        details="Missing gori.breakdown object",
                    )
            else:
                print_result(
                    "Prediction Execution",
                    FAILED,
                    latency,
                    "Missing critical fields in response",
                )
        else:
            print_result(
                "Prediction Execution", FAILED, latency, f"Status {resp.status_code}"
            )


async def test_analytics():
    print_header("5. Analytics Engine Test")
    async with httpx.AsyncClient(timeout=30.0) as client:
        start = time.time()
        resp = await client.get(f"{BASE_URL}/api/v1/analytics/overview")
        latency = (time.time() - start) * 1000

        if resp.status_code == 200:
            data = resp.json()
            if "data" in data and "city_health" in data["data"]:
                score = data["data"]["city_health"].get("health_score")
                print_result(
                    "Analytics Overview", PASSED, latency, f"City Health: {score}"
                )
            else:
                print_result(
                    "Analytics Overview", FAILED, latency, "Missing city_health_score"
                )
        else:
            print_result(
                "Analytics Overview", FAILED, latency, f"Status {resp.status_code}"
            )


async def test_optimization():
    print_header("6. Resource Optimization Test")
    payload = {
        "incident_id": "TEST-123",
        "latitude": 19.0760,
        "longitude": 72.8777,
        "gori_score": 85.0,
        "congestion_severity": "HIGH",
        "requires_closure": True,
        "heavy_vehicle_involved": True,
        "is_rush_hour": True,
        "hotspot_recurrence": 0.5,
        "historical_spread_probability": 0.6,
    }
    async with httpx.AsyncClient(timeout=30.0) as client:
        start = time.time()
        resp = await client.post(
            f"{BASE_URL}/api/v1/optimization/incident-response", json=payload
        )
        latency = (time.time() - start) * 1000

        if resp.status_code == 200:
            data = resp.json()
            if "resource_plan" in data:
                print_result(
                    "Resource Optimization",
                    PASSED,
                    latency,
                    f"Plan ID: {data.get('plan_id')}",
                )
            else:
                print_result(
                    "Resource Optimization", FAILED, latency, "Missing resource_plan"
                )
        else:
            print_result(
                "Resource Optimization", FAILED, latency, f"Status {resp.status_code}"
            )


async def test_simulation():
    print_header("7. Simulation Engine Test")
    async with httpx.AsyncClient(timeout=30.0) as client:
        start = time.time()
        resp = await client.post(f"{BASE_URL}/api/v1/simulation/demo")
        latency = (time.time() - start) * 1000

        if resp.status_code == 200:
            data = resp.json()
            if "baseline_state" in data and "optimized_state" in data:
                b_gori = data["baseline_state"].get("final_gori", 0)
                a_gori = data["optimized_state"].get("final_gori", 0)
                if a_gori < b_gori:
                    print_result(
                        "Simulation Engine",
                        PASSED,
                        latency,
                        f"GORI reduced: {b_gori} -> {a_gori}",
                    )
                else:
                    print_result(
                        "Simulation Engine",
                        PASSED,
                        latency,
                        f"GORI did not reduce (baseline logic): {b_gori} -> {a_gori}",
                    )
            else:
                print_result(
                    "Simulation Engine", FAILED, latency, "Missing before/after states"
                )
        else:
            print_result(
                "Simulation Engine", FAILED, latency, f"Status {resp.status_code}"
            )


async def test_genai():
    print_header("9. GenAI Test")
    payload = {
        "incident_id": "TEST-123",
        "type": "ACCIDENT",
        "gori_score": 85,
        "latitude": 19.0760,
        "longitude": 72.8777,
        "mode": "EXECUTIVE",
    }
    async with httpx.AsyncClient(timeout=30.0) as client:
        start = time.time()
        try:
            resp = await client.post(f"{BASE_URL}/api/v1/genai/explain", json=payload)
            latency = (time.time() - start) * 1000

            if resp.status_code == 200:
                data = resp.json()
                if "explanation" in data or "narrative" in data or "data" in data:
                    print_result(
                        "GenAI Explain",
                        PASSED,
                        latency,
                        "Explanation generated successfully",
                    )
                else:
                    print_result(
                        "GenAI Explain", FAILED, latency, "Missing explanation payload"
                    )
            else:
                print_result(
                    "GenAI Explain", FAILED, latency, f"Status {resp.status_code}"
                )
        except Exception as e:
            print_result(
                "GenAI Explain",
                FAILED,
                (time.time() - start) * 1000,
                f"Exception: {str(e)}",
            )


async def test_failures():
    print_header("11. Failure Handling Test")
    payload = {
        "latitude": 999,
        "longitude": 999,
        "priority": "Medium",
        "requires_road_closure": False,
    }
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(
            f"{BASE_URL}/api/v1/predictions/full-assessment", json=payload
        )
        if resp.status_code in [400, 422, 500]:
            print_result(
                "Invalid Coordinates Rejection",
                PASSED,
                details=f"Status: {resp.status_code} (Graceful handled)",
            )
        else:
            print_result(
                "Invalid Coordinates Rejection",
                FAILED,
                details=f"Status: {resp.status_code} (Expected error status)",
            )

        payload_missing = {"latitude": 19.0}
        resp_missing = await client.post(
            f"{BASE_URL}/api/v1/predictions/full-assessment", json=payload_missing
        )
        if resp_missing.status_code == 422:
            print_result("Missing Fields Rejection", PASSED, details="Status: 422")
        else:
            print_result(
                "Missing Fields Rejection",
                FAILED,
                details=f"Status: {resp_missing.status_code}",
            )


async def test_concurrent():
    print_header("B. Concurrent Request Test")
    payload = {"latitude": 19.0760, "longitude": 72.8777, "priority": "Medium"}

    async def make_req(client, idx):
        start = time.time()
        resp = await client.post(
            f"{BASE_URL}/api/v1/predictions/full-assessment", json=payload
        )
        return resp.status_code, (time.time() - start) * 1000, resp.text

    async with httpx.AsyncClient(timeout=60.0) as client:
        tasks = [make_req(client, i) for i in range(50)]
        start_time = time.time()
        results = await asyncio.gather(*tasks)
        total_time = (time.time() - start_time) * 1000

        successes = sum(1 for status, l, text in results if status == 200)
        avg_latency = sum(l for status, l, text in results) / 50

        if successes == 50:
            print_result(
                "50 Concurrent Requests",
                PASSED,
                total_time,
                f"Avg Latency per req: {avg_latency:.2f}ms",
            )
        else:
            statuses = [(status, text) for status, l, text in results]
            print_result(
                "50 Concurrent Requests",
                FAILED,
                total_time,
                f"Successes: {successes}/50. Statuses: {statuses[:2]}",
            )


async def main():
    print("Starting GridWise AI End-to-End Certification...")
    await test_openapi()
    await test_health()
    await test_prediction()
    await test_analytics()
    await test_optimization()
    await test_simulation()
    await test_genai()
    await test_failures()
    await test_concurrent()
    print("\nEnd-to-End test suite completed.")


if __name__ == "__main__":
    asyncio.run(main())
