import requests
import json

def download_instagram_post(insta_url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest",
        "Origin": "https://igram.io",
        "Referer": "https://igram.io/",
    }
    
    api_url = "https://igram.io/api/ajaxSearch"
    payload = {"q": insta_url}

    print(f"[INFO] Attempting to download: {insta_url}")
    print(f"[INFO] API URL: {api_url}")
    # print(f"[INFO] Headers: {headers}") # For very detailed logging if needed
    # print(f"[INFO] Payload: {payload}")

    try:
        res = requests.post(
            api_url,
            headers=headers,
            data=payload,
            timeout=20 
        )

        print(f"[INFO] Response Status Code: {res.status_code}")
        # It's useful to see the beginning of the response text, especially for errors
        print(f"[INFO] Response Text (first 300 chars): {res.text[:300]}")

        if res.status_code == 403:
             print(f"[ERROR] API request forbidden (403). This might be an IP block or header issue.")
             print(f"[ERROR] Full Response content: {res.text}")
             return None
        if res.status_code == 429:
             print(f"[ERROR] API rate limit exceeded (429). Too many requests.")
             print(f"[ERROR] Full Response content: {res.text}")
             return None
        if res.status_code != 200:
            print(f"[ERROR] API request failed with status code {res.status_code}.")
            print(f"[ERROR] Full Response content: {res.text}")
            return None

        content_type = res.headers.get("Content-Type", "")
        if "application/json" not in content_type.lower():
            print(f"[ERROR] Response content type is not JSON: {content_type}")
            print(f"[ERROR] Full Response content: {res.text}")
            # Attempt to parse if it looks like JSON but header is wrong
            try:
                data = json.loads(res.text)
                print("[WARNING] Parsed JSON despite incorrect Content-Type header.")
            except json.JSONDecodeError:
                print("[ERROR] Could not parse non-JSON response after attempting.")
                return None
        else:
            try:
                data = res.json()
            except json.JSONDecodeError as e:
                print(f"[ERROR] Failed to decode JSON response: {e}")
                print(f"[ERROR] Response text that failed to parse: {res.text}")
                return None
        
        print(f"[INFO] JSON Response Data: {data}")

        if isinstance(data, dict) and data.get("status") == "error":
            error_message = data.get("message", "Unknown error from igram.io")
            print(f"[ERROR] igram.io reported an error: {error_message}")
            if "blocked" in error_message.lower():
                print(f"[INFO] This often means your server's IP is blocked by igram.io.")
            return None

        media_list = []
        if isinstance(data, dict) and data.get("status") == "success" and "medias" in data:
            for item in data.get("medias", []):
                media_url = item.get("url")
                if not media_url:
                    print(f"[WARNING] Media item found without a URL: {item}")
                    continue
                
                media_type = item.get("type", "").lower() 
                if not media_type:
                    media_type = "video" if ".mp4" in media_url.lower() else "image"
                
                media_list.append({"type": media_type, "url": media_url})
        else:
            print(f"[WARNING] 'medias' key not found, status was not 'success', or response format is unexpected: {data}")
            return None

        if not media_list:
            print("[INFO] No media items extracted from the response.")
            return None
            
        return media_list

    except requests.exceptions.Timeout:
        print(f"[ERROR] Request to {api_url} timed out.")
        return None
    except requests.exceptions.RequestException as e: # Catches network-related errors
        print(f"[ERROR] Request Exception: {e}")
        return None
    except Exception as e: # Catches any other unexpected errors
        print(f"[ERROR] An unexpected error occurred in download_instagram_post: {e}")
        return None
