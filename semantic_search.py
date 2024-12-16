import openai
import json
import re
from pinecone import Pinecone, ServerlessSpec
import sys  # To accept command-line arguments

# Initialize Pinecone and OpenAI
openai.api_key = ""
pc = Pinecone(api_key="")

# Ensure the index exists
index_name = "smartlease-pinecone-index"
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=1536,
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        )
    )

# Connect to the Pinecone index
index = pc.Index(index_name)

# Generate Query Embedding
def get_query_embedding(query):
    try:
        response = openai.Embedding.create(
            model="text-embedding-ada-002",
            input=query
        )
        return response['data'][0]['embedding']
    except Exception as e:
        print(f"Error generating embedding: {e}")
        raise

# Refine User Query with ChatGPT
def refine_user_query_with_chatgpt(user_query):
    system_message = (
        "You are a query assistant for a property search system. Refine the user's query for semantic search "
        "by restructuring it into a natural language description of the desired property. Keep the refinement concise."
    )
    user_message = f"Refine this query: {user_query}"
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ]
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print(f"Error refining user query: {e}")
        raise

# Refine Results with ChatGPT
def refine_results_with_chatgpt(refined_query, results, user_supplied_address):
    system_message = (
        "You are a property matching assistant. Based on the refined query and the search results, select all the matches "
        "and organize the data in a structured format. Ensure the output is JSON. "
        "Add a field called 'user_supplied_address' with the address provided in the query to each property in the results."
    )
    user_message = f"Refined Query: {refined_query}\nSearch Results: {json.dumps(results)}\nUser Supplied Address: {user_supplied_address}"

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ]
        )
        raw_content = response["choices"][0]["message"]["content"]
        cleaned_content = raw_content.strip("```").strip()
        return json.loads(cleaned_content)
    except Exception as e:
        print(f"Error refining results: {e}")
        raise

# Extract Address from User Query
def extract_user_supplied_address(user_query):
    address_pattern = r"\d{1,5}\s[\w\s]+(?:st|street|ave|avenue|road|rd|blvd|boulevard|ln|lane|way|dr|drive|court|ct)\b.*"
    match = re.search(address_pattern, user_query, re.IGNORECASE)
    return match.group(0).strip() if match else "Unknown Address"

# Search Properties
def search_properties(user_query, top_k=10):
    user_supplied_address = extract_user_supplied_address(user_query)

    # Refine query using ChatGPT
    refined_query = refine_user_query_with_chatgpt(user_query)
    print("Refined Query:", refined_query)
    print("User Supplied Address:", user_supplied_address)

    # Generate query embedding
    query_embedding = get_query_embedding(refined_query)

    # Perform semantic search
    response = index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True
    )

    if not response['matches']:
        print("No matches found in Pinecone. Please check the embeddings or refine the query.")
        return []

    # Relevant metadata fields to display
    relevant_metadata_fields = [
        "property_title",
        "property_address",
        "monthly_rent",
        "bedrooms",
        "bathrooms",
        "square_feet",
        "availability",
        "property_image_folder_s3_path",
    ]

    # Format results
    results = []
    for match in response['matches']:
        metadata = match['metadata']
        filtered_metadata = {key: metadata.get(key, "N/A") for key in relevant_metadata_fields}
        result = {
            "property_id": match['id'],
            "score": match['score'],
            "metadata": filtered_metadata
        }
        results.append(result)

    # Refine results with ChatGPT
    return refine_results_with_chatgpt(refined_query, results, user_supplied_address)

# Main Function
def main():
    # Accept user query as a command-line argument
    if len(sys.argv) < 2:
        print("Error: Please provide a user query as a command-line argument.")
        return

    user_query = sys.argv[1]

    try:
        final_results = search_properties(user_query)

        if not final_results:
            print("No results returned. Please refine your query.")
            return

        output_file = "temp_data_store_json/semantic_search_output.json"
        with open(output_file, "w") as f:
            json.dump(final_results, f, indent=2)
        print(f"Results saved to {output_file}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
