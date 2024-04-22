import requests

for i in range(1000):
    resp = requests.get(f"https://example.com/ischool/public/AlbumViewer/index.php?aid={i}").text
    print(f"trying {i}")
    if "內部控制" in resp:
        print(f"Found at {i}")
        break
