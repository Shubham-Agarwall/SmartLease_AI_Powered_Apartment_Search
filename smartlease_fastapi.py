from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import subprocess
import os
import json

# Initialize FastAPI app
app = FastAPI(title="SmartLease FastAPI", description="API for SmartLease Property Search System")

# Path to the temporary JSON files
OUTPUT_FOLDER = "temp_data_store_json"
FINAL_OUTPUT_FILE = os.path.join(OUTPUT_FOLDER, "properties_with_distances.json")


# Request model for the user query
class UserQuery(BaseModel):
    user_query: str


@app.get("/health", tags=["Health Check"])
def health_check():

    return {"status": "running", "message": "SmartLease API is operational."}


@app.post("/search", tags=["Search"])
def search_properties(user_query: UserQuery):

    try:
        # Ensure temp_data_store_json folder exists
        if not os.path.exists(OUTPUT_FOLDER):
            os.makedirs(OUTPUT_FOLDER)

        # Run control_execution.py with the user query as an argument
        query = user_query.user_query
        process = subprocess.run(
            ["python3", "control_execution.py", query],
            capture_output=True,
            text=True
        )

        # Check if the control_execution script ran successfully
        if process.returncode != 0:
            raise HTTPException(status_code=500, detail=f"Error executing scripts: {process.stderr}")

        # Load the final output JSON
        if not os.path.exists(FINAL_OUTPUT_FILE):
            raise HTTPException(status_code=500, detail="Final output file not found.")

        with open(FINAL_OUTPUT_FILE, "r") as f:
            results = json.load(f)

        return {"status": "success", "data": results}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
