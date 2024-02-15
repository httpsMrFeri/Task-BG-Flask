import requests

url = "http://127.0.0.1:5000/api/store_data"
headers = {"Content-Type": "application/json", "Token": "YOUR_ACCESS_TOKEN"}

data = {
    "Device_ID": 65256,
    "event": 1,
    "Time": "15:16:20",
    "Date": "1402/12/10",
    "Data": {
        "Voltage": 6700,
        "Current": 250,
        "W_Temp1": 78,
        "W_Temp2": 76,
        "W_Temp3": 75,
        "W_Temp4": 80,
        "W_Temp5": 76.5,
        "W_Temp6": 80.2,
        "B_Temp1": 120.2,
        "B_Temp2": 110.2,
        "Vib1": 110,
        "Vin2": 115,
    },
}

try:
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()  # در صورتی که پاسخ مشکل داشته باشد، این خطا ایجاد می‌شود

    print(response.status_code)
    print(response.json())
except requests.exceptions.HTTPError as errh:
    print("HTTP Error:", errh)
except requests.exceptions.ConnectionError as errc:
    print("Error Connecting:", errc)
except requests.exceptions.Timeout as errt:
    print("Timeout Error:", errt)
except requests.exceptions.RequestException as err:
    print("Error:", err)
