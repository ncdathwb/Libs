import base64
import requests
from datetime import datetime
import platform
import hashlib
import wmi
import time
import sys
from tqdm.notebook import tqdm

def exit_program(t):
    for i in tqdm(range(t)):
        time.sleep(1)

def check_license(phone):
    repository = "ncdathwb/License"
    access_token = "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"
    file_path = f"{phone}.txt"

    def get_day_now():
        datetime_now = datetime.now()
        return datetime_now

    def get_file_content_from_github(repository, file_path, access_token):
        api_url = f"https://api.github.com/repos/{repository}/contents/{file_path}"
        headers = {
            "Authorization": f"token {access_token}"
        }
        response = requests.get(api_url, headers=headers)
        response_data = response.json()
        if response.status_code == 200:
            file_content = response_data["content"]
            decoded_content = base64.b64decode(file_content).decode("utf-8")
            return decoded_content.strip()
        else:
            print("• Request failed with status code:", response.status_code)
            print("• Error message:", response_data.get("message", ""))
            return None

    def calculate_hashed_values():
        wmi_obj = wmi.WMI()
        uid = wmi_obj.Win32_ComputerSystemProduct()[0].UUID
        cpuid = platform.processor()
        hardwareid = platform.node()
        combined_id = uid + cpuid + hardwareid
        hash_object = hashlib.sha256()
        hash_object.update(combined_id.encode())
        hashed_value = hash_object.hexdigest()
        return hashed_value

    bool_phone = get_file_content_from_github(repository, file_path, access_token)

    if bool_phone is not None:
        file_content = bool_phone.split('|')
        hashed_value_saved_github = file_content[0]
        expiry_time = file_content[1]
        expiry_datetime = datetime.strptime(expiry_time, '%Y-%m-%d %H:%M:%S')
        expiry_datetime_unix = expiry_datetime.timestamp()
        time_day_now = get_day_now()
        time_day_now_unix = time_day_now.timestamp()
        hashed_value = calculate_hashed_values()

        if hashed_value_saved_github == hashed_value:
            if expiry_datetime_unix > time_day_now_unix:
                time_difference = expiry_datetime_unix - time_day_now_unix
                days = time_difference // (24 * 3600)
                hours = (time_difference % (24 * 3600)) // 3600
                minutes = (time_difference % 3600) // 60
                seconds = time_difference % 60
                print(f"• License còn hạn sử dụng đến: [ {int(days)}d - {int(hours)}h - {int(minutes)}m - {int(seconds)}s ]")
                # Perform other actions for a valid license
                pass
            else:
                print("• License đã hết hạn sử dụng")
                print("• Liên hệ: [ 0375097105 - Đạt ] để kích hoạt bản quyền")
                print('• Chờ 5s để thoát chương trình')
                exit_program(5)
                sys.exit()
                # Perform other actions for an expired license

        else:
            print("• License không hợp lệ cho máy tính này")
            print('• Chờ 5s để thoát chương trình')
            exit_program(5)
            sys.exit()
            # Perform other actions for an invalid license
    else:
        print("• Chưa có file license cho số điện thoại này trên Data License Github")
        yesno = input('Nhập Y/N để dùng thử [12h]: ').upper()
        if yesno == 'Y':
            regIDPC = calculate_hashed_values()
            current_time = datetime.now()
            unix_time = int(time.mktime(current_time.timetuple()))
            unix_time_plus_12h = unix_time + (12 * 3600)
            new_time = datetime.fromtimestamp(unix_time_plus_12h)
            formatted_time = new_time.strftime('%Y-%m-%d %H:%M:%S')
            content_reg_github = regIDPC + '|' + formatted_time
            create_file_on_github(repository, file_path, content_reg_github, access_token)
            print('• Đã đăng ký dùng thử thành công')
            print('• Chờ 5s để thoát chương trình')
            exit_program(5)
            sys.exit()

        else:
            print('• Chờ 5s để thoát chương trình')
            exit_program(5)
            sys.exit()

def create_file_on_github(repository, file_path, content, access_token):
    api_url = f"https://api.github.com/repos/{repository}/contents/{file_path}"
    headers = {
        "Authorization": f"token {access_token}"
    }
    encoded_content = base64.b64encode(content.encode()).decode()
    data = {
        "message": "Create file",
        "content": encoded_content
    }
    response = requests.put(api_url, headers=headers, json=data)
    if response.status_code == 201:
        print("File created successfully.")
    else:
        print("Failed to create file.")
        print("Status Code:", response.status_code)
        print("Response:", response.json())
# Example usage:
phone_number = input("Nhập số điện thoại: ")
check_license(phone_number)
print('- Đã pass')