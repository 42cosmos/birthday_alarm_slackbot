import os
import sys
import json
import slack_sdk
import requests


def load_secret(name, key_path=None):
    if not key_path:
        key_path = os.getcwd()
    with open(os.path.join(key_path, "secret.json"), "r") as f:
        secret = json.load(f)[name]
    return secret


class SlackMessenger:
    def __init__(self, test=False):
        name = "TEST_SLACK" if test else "SLACK"
        secret = load_secret(name)
        self._channel = secret["CHANNEL"]
        self._token = secret["ACCESSED_TOKEN"]
        self._web_hook_url = secret["WEB_HOOK_URL"]
        self._client = slack_sdk.WebClient(token=self._token)

    def send_file(self, file_path, file_title):
        response = self._client.files_upload(
            channels=self._channel,
            file=file_path,
            title=file_title,
            filetype='excel'
        )

    def send_msg(self, slack_text):
        slack_text = make_slack_format(slack_text)
        response = requests.post(self._web_hook_url, data=slack_text, headers={'Content-Type': 'application/json'})
        if response.status_code != 200:
            raise ValueError(response.status_code, response.text)

    def alarm_msg(self, title, alarm_text, colour="#0000ff"):
        slack_text = make_alarm_format(title, alarm_text, colour)
        response = requests.post(self._web_hook_url, data=slack_text, headers={'Content-Type': 'application/json'})
        if response.status_code != 200:
            raise ValueError(response.status_code, response.text)


def make_slack_format(text: str):
    return json.dumps({"text": text})


def make_alarm_format(title: str, text: str, colour):
    result = {"attachments": [
        {
            "color": colour,
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "plain_text",
                        "text": f"{title}"
                    }
                },
                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "plain_text",
                            "text": f"{text}"
                        }
                    ]
                }
            ]}]}
    return json.dumps(result)
