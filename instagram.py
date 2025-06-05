import requests

def download_instagram_post(url):
    api = "https://api.rinziproject.com/instagram"
    response = requests.get(api, params={"url": url})
    if response.status_code != 200:
        return None

    data = response.json()
    results = []

    if data.get("status") != "success":
        return None

    for media in data["media"]:
        results.append({
            "type": media["type"],  # image, video
            "url": media["url"]
        })
    return results
