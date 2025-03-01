import requests
import csv
import os
import time
import argparse

# Function to get video categories from a specific country
def get_video_categories(region_code):
    request_url = f"https://www.googleapis.com/youtube/v3/videoCategories?part=snippet&regionCode={region_code}&key={api_key}"
    try:
        request = requests.get(request_url, timeout=10)
        request.raise_for_status()
        categories_data = request.json().get("items", [])
    except requests.exceptions.RequestException as e:
        print(f"\033[0;31mFailed to fetch video categories for {region_code}: {e}")
        return None
    return categories_data

# Function to generate CSV of categories for each country
def write_categories_to_csv(region_code, categories):
    # Create output directory if doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # CSV file path for specific country
    csv_file_path = f"{output_dir}/{region_code}_categories.csv"

    # Open the file and write the data
    with open(csv_file_path, mode='w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["category_id", "category_name", "assignable"])  # Cabeçalho do CSV

        for category in categories:
            category_id = category.get("id", "N/A")
            snippet = category.get("snippet", {})
            category_name = snippet.get("title", "N/A")
            assignable = snippet.get("assignable", "N/A")
            writer.writerow([category_id, category_name, assignable])

    print(f"\033[0;32mCategories for {region_code} written to {csv_file_path}")

# Function to read the country code file and make requests
def get_categories_for_countries():
    for country_code in country_codes:
        print(f"\033[0;36mFetching categories for country: {country_code}")
        categories = get_video_categories(country_code)
        if categories:
            write_categories_to_csv(country_code, categories)

# Main function to start the process
if __name__ == "__main__":
    start_time = time.time()

    parser = argparse.ArgumentParser()
    parser.add_argument('--key_path', help='Path to the file containing the API key', default='api_key.txt')
    parser.add_argument('--country_code_path', help='Path to the file containing the list of country codes', default='country_codes.txt')
    parser.add_argument('--output_dir', help='Directory to save the output CSV files', default='categories/')
    args = parser.parse_args()

    # Set output directory and read API key and country codes
    output_dir = args.output_dir
    with open(args.key_path, 'r') as file:
        api_key = file.readline().strip()
    with open(args.country_code_path, 'r') as file:
        country_codes = [line.strip() for line in file.readlines()]

    # Call function to process each country
    get_categories_for_countries()

    # Calculate and display total execution time
    end_time = time.time()
    total_time = end_time - start_time
    print(f"\033[0;36mRuntime: {(total_time % 3600) // 60} minutes and {total_time % 60:.2f} seconds\033[m")
