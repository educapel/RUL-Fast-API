import requests

url = 'http://0.0.0.0:8000/rul'



sample_data = {
  "s_1": 0.0,
  "s_2": 0.421876,
  "s_3": 0.512349,
  "s_4": 0.0,
  "s_5": 1.0,
  "s_6": 0.492156,
  "s_7": 0.334521,
  "s_8": 0.198765,
  "s_9": 0.0,
  "s_10": 0.389234,
  "s_11": 0.578912,
  "s_12": 0.312456,
  "s_13": 0.167890,
  "s_14": 0.456123,
  "s_15": 0.0,
  "s_16": 0.423567,
  "s_17": 0.0,
  "s_18": 0.0,
  "s_19": 0.467823,
  "s_20": 0.534219,
  "s_21": 0.601234
}

try:
    response = requests.post(url, json=sample_data)
    resp_json = response.json()
    print(resp_json)
    rul = resp_json['predicted_rul']

except requests.JSONDecodeError:
    print("Response is not valid JSON")
    print("Response text:", response.text)
    resp_json = None



print(f'Expected life of the machine: {rul} cycles')