import os
import subprocess

# Paths to scripts
SEMANTIC_SEARCH_SCRIPT = "semantic_search.py"
DISTANCE_AGENT_SCRIPT = "distance_agent.py"

# Directory for JSON storage
OUTPUT_DIR = "temp_data_store_json"
SEMANTIC_OUTPUT_FILE = os.path.join(OUTPUT_DIR, "semantic_search_output.json")
DISTANCE_OUTPUT_FILE = os.path.join(OUTPUT_DIR, "properties_with_distances.json")


def execute_script(script_path, args=None):

    try:
        command = ["python3", script_path]
        if args:
            command.extend(args)
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        print(result.stdout)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error executing {script_path}: {e.stderr}")
        raise


def run_pipeline(user_query):

    # Ensure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Step 1: Run Semantic Search Script
    print("Running Semantic Search...")
    try:
        execute_script(SEMANTIC_SEARCH_SCRIPT, args=[user_query])
    except Exception as e:
        print(f"Error running semantic search: {str(e)}")
        return

    # Check if semantic search output was created
    if not os.path.exists(SEMANTIC_OUTPUT_FILE):
        print("Semantic search output file not found. Aborting.")
        return

    # Step 2: Run Distance Agent Script
    print("Running Distance Calculation...")
    try:
        execute_script(DISTANCE_AGENT_SCRIPT)
    except Exception as e:
        print(f"Error running distance calculation: {str(e)}")
        return

    # Check if distance output file was created
    if not os.path.exists(DISTANCE_OUTPUT_FILE):
        print("Distance output file not found. Aborting.")
        return

    print("Pipeline executed successfully.")
    print(f"Final output saved to: {DISTANCE_OUTPUT_FILE}")


if __name__ == "__main__":
    # Example input, replace with FastAPI integration
    user_query = "Looking for a property with rent: $5,000, 4 bedrooms, 3 bathrooms, at 123 Main St, Boston, MA"
    run_pipeline(user_query)
