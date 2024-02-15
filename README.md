```
python3 -m venv venv
source venv/bin/activate  
pip install -r requirements.txt
```
for send data using `send.py` or 
```
curl -X POST -H "Content-Type: application/json" -H "Token: 8987b526fdeff62162fba711a7156835" -d '{"device_id": 2, "time": "2024-02-14T12:00:00Z", "date": "2024-02-14", "event_id": 1, "W_Temp1": 254.5, "W_Temp2": 426.0, "W_Temp3": 4.8, "W_Temp4": 2.2, "W_Temp5": 2.5, "W_Temp6": 1.9, "B_Temp1": 354.0, "B_Temp2": 363.2, "Vib1": 2.02, "Vib2": 0.215}' http://127.0.0.1:5000/api/store_data
```
