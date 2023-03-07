import pandas as pd
from datetime import datetime

from slack_messenger import SlackMessenger
from gsheet_downloader import SpreadSheetsDownloader


def birthday_alarm(slack_id, birthday):
    try:
        today = datetime.now().strftime("%m%d")
        if birthday[4:] == today:
            slack.send_msg(f"<@{slack_id}> 님의 생일을 축하드립니다 ! ")
            print("Send Message")
    except Exception as e:
        print(e)


if __name__ == "__main__":
    slack = SlackMessenger()
    gsheet = SpreadSheetsDownloader("1uXgHbGF9vjDxI1iyE23wmi9GuFZUaUHpjB2b-2KaeXI")

    sheet_values = gsheet.get_sheet_values("시트1")["values"]

    df = pd.DataFrame(sheet_values[1:], columns=sheet_values[0])[["한글이름", "생년월일", "SLACK ID"]]
    df.columns = ["name", "birthday", "slack_id"]

    df.apply(lambda x: birthday_alarm(slack_id=x["slack_id"], birthday=x["birthday"]), axis=1)
