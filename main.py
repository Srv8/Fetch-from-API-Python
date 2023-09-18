import requests
import pandas as pd
from datetime import datetime, timedelta

# Replace with the base URL of the API you want to fetch data from
base_api_url = "YOUR_API_URL"

# Define the date and time range (from today's 5 PM to last date's 5 PM)
end_datetime = datetime.now().replace(hour=17, minute=0, second=0, microsecond=0)
start_datetime = end_datetime - timedelta(days=1)

# Initialize an empty list to store data within the date and time range
filtered_data = []

# Initialize a page counter
page = 1

while True:
    # Construct the full API URL for the current page
    api_url = base_api_url + str(page)

    # Make an HTTP GET request to the API
    response = requests.get(api_url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Convert the JSON response to a Python dictionary
        data = response.json()

        # Extract specific fields from the "results" section
        results = data["results"]

        for entry in results:
            created_at = datetime.strptime(entry["created_at"], "%Y-%m-%dT%H:%M:%SZ")

            # Check if the entry's created_at timestamp is within the specified range
            if start_datetime <= created_at <= end_datetime:
                filtered_data.append({"domain": entry["domain"], "title": entry["title"], "created_at": entry["created_at"]})

        # Check if there is a next page, and if not, break out of the loop
        if not data["next"]:
            break

        # Increment the page counter for the next iteration
        page += 1
    else:
        print(f"Failed to fetch data from page {page}. Status code: {response.status_code}")
        break

# Create a DataFrame from the filtered data
df = pd.DataFrame(filtered_data)

# Get the current date in the desired format for the filename (YYYY-MM-DD)
current_date = datetime.now().strftime("%Y-%m-%d")

# Specify the path where you want to save the CSV file
csv_file_path = f"{current_date} all_news.csv"

# Encoding and data type handling if needed
df.to_csv(csv_file_path, index=False, encoding='utf-8')

print(f"File created successfully {csv_file_path}")
