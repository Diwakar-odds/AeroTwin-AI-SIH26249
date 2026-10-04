"""
AeroTwin AI: Military Aircraft Predictive Maintenance API
"""
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import datetime

app = FastAPI(
    title="AeroTwin AI Fleet Analytics Engine",
    description="Predictive Maintenance & Fleet Availability Platform for SIH26249 (DSSC / MoD)",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {
        "system": "AeroTwin AI",
        "ps_id": "SIH26249",
        "organization": "Defence Services Staff College (DSSC)",
        "ministry": "Ministry of Defence (MoD)",
        "fleet_availability": "88.5%",
        "status": "OPERATIONAL"
    }

@app.get("/api/v1/fleet")
def get_fleet_status():
    return {
        "total_aircraft": 42,
        "mission_ready": 38,
        "scheduled_service": 3,
        "grounded": 1,
        "fleet_availability_rate": 0.885,
        "squadron": "No. 20 Squadron (Lightnings) - Su-30MKI / Tejas LCA",
        "aircraft_inventory": [
            {"id": "SB-145", "type": "Su-30MKI", "health_index": 0.94, "status": "Mission Ready", "rul_cycles": 142},
            {"id": "RB-003", "type": "Rafale", "health_index": 0.89, "status": "Mission Ready", "rul_cycles": 118},
            {"id": "TJ-012", "type": "Tejas LCA", "health_index": 0.68, "status": "Attention Needed", "rul_cycles": 38},
            {"id": "SB-082", "type": "Su-30MKI", "health_index": 0.32, "status": "Grounded (HPC Wear)", "rul_cycles": 6}
        ]
    }

@app.get("/api/v1/aircraft/{aircraft_id}/telemetry")
def get_aircraft_telemetry(aircraft_id: str):
    return {
        "aircraft_id": aircraft_id,
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "subsystems": {
            "high_pressure_compressor": {"status": "Healthy", "temp_r": 1585.2, "health_score": 0.92},
            "low_pressure_turbine": {"status": "Attention", "egt_temp_r": 1410.8, "health_score": 0.74},
            "hydraulics": {"status": "Nominal", "pressure_psi": 3050.0, "health_score": 0.96},
            "avionics": {"status": "Nominal", "temp_c": 34.5, "health_score": 0.99}
        },
        "predicted_rul_cycles": 118,
        "maintenance_recommendation": "Perform borescope inspection of LPT stage 2 blades at next scheduled turnaround."
    }
