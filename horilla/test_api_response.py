#!/usr/bin/env python
import requests
import json

def test_chatbot_api():
    url = "http://localhost:8000/nlp/api/chatbot/"
    headers = {
        "Content-Type": "application/json",
        "X-CSRFToken": "test"
    }
    cookies = {"csrftoken": "test"}
    data = {"message": "Halo"}
    
    try:
        print(f"Testing API endpoint: {url}")
        print(f"Request data: {data}")
        
        response = requests.post(url, json=data, headers=headers, cookies=cookies)
        
        print(f"\nResponse status code: {response.status_code}")
        print(f"Response headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            try:
                json_response = response.json()
                print(f"\n=== API Response ===")
                print(json.dumps(json_response, indent=2, ensure_ascii=False))
                
                if 'response' in json_response:
                    print(f"\nResponse field found: {json_response['response']}")
                else:
                    print("\nNo 'response' field in API response")
                    
            except json.JSONDecodeError as e:
                print(f"\nFailed to parse JSON response: {e}")
                print(f"Raw response: {response.text}")
        else:
            print(f"\nAPI request failed with status {response.status_code}")
            print(f"Response text: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("\nConnection error: Make sure Django server is running on localhost:8000")
    except Exception as e:
        print(f"\nError testing API: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_chatbot_api()