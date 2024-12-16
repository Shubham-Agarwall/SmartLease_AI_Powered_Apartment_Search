import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def scrape_property_details(input_path, output_path, start_row=0, end_row=None, user_agent=None):
    def get_driver():
    """
    Set up and return a Selenium WebDriver instance.
    """
    options = Options()
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.5672.126 Safari/537.36"
    )
    options.add_argument("--start-maximized")  # Start browser maximized
    driver = webdriver.Chrome(options=options)
    return driver

def extract_image_url(style_attribute):
    """
    Extract the actual image URL from the style attribute.
    """
    if not style_attribute:
        return None
    try:
        start_idx = style_attribute.find("url(") + 4
        end_idx = style_attribute.find(")", start_idx)
        image_url = style_attribute[start_idx:end_idx].strip('"')
        return image_url
    except Exception as e:
        print(f"Error extracting image URL: {e}")
        return None



def scrape_property_details(csv_file, start_row=0, end_row=None):
    """
    Scrape property details, images, and additional information from the provided CSV file.
    
    Args:
    - csv_file (str): Path to the input CSV file.
    - start_row (int): Starting row index to process.
    - end_row (int, optional): Ending row index to process. If None, process all rows.
    
    Returns:
    - DataFrame: Scraped data.
    """
    # Read the input CSV
    properties = pd.read_csv(csv_file)
    
    # Apply slicing based on start_row and end_row
    properties = properties.iloc[start_row:end_row]
    
    scraped_data = []
    driver = get_driver()



    
    for index, row in properties.iterrows():
        property_title = row["property_title"]
        property_url = row["property_url"]
        property_address = row["property_address"]
        
        print(f"Scraping: {property_title} ({property_url})")
        
        # Initialize placeholders
        picture_1, picture_2, picture_3, picture_4, picture_5 = None, None, None, None, None
        monthly_rent, bedrooms, bathrooms, square_feet = None, None, None, None
        house_feature_1, house_feature_2, house_feature_3, house_feature_4, house_feature_5 = None, None, None, None, None
        neighborhood_p1, neighborhood_p2, neighborhood_p3 = None, None, None
        about_property_p1, about_property_p2 = None, None



        
        try:
            driver.get(property_url)
            time.sleep(5)  # Wait for the page to load
            
            # # Scrape images
            # try:
            #     xpath = '//*[@id="carouselSection"]/div[2]/div/ul/li[1]/div/div/div/div'
            #     element = driver.find_element(By.XPATH, xpath)
            #     style_attribute = element.get_attribute("style")
            #     picture_1 = extract_image_url(style_attribute)
            #     print(f"Found picture_1: {picture_1}")
            # except Exception as e:
            #     print(f"Could not get picture_1: {e}")

            # Scrape images
            try:
                # Primary XPath for picture_1
                xpath = "//*[@id='carouselSection']/div[2]/div/ul/li[1]/div/div/div/div"
                element = driver.find_element(By.XPATH, xpath)
                style_attribute = element.get_attribute("style")
                picture_1 = extract_image_url(style_attribute)
                print(f"Found picture_1: {picture_1}")
            except Exception as e:
                print(f"Primary XPath could not get picture_1")
                print("\n")
                
                # Fallback XPath for picture_1
                try:
                    fallback_xpath = "//*[@id='carouselSection']/div[1]/div/ul/li/div/div/div/div"
                    element = driver.find_element(By.XPATH, fallback_xpath)
                    style_attribute = element.get_attribute("style")
                    picture_1 = extract_image_url(style_attribute)
                    print(f"Found picture_1 with fallback XPath: {picture_1}")
                except Exception as e:
                    print(f"Fallback XPath also could not get picture_1")
                    print("\n")

            
            try:
                xpath = "//*[@id='carouselSection']/div[2]/div/ul/li[2]/div[1]/div/div/div"
                element = driver.find_element(By.XPATH, xpath)
                style_attribute = element.get_attribute("style")
                picture_2 = extract_image_url(style_attribute)
                print(f"Found picture_2: {picture_2}")
            except Exception as e:
                print(f"Could not get picture_2")
                print("\n")
            
            try:
                xpath = "//*[@id='carouselSection']/div[2]/div/ul/li[2]/div[2]/div/div/div"
                element = driver.find_element(By.XPATH, xpath)
                style_attribute = element.get_attribute("style")
                picture_3 = extract_image_url(style_attribute)
                print(f"Found picture_3: {picture_3}")
            except Exception as e:
                print(f"Could not get picture_3")
                print("\n")
            
            try:
                xpath = "//*[@id='carouselSection']/div[2]/div/ul/li[3]/div[1]/div/div/div"
                element = driver.find_element(By.XPATH, xpath)
                style_attribute = element.get_attribute("style")
                picture_4 = extract_image_url(style_attribute)
                print(f"Found picture_4: {picture_4}")
            except Exception as e:
                print(f"Could not get picture_4")
                print("\n")
            
            try:
                xpath = "//*[@id='carouselSection']/div[2]/div/ul/li[3]/div[2]/div/div/div"
                element = driver.find_element(By.XPATH, xpath)
                style_attribute = element.get_attribute("style")
                picture_5 = extract_image_url(style_attribute)
                print(f"Found picture_5: {picture_5}")
            except Exception as e:
                print(f"Could not get picture_5")
                print("\n")
            
            # Scrape additional details
            try:
                monthly_rent = driver.find_element(
                    By.XPATH, "//*[@id='priceBedBathAreaInfoWrapper']/div/div/ul/li[1]/div/p[2]"
                ).text
                print(f"Monthly Rent: {monthly_rent}")
            except Exception as e:
                print(f"Could not get monthly_rent")
                monthly_rent = None
                print("\n")
            
            try:
                bedrooms = driver.find_element(
                    By.XPATH, "//*[@id='priceBedBathAreaInfoWrapper']/div/div/ul/li[2]/div/p[2]"
                ).text
                print(f"Bedrooms: {bedrooms}")
            except Exception as e:
                print(f"Could not get bedrooms")
                bedrooms = None
                print("\n")
            
            try:
                bathrooms = driver.find_element(
                    By.XPATH, "//*[@id='priceBedBathAreaInfoWrapper']/div/div/ul/li[3]/div/p[2]"
                ).text
                print(f"Bathrooms: {bathrooms}")
            except Exception as e:
                print(f"Could not get bathrooms")
                bathrooms = None
                print("\n")
            
            try:
                square_feet = driver.find_element(
                    By.XPATH, "//*[@id='priceBedBathAreaInfoWrapper']/div/div/ul/li[4]/div/p[2]"
                ).text
                print(f"Square Feet: {square_feet}")
            except Exception as e:
                print(f"Could not get square_feet")
                square_feet = None
                print("\n")


            try:
                availability = driver.find_element(
                    By.XPATH, "//*[@id='unitDetailInfoWrapper']/div[1]/span/span[3]"
                ).text
                print(f"Availability: {availability}")
            except Exception as e:
                print(f"Could not get availability")
                availability = None
                print("\n")


            try:
                deposit = driver.find_element(
                    By.XPATH, "//*[@id='unitDetailInfoWrapper']/div[1]/span/span[2]"
                ).text
                print(f"Deposit: {deposit}")
            except Exception as e:
                print(f"Could not get deposit")
                deposit = None
                print("\n")

            try:
                lease_duration = driver.find_element(
                    By.XPATH, "//*[@id='unitDetailInfoWrapper']/div[1]/span/span[1]"
                ).text
                print(f"Lease Duration: {lease_duration}")
            except Exception as e:
                print(f"Could not get lease_duration")
                lease_duration = None
                print("\n")

            try:
                about_property_p1 = driver.find_element(
                    By.XPATH, "//*[@id='descriptionSection']/p[1]"
                ).text
                print(f"About Property (Paragraph 1): {about_property_p1}")
            except Exception as e:
                print(f"Could not get about_property_p1")
                about_property_p1 = None
                print("\n")

            try:
                about_property_p2 = driver.find_element(
                    By.XPATH, "//*[@id='descriptionSection']/p[2]"
                ).text
                print(f"About Property (Paragraph 2): {about_property_p2}")
            except Exception as e:
                print(f"Could not get about_property_p2")
                about_property_p2 = None
                print("\n")

            # Create a single string combining all about property paragraphs
            about_property_details = " ".join(
                filter(None, [about_property_p1, about_property_p2])
            )
            print(f"About Property Details: {about_property_details}")



            try:
                house_feature_1 = driver.find_element(
                    By.XPATH, '//*[@id="amenitiesSection"]/div/div/div/div/div/ul/li[1]/span'
                ).text
                print(f"House Feature 1: {house_feature_1}")
            except Exception as e:
                print(f"Could not get house_feature_1")
                house_feature_1 = None
                print("\n")


            try:
                house_feature_2 = driver.find_element(
                    By.XPATH, '//*[@id="amenitiesSection"]/div/div/div/div/div/ul/li[2]/span'
                ).text
                print(f"House Feature 2: {house_feature_2}")
            except Exception as e:
                print(f"Could not get house_feature_2")
                house_feature_2 = None
                print("\n")


            try:
                house_feature_3 = driver.find_element(
                    By.XPATH, '//*[@id="amenitiesSection"]/div/div[2]/div/div/div/ul/li[3]/span'
                ).text
                print(f"House Feature 3: {house_feature_3}")
            except Exception as e:
                print(f"Could not get house_feature_3")
                house_feature_3 = None
                print("\n")


            try:
                house_feature_4 = driver.find_element(
                    By.XPATH, '//*[@id="amenitiesSection"]/div/div[2]/div/div/div/ul/li[4]/span'
                ).text
                print(f"House Feature 4: {house_feature_4}")
            except Exception as e:
                print(f"Could not get house_feature_4")
                house_feature_4 = None
                print("\n")


            
            try:
                house_feature_5 = driver.find_element(
                    By.XPATH, '//*[@id="amenitiesSection"]/div/div[2]/div/div/div/ul/li[5]/span'
                ).text
                print(f"House Feature 5: {house_feature_5}")
            except Exception as e:
                print(f"Could not get house_feature_5")
                house_feature_5 = None
                print("\n")

            # House feature concat block
            # Create a comma-separated string of all house features
            house_features = ", ".join(
                filter(None, [house_feature_1, house_feature_2, house_feature_3, house_feature_4, house_feature_5])
            )
            print(f"All House Features: {house_features}")


            try:
                neighborhood_p1 = driver.find_element(
                    By.XPATH, '//*[@id="subMarketSection"]/div/div/div/div/p[2]'
                ).text
                print(f"Neighborhood Paragraph 1: {neighborhood_p1}")
            except Exception as e:
                print(f"Could not get neighborhood_p1")
                neighborhood_p1 = None
                print("\n")

            
            try:
                neighborhood_p2 = driver.find_element(
                    By.XPATH, '//*[@id="subMarketSection"]/div/div/div/div/p[3]'
                ).text
                print(f"Neighborhood Paragraph 2: {neighborhood_p2}")
            except Exception as e:
                print(f"Could not get neighborhood_p2")
                neighborhood_p2 = None
                print("\n")


            try:
                neighborhood_p3 = driver.find_element(
                    By.XPATH, '//*[@id="subMarketSection"]/div/div/div/div/p[4]'
                ).text
                print(f"Neighborhood Paragraph 3: {neighborhood_p3}")
            except Exception as e:
                print(f"Could not get neighborhood_p3")
                neighborhood_p3 = None
                print("\n")



            # Neighborhood concat block
            # Create a single string combining all neighborhood paragraphs
            neighborhood_details = " ".join(
                filter(None, [neighborhood_p1, neighborhood_p2, neighborhood_p3])
            )
            print(f"All Neighborhood Details: {neighborhood_details}")



            try:
                utilities_included_1 = driver.find_element(
                    By.XPATH, "//*[@id='profileV2FeesWrapper']/div[2]/div[1]/div/div/div[2]/ul/li[1]/div/div"
                ).text
                print(f"Utilities Included 1: {utilities_included_1}")
            except Exception as e:
                print(f"Could not get utilities_included_1")
                utilities_included_1 = None
                print("\n")

            try:
                utilities_included_2 = driver.find_element(
                    By.XPATH, "//*[@id='profileV2FeesWrapper']/div[2]/div[1]/div/div/div[2]/ul/li[2]/div/div"
                ).text
                print(f"Utilities Included 2: {utilities_included_2}")
            except Exception as e:
                print(f"Could not get utilities_included_2")
                utilities_included_2 = None
                print("\n")


            try:
                utilities_included_3 = driver.find_element(
                    By.XPATH, "//*[@id='profileV2FeesWrapper']/div[2]/div[1]/div/div/div[2]/ul/li[3]/div/div"
                ).text
                print(f"Utilities Included 3: {utilities_included_3}")
            except Exception as e:
                # print(f"Could not get utilities_included_3: {e}")
                print(f"Could not get utilities_included_3:")
                utilities_included_3 = None
                print("\n")

            try:
                utilities_included_4 = driver.find_element(
                    By.XPATH, "//*[@id='profileV2FeesWrapper']/div[2]/div[1]/div/div/div[2]/ul/li[4]/div/div"
                ).text
                print(f"Utilities Included 4: {utilities_included_4}")
            except Exception as e:
                print(f"Could not get utilities_included_4:")
                utilities_included_4 = None
                print("\n")

            # Create a comma-separated string combining all utilities included
            utilities_included = ", ".join(
                filter(None, [utilities_included_1, utilities_included_2, utilities_included_3, utilities_included_4])
            )
            print(f"All Utilities Included: {utilities_included}")





        
        except Exception as e:
            print(f"Error scraping {property_title}: {e}")

        scraped_data.append({
            "property_title": property_title,
            "property_address": property_address,
            "property_url": property_url,
            "monthly_rent": monthly_rent,
            "bedrooms": bedrooms,
            "bathrooms": bathrooms,
            "square_feet": square_feet,
            "availability": availability,
            "deposit": deposit,
            "lease_duration": lease_duration,
            "about_property_p1": about_property_p1,
            "about_property_p2": about_property_p2,
            "about_property_details": about_property_details,
            "house_feature_1": house_feature_1,
            "house_feature_2": house_feature_2,
            "house_feature_3": house_feature_3,
            "house_feature_4": house_feature_4,
            "house_feature_5": house_feature_5,
            "house_features": house_features,
            "neighborhood_p1": neighborhood_p1,
            "neighborhood_p2": neighborhood_p2,
            "neighborhood_p3": neighborhood_p3,
            "neighborhood_details": neighborhood_details,
            "utilities_included_1": utilities_included_1,
            "utilities_included_2": utilities_included_2,
            "utilities_included_3": utilities_included_3,
            "utilities_included_4": utilities_included_4,
            "utilities_included": utilities_included,
            "picture_1": picture_1,
            "picture_2": picture_2,
            "picture_3": picture_3,
            "picture_4": picture_4,
            "picture_5": picture_5,
        })

    driver.quit()
    pd.DataFrame(data).to_csv(output_path, index=False)
    print(f"Step 2 completed. Data saved to {output_path}")