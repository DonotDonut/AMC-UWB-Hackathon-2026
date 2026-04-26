"""
CrowdCue: Event-Based Workforce Scheduling System 

This script performs the full data pipeline:

1. Extract store locations using Turbo Overpass API
2. Generate KML visualization
3. Extract event data from Ticketmaster in the seattle region 
4. Generate synthetic employee dataset
5. Estimate store capacity 
6. Add coordinates to events 
7. Run Eclat algorithm for scheduling suggestions
8. Validate results (statistics + train/test split)

Author: Timothy Caole 
Date: April 2026

Description:
This project implements an event driven workforce scheduling
system using the Eclat frequent pattern mining algorithm.

Note:
This code was developed with assistance from AI tools
for structuring, debugging, and optimization.
"""


# Importing Python Libraries
import os
import pandas as pd
import random
import matplotlib.pyplot as plt
from pathlib import Path

# Script / Python File connection
from backend.database_access.turbo_overpass import TurboOverpass
from backend.database_access.geographic_information_system import GIS
from backend.database_access.ticketmaster import TicketMaster
from backend.database_creation.employee import EmployeeGenerator
from backend.database_modificaiton.resturant_capacity import ResturantCapacityEstimator
from backend.database_modificaiton.event_coordinates import EventCoordinateMapper
from backend.machine_learning.eclat import EclatScheduleSuggestion
from backend.machine_learning.test import EclatTest

PROJECT_DIR = Path(__file__).resolve().parents[2]

# Global File Paths
DATA_DIR = PROJECT_DIR / "data"
OUTPUT_DIR = PROJECT_DIR / "output data"

ECLAT_OUTPUT_FILE = OUTPUT_DIR / "schedule_suggestions_eclat.xlsx"

# data use for the front end 
CURRENT_EMPLOYEE = DATA_DIR / "staff_data.xlsx"
CURRENT_STORES_FILE = DATA_DIR / "current_store_location.xlsx"
CURRENT_EVENTS_FILE = DATA_DIR / "current_events.xlsx"
RECOMMENDED_SCHEDULE_FILE = DATA_DIR / "recommended_staff_schedule.xlsx"


# Run Eclat + Validation
def run_eclat_model():
    suggestions_df, frequent_df, rules_df = EclatScheduleSuggestion.process(
        employee_file=CURRENT_EMPLOYEE,
        store_file=CURRENT_STORES_FILE,
        event_file=CURRENT_EVENTS_FILE,
        output_file=ECLAT_OUTPUT_FILE,
        radius_miles=1.0,
        min_support=75,
        min_confidence=0.75,
        min_lift=1.5,
        max_pattern_length=2,
        focus_maximal_patterns=False
    )

    final_schedule_df = suggestions_df[[
        "Employee",
        "Day",
        "Start Time",
        "End Time",
        "event_name",
        "venue",
        "crowd_rank",
        "store_name",
        "distance_to_event_miles",
        "Role",
    ]]

    final_schedule_df.to_excel(
        RECOMMENDED_SCHEDULE_FILE,
        sheet_name="Recommended Schedule",
        index=False
    )

    print(f"Recommended schedule saved to: {RECOMMENDED_SCHEDULE_FILE}")

    return {
        "suggestions": final_schedule_df.to_dict(orient="records"),
        "output_file": str(RECOMMENDED_SCHEDULE_FILE),
    }

# main
if __name__ == "__main__":
    random.seed(42)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    run_eclat_model()

    print("Pipeline completed successfully.")


