import base64
import requests
from datetime import datetime, timedelta
import hashlib
import platform
import time
import sys

def check_license(phone):
    repository = "ncdathwb/License"
    access_token = "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"
    file_path = f"{phone}.txt"

    def get_file_content_from_github(repository, file_path, access_token):
        api_url = f"https://api.github.com/repos/{repository}/contents/{file_path}"
        headers = {"Authorization": f"token {access_token}"}
        response = requests.get(api_url, headers=headers)
        response_data = response.json()
        if response.status_code == 200:
            return response_data.get("content")
        else:
            print(f"Request failed with status code: {response.status_code}")
            print(f"Error message: {response_data.get('message', '')}")
            return None

    def calculate_hashed_value():
        uid = platform.uname().node + platform.processor() + platform.node()
        hashed_value = hashlib.sha256(uid.encode()).hexdigest()
        return hashed_value

    def create_file_on_github(repository, file_path, content, access_token):
        api_url = f"https://api.github.com/repos/{repository}/contents/{file_path}"
        headers = {"Authorization": f"token {access_token}"}
        encoded_content = base64.b64encode(content.encode()).decode()
        data = {"message": "Create file", "content": encoded_content}
        response = requests.put(api_url, headers=headers, json=data)
        if response.status_code == 201:
            print("File created successfully.")
        else:
            print("Failed to create file.")
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.json()}")

    file_content = get_file_content_from_github(repository, file_path, access_token)

    if file_content is not None:
        decoded_content = base64.b64decode(file_content).decode("utf-8")
        hashed_value_saved_github, expiry_time = decoded_content.strip().split("|")
        expiry_datetime = datetime.strptime(expiry_time, "%Y-%m-%d %H:%M:%S")
        hashed_value = calculate_hashed_value()
        current_datetime = datetime.now()

        if hashed_value_saved_github == hashed_value:
            if expiry_datetime > current_datetime:
                remaining_time = expiry_datetime - current_datetime
                print(f"License is valid until: {remaining_time}")
                # Perform other actions for a valid license
                return
            else:
                print("License has expired")
                print("Contact: [0375097105 - Đạt] to activate the license")
        else:
            print("Invalid license for this computer")
    else:
        print(f"No license file found for this phone number on the GitHub License repository")
        choice = input("Enter Y/N to use the trial [12h]: ").upper()
        if choice == "Y":
            hashed_value = calculate_hashed_value()
            expiry_datetime = datetime.now() + timedelta(hours=12)
            formatted_time = expiry_datetime.strftime("%Y-%m-%d %H:%M:%S")
            content = f"{hashed_value}|{formatted_time}"
            create_file_on_github(repository, file_path, content, access_token)
            print("Trial registration successful")
        else:
            print("Exiting the program")

    print("Exiting the program")
    time.sleep(5)
    sys.exit()

# Example usage:
phone_number = input("Enter the phone number: ")
check_license(phone_number)
print("- Đã pass")
