import streamlit as st
import pymysql
import bcrypt
import base64
import requests
import os
import boto3
from datetime import datetime, timedelta
from jose import jwt, JWTError

# Set page configuration
st.set_page_config(
    page_title="Apartment Finder",
    page_icon="🏡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# AWS S3 configuration
AWS_ACCESS_KEY = "removed"
AWS_SECRET_KEY = "removed"
REGION_NAME = "us-east-2"

s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=REGION_NAME,
)

# FastAPI endpoint
FASTAPI_URL = "http://127.0.0.1:8000/search"

# JWT configuration (dummy token used after login)
SECRET_KEY = "your_secret_key_here"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Path to your background image file
image_path = "/home/ubuntu/smartlease/Screenshot 2024-12-13 at 10.48.36 AM.png"

def get_base64_of_bin_file(bin_file_path):
    with open(bin_file_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

base64_image = get_base64_of_bin_file(image_path)

def set_background(image_file_path, apply_image):
    if apply_image:
        bin_str = get_base64_of_bin_file(image_file_path)
        background_image = f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{bin_str}");
            background-size: cover;
            background-repeat: no-repeat;
            background-position: center;
        }}
        </style>
        """
        st.markdown(background_image, unsafe_allow_html=True)

# Database connection details
DB_HOST = "removed"
DB_USER = "removed"
DB_PASSWORD = "removed"
DB_NAME = "removed"

def connect_to_db():
    try:
        return pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
    except Exception as e:
        st.error("Database connection failed!")
        st.error(str(e))
        return None

def hash_password(password):
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

def verify_password(password, hashed_password_bytes):
    # hashed_password_bytes is retrieved from DB as bytes (after decoding from latin-1 if needed)
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password_bytes)

def navigate_to(page):
    st.session_state.page = page

def show_homepage():
    st.markdown(
        """
        <style>
        .text-box {
            background-color: rgba(255, 255, 255, 0.8);
            padding: 30px;
            border-radius: 15px;
            text-align: center;
            max-width: 600px;
            margin: auto;
            margin-top: 10%;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }
        .stButton>button {
            display: inline-block;
            margin: 10px 20px;
            width: 150px;
            height: 45px;
            font-size: 16px;
            font-weight: bold;
            border-radius: 10px;
            background-color: #007BFF;
            color: white;
            border: none;
        }
        </style>
        <div class="text-box">
            <h1 style="font-size: 36px; font-weight: bold; margin-bottom: 10px;">Welcome to Smartlease!</h1>
            <p style="font-size: 18px; margin-bottom: 30px;">Find your dream apartment with ease, we’ve got you covered!</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_empty, col1, col2 = st.columns([1, 1, 1.7])
    # with col1:
    #     if st.button("Register"):
    #         st.session_state.page = "register"
    # with col2:
    #     if st.button("Login"):
    #         st.session_state.page = "login"
    
    # with col1:
    #     if st.button("Register", key="homepage_register"):
    #         st.session_state.page = "register"
    with col1:
        if st.button("Register", key="homepage_register"):
            st.session_state.page = "register"
            st.session_state["button_clicked"] = False
    with col2:
        if st.button("Login", key="homepage_login"):
            st.session_state.page = "login"

def register_user():
    st.title("Register")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    # if st.button("Submit"):
    #     st.session_state.button_clicked = False
    # if st.button("Submit", key="register_submit"):
    #     st.session_state.button_clicked = True 
    if st.button("Submit", key="register_submit"):
        if not st.session_state["button_clicked"]:
            st.session_state["button_clicked"] = True
        # Your registration logic here

        # Basic validations
        if not username or not password:
            st.error("Please fill out all fields.")
        elif not username.isalnum():
            st.error("Username should be alphanumeric.")
        elif len(password) < 6:
            st.error("Password should be at least 6 characters long.")
        else:
            # Proceed with registration
            connection = connect_to_db()
            if connection:
                try:
                    hashed_password = hash_password(password)
                    hashed_password_str = hashed_password.decode('latin-1')
                    cursor = connection.cursor()
                    cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password_str))
                    connection.commit()
                    st.success("Registration successful!")
                    st.session_state.page = "home"
                except pymysql.IntegrityError:
                    st.error("Username already exists! Please choose a different username.")
                except Exception as e:
                    st.error("An error occurred during registration.")
                    st.error(str(e))
                finally:
                    connection.close()
    if st.button("Back"):
        st.session_state.page = "home"


def login_user():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Submit", key="login_submit"):
        st.session_state.button_clicked = False  # Track button click
        if username and password:
            connection = connect_to_db()
            if connection:
                try:
                    cursor = connection.cursor()
                    cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
                    result = cursor.fetchone()
                    if result:
                        # Convert stored latin-1 string back to bytes
                        hashed_password_str = result[0]
                        hashed_password_bytes = hashed_password_str.encode('latin-1')
                        if verify_password(password, hashed_password_bytes):
                            st.success("Login successful!")
                            st.session_state["token"] = "dummy_token" # Dummy token
                            st.session_state.page = "listings"
                        else:
                            st.error("Invalid username or password!")
                    else:
                        st.error("Invalid username or password!")
                except Exception as e:
                    st.error("An error occurred during login.")
                    st.error(str(e))
                finally:
                    connection.close()
        else:
            st.error("Please fill out all fields.")

    if st.button("Back"):
        st.session_state.page = "home"

def add_footer():
    st.markdown(
        """
        <style>
        .footer {
            position: relative;
            bottom: 0;
            width: 100%;
            background-color: #f8f9fa;
            color: #6c757d;
            text-align: center;
            padding: 20px 0;
            font-size: 14px;
            margin-top: 30px;
            border-top: 1px solid #eaeaea;
        }
        .footer a {
            color: #007bff;
            text-decoration: none;
            margin: 0 10px;
        }
        .footer a:hover {
            text-decoration: underline;
        }
        .footer p {
            margin: 5px 0;
        }
        </style>
        <div class="footer">
            <p>
                <a href="https://github.com/BigDataIA-Fall2024-Team9/Final_Project" target="_blank">Github</a> |
                <a href="https://codelabs-preview.appspot.com/?file_id=1WbWk5iBNWCyzCEaPw00eHkIJtrVBlYLllg1MIPXEyOk#0" target="_blank">Project Documentation</a>
            </p>
            <p>SmartLease revolutionizes apartment searching by enabling users to search conversationally, bypassing traditional filters. Utilizing AI-powered system, simplifies and personalizes the search process.</p>
            <p>&copy; 2024 SmartLease. All rights reserved.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
def fetch_images_from_s3(folder_path):
    if folder_path.startswith("s3://"):
        folder_path = folder_path.replace("s3://", "")
    else:
        return []

    parts = folder_path.split("/", 1)
    if len(parts) < 2:
        return []
    bucket_name, prefix = parts
    images = []
    try:
        response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
        for obj in response.get("Contents", []):
            if obj["Key"].endswith((".jpeg", ".jpg", ".png")):
                image_url = f"https://{bucket_name}.s3.{REGION_NAME}.amazonaws.com/{obj['Key']}"
                images.append(image_url)
    except Exception as e:
        st.error(f"Error fetching images from S3: {e}")
    return images

def show_apartment_listings():
    st.markdown(
        f"""
        <style>
        .background {{
            background-image: url("data:image/jpeg;base64,{base64_image}");
            background-size: cover;
            background-repeat: no-repeat;
            background-position: center;
            height: 250px;
            width: 100%;
        }}
        .title-container {{
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100%;
            color: white;
            font-size: 48px;
            font-weight: bold;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.7);
        }}
        </style>
        <div class="background">
            <div class="title-container">
                 Smartlease
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if "token" not in st.session_state:
        st.error("Please log in first.")
        return

    search_query = st.text_input("Looking for apartment?", placeholder="Search Your Dream Home")

    apartments = []
    if search_query:
        try:
            headers = {"Authorization": f"Bearer {st.session_state['token']}"}
            payload = {"user_query": search_query}
            response = requests.post(FASTAPI_URL, headers=headers, json=payload)

            if response.status_code == 200:
                data = response.json()
                if data["status"] == "success":
                    apartments = data["data"]
                else:
                    st.error("Failed to fetch results.")
            else:
                st.error(f"FastAPI returned error: {response.status_code}")
        except Exception as e:
            st.error(f"Error querying FastAPI: {e}")

    if apartments:
        for i in range(0, len(apartments), 3):
            cols = st.columns(3)
            for idx, col in enumerate(cols):
                if i + idx < len(apartments):
                    apt = apartments[i + idx]
                    meta = apt["metadata"]
                    folder_path = meta.get("property_image_folder_s3_path", "")
                    images = fetch_images_from_s3(folder_path)
                    with col:
                        st.image(images[0] if images else "https://via.placeholder.com/150", use_container_width=True)
                        st.markdown(f"**{meta.get('property_title', 'N/A')}**")
                        st.markdown(f"**Address:** {meta.get('property_address', 'N/A')}")
                        st.markdown(f"**Rent:** {meta.get('monthly_rent', 'N/A')}")
                        st.markdown(f"**Bedrooms:** {meta.get('bedrooms', 'N/A')}, **Bathrooms:** {meta.get('bathrooms', 'N/A')}")
                        st.markdown(f"**Square Feet:** {meta.get('square_feet', 'N/A')}")
                        st.markdown(f"**Distance:** {meta.get('distance', 'N/A')}")

                        with st.expander("View More Details"):
                            st.markdown(f"**Availability:** {meta.get('availability', 'N/A')}")
                            st.markdown(f"**Details:** {meta.get('about_property_details', 'N/A')}")
                            st.markdown(f"**Features:** {meta.get('house_features', 'N/A')}")
                            st.markdown(f"**Lease Duration:** {meta.get('lease_duration', 'N/A')}")
                            st.markdown(f"**Deposit:** {meta.get('deposit', 'N/A')}")
                            st.markdown(f"**Utilities Included:** {meta.get('utilities_included', 'N/A')}")

    else:
        st.warning("No apartments found matching your search.")

    if st.button("Logout", key="logout"):
        st.session_state.page = "home"
        st.session_state.token = None  

    add_footer()

if "page" not in st.session_state:
    st.session_state.page = "home"

if st.session_state.page == "home":
    set_background(image_path, True)
    show_homepage()
elif st.session_state.page == "register":
    set_background(image_path, False)
    register_user()
elif st.session_state.page == "login":
    set_background(image_path, False)
    login_user()
elif st.session_state.page == "listings":
    set_background(image_path, False)
    show_apartment_listings()
