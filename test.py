import requests
version = "1.0.0\n"
web = requests.get("https://raw.githubusercontent.com/SeeminglyUnrelated/Omega/main/update.txt").text
print(version == web)
print(web)