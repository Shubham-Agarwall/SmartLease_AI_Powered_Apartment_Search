import os
import time
import random
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from PIL import Image

def scrape_images(input_path, output_path, output_folder, user_agent=None):
    """Step 3: Scrape and save property images."""
    def get_driver(user_agent):

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--start-maximized")  # Start the browser maximized
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument(f"user-agent={user_agent}")  # Use the provided user agent
    driver = webdriver.Chrome(options=options)
    return driver


def crop_screenshot(screenshot_path, cropped_path):

    try:
        with Image.open(screenshot_path) as img:
            width, height = img.size
            # Define cropping region (center 50% width and 60% height)
            left = width * 0.25
            right = width * 0.75
            top = height * 0.2
            bottom = height * 0.8

            cropped_img = img.crop((left, top, right, bottom))
            cropped_img.save(cropped_path)
            print(f"Cropped and saved image to {cropped_path}")
    except Exception as e:
        print(f"Error cropping image {screenshot_path}: {e}")


def open_images_in_browser(input_csv, output_csv, output_folder, user_agent):

    # Read the input CSV
    df = pd.read_csv(input_csv)

    # Add a column for image folder paths
    df['image_folder_path'] = None

    # Initialize Selenium WebDriver
    driver = get_driver(user_agent)

    # Iterate over each row
    for index, row in df.iterrows():
        property_id = row['property_id']
        property_folder = os.path.join(output_folder, property_id)

        # Create the folder only if an image is processed
        image_processed = False

        for i in range(1, 6):  # Loop through picture_1 to picture_5
            picture_column = f'picture_{i}'
            image_url = row[picture_column]

            if pd.notna(image_url):  # Check if the URL is valid
                try:
                    # Open the image URL in Chrome
                    driver.get(image_url)
                    # time.sleep(3)  # Wait for the page to load
                    # adding random wait instead of fixed 3 seconds wait to replicate human like behaviour
                    time.sleep(random.uniform(1, 2))

                    # Create the folder only when processing the first valid image
                    if not image_processed:
                        os.makedirs(property_folder, exist_ok=True)
                        df.at[index, 'image_folder_path'] = property_folder  # Update the CSV
                        image_processed = True

                    # Save a screenshot of the loaded page
                    screenshot_path = os.path.join(property_folder, f"{property_id}_picture_{i}_screenshot.jpg")
                    driver.save_screenshot(screenshot_path)
                    print(f"Saved screenshot for {property_id}_picture_{i}")

                    # Crop the screenshot to remove black spaces
                    cropped_path = os.path.join(property_folder, f"{property_id}_picture_{i}.jpg")
                    crop_screenshot(screenshot_path, cropped_path)

                    # Remove the original un-cropped screenshot
                    os.remove(screenshot_path)
                except Exception as e:
                    print(f"Error opening {image_url}: {e}")

    # Quit the driver
    driver.quit()
    df.to_csv(output_path, index=False)
    print(f"Step 3 completed. Data saved to {output_path}")

