import requests
import re

def download_instagram_post(url):
    session = requests.Session()
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        res = session.post("https://igram.io/api/ajaxSearch", headers=headers, data={"q": url})
        if res.status_code != 200:
            return None

        data = res.json()

        results = []
        for item in data.get("medias", []):
            media_url = item.get("url")
            media_type = "video" if ".mp4" in media_url else "image"
            results.append({"type": media_type, "url": media_url})

        return results

    except Exception as e:
        print(f"Error: {e}")
        return None
