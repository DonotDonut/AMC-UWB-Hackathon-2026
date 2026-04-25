import random
import pandas as pd
import os
import random

class EmployeeGenerator:

    @staticmethod
    def generate_employee_sheet(
        input_store_file,
        output_file,
        positions,
        availability,
        schedules,
        people_per_store=7
    ):
        stores_df = pd.read_excel(input_store_file)

        non_manager_positions = [
            position for position in positions
            if position != "Store Manager"
        ]

        rows = []
        employee_id = 1

        for _, store in stores_df.iterrows():

            # Create exactly 1 manager per store
            rows.append({
                "Employee ID": employee_id,
                "OSM ID": store["osm_id"],
                "Store Name": store["name"],
                "Latitude": store["lat"],
                "Longitude": store["lon"],
                "Position": "Store Manager",
                "Staff Availability": "Full-time",
                "Current Work Schedule": random.choice(schedules),
            })
            employee_id += 1

            # Create remaining employees
            for _ in range(people_per_store - 1):
                rows.append({
                    "Employee ID": employee_id,
                    "OSM ID": store["osm_id"],
                    "Store Name": store["name"],
                    "Latitude": store["lat"],
                    "Longitude": store["lon"],
                    "Position": random.choice(non_manager_positions),
                    "Staff Availability": random.choice(availability),
                    "Current Work Schedule": random.choice(schedules),
                })
                employee_id += 1

        df = pd.DataFrame(rows)

        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        df.to_excel(output_file, index=False)

        print(f"Saved: {output_file}")
        print(f"Total Employees: {len(df)}")

        return df