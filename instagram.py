import requests

def download_instagram_post(insta_url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        res = requests.post(
            "https://igram.io/api/ajaxSearch",
            headers=headers,
            data={"q": insta_url}
        )

        if res.status_code != 200:
            return None

        data = res.json()
        media_list = []

        for item in data.get("medias", []):
            media_url = item.get("url")
            media_type = "video" if ".mp4" in media_url else "image"
            media_list.append({"type": media_type, "url": media_url})

        return media_list if media_list else None

    except Exception as e:
        print(f"[ERROR] {e}")
        return None
