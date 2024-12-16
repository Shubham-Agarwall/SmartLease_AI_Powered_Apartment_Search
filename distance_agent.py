import json
import googlemaps

# Google Maps API Key
API_KEY = "removed"  # Replace with your Google Maps API key
gmaps = googlemaps.Client(key=API_KEY)

def calculate_distance(origin, destination):
    
    try:
        # Call the Google Maps Distance API 
        response = gmaps.distance_matrix(
            origins=origin,
            destinations=destination,
            mode="driving",
            units="imperial"
        )
        distance_info = response["rows"][0]["elements"][0]

        if distance_info["status"] == "OK":
            return distance_info["distance"]["text"] 
        else:
            return "Distance not available"
    except Exception as e:
        print(f"Error calculating distance between {origin} and {destination}: {e}")
        return "Error"
#adding distance
def add_distances_to_properties():
    """
    Load properties from a JSON file, calculate driving distances, and save the updated properties back to a file.
    """
    # Input and output file paths
    input_file = "temp_data_store_json/semantic_search_output.json"
    output_file = "temp_data_store_json/properties_with_distances.json"

    try:
        # Loading properties from the input file
        with open(input_file, "r") as f:
            properties = json.load(f)
    except FileNotFoundError:
        print(f"Input file '{input_file}' not found. Ensure the semantic search script has run successfully.")
        return
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from file '{input_file}': {e}")
        return
#for property
    for property in properties:
            # Extract origin (user-supplied address) and destination (property address)
        origin = property.get("user_supplied_address", "Unknown Address")
        destination = property["metadata"].get("property_address", "Unknown Address")

        if origin == "Unknown Address" or destination == "Unknown Address":
            print(f"Skipping property {property.get('property_id', 'Unknown ID')} due to missing addresses.")
            property["metadata"]["distance"] = "Address not available"
            continue

            # Calculate distance and add metadata
        distance = calculate_distance(origin, destination)
        property["metadata"]["distance"] = distance

    try:
        # Save the updated properties back to output file
        with open(output_file, "w") as f:
            json.dump(properties, f, indent=2)
        print(f"Updated properties with distances saved to {output_file}")
    except Exception as e:
        print(f"Error saving to file '{output_file}': {e}")

if __name__ == "__main__":
    add_distances_to_properties()
