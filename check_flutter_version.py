import requests
import os

SLACK_WEBHOOK_URL = os.environ['SLACK_WEBHOOK_URL']

# Flutter SDK의 최신 버전을 가져옵니다.
response = requests.get('https://api.github.com/repos/flutter/flutter/releases')
releases = response.json()

stable_release = next((release for release in releases if "stable" in release["body"].lower()), None)
if stable_release:
    new_version = stable_release["tag_name"]

# 이전 버전 정보를 읽습니다.
try:
    with open('flutter_version.txt', 'r') as file:
        last_version = file.read().strip()
except FileNotFoundError:
    last_version = None

# 버전이 업데이트되었는지 확인합니다.
if new_version != last_version:
# Slack에 알림을 보냅니다.
    payload = {
        'text': f'Flutter SDK has a new version: {new_version}'
    }
    requests.post(SLACK_WEBHOOK_URL, json=payload)

# 최신 버전 정보를 파일에 저장합니다.
    with open('flutter_version.txt', 'w') as file:
        file.write(new_version)