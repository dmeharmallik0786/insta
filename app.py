import os
from flask import Flask, request, jsonify, render_template
from apify_client import ApifyClient

# --- Flask App Initialization ---
app = Flask(__name__)

# --- Configuration ---
# Your API token has been inserted here.
APIFY_API_TOKEN = "apify_api_YBX5K09CWQfvhooK3A213M0Y0svZaV0mtxJo"
ACTOR_ID = "apify/instagram-hashtag-scraper"

# --- Backend Routes ---
@app.route('/')
def index():
    """ This route serves the main HTML page. """
    return render_template('index.html')

@app.route('/scrape')
def scrape():
    """ This is the API endpoint that the webpage will call to start the scraper. """
    print("LOG: Scrape endpoint was hit.")
    
    # Critical Check: Ensure the API token is available.
    if not APIFY_API_TOKEN:
        print("ERROR: APIFY_API_TOKEN is missing from the code.")
        return "Server configuration error: Apify API token is missing.", 500

    # Get parameters from the request URL.
    hashtag = request.args.get('hashtag')
    count = request.args.get('count', default=10, type=int)

    if not hashtag:
        print("ERROR: Request is missing the 'hashtag' parameter.")
        return "Error: Hashtag parameter is required.", 400

    print(f"LOG: Starting scrape for #{hashtag} (Count: {count})...")
    
    try:
        client = ApifyClient(APIFY_API_TOKEN)
        run_input = {"hashtags": [hashtag], "resultsLimit": count}

        # Run the Apify Actor and wait for it to finish.
        run = client.actor(ACTOR_ID).call(run_input=run_input)
        
        # Fetch the results from the actor's dataset.
        dataset_items = client.dataset(run["defaultDatasetId"]).list_items().items
        
        print(f"SUCCESS: Found {len(dataset_items)} items. Sending to webpage.")
        return jsonify(dataset_items)

    except Exception as e:
        print(f"CRITICAL ERROR during scraping: {e}")
        return f"An error occurred on the server: {e}", 500

# --- Run the App ---
if __name__ == '__main__':
    print("--- Flask Server Starting ---")
    print("TOKEN: API token is hardcoded in the script.")
    print("-> Open http://127.0.0.1:5000 in your browser.")
    app.run(debug=True)