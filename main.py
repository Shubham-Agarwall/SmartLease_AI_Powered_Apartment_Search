from step1_scrape_list import scrape_property_list
from step2_scrape_details import scrape_property_details
from step3_scrape_images import scrape_images
import toml

if __name__ == "__main__":
    config = toml.load("config.toml")

    # Step 1: Scrape property list
    scrape_property_list(
        base_url=config["base_url"],
        pages=config["pages"],
        output_path=config["paths"]["stage1_output"],
        user_agent=config["user_agent"]
    )

    # Step 2: Scrape property details
    scrape_property_details(
        input_path=config["paths"]["stage1_output"],
        output_path=config["paths"]["stage2_output"],
        user_agent=config["user_agent"]
    )

    # Step 3: Scrape images
    scrape_images(
        input_path=config["paths"]["stage2_output"],
        output_path=config["paths"]["final_output"],
        output_folder=config["paths"]["image_folder"],
        user_agent=config["user_agent"]
    )
