## 필요한 파일
1. 구글 스프레드 시트 접근 권한 및 json 파일
2. 슬랙의 channel, accessed_token, web hook url 값이 담긴 env 파일
3. 스프레드 시트의 id값 
---

## 실행 순서
1. main.py에 구글 스프레드 시트의 id 값을 삽입한다.
여기서 행 이름은 한글이름, 생년월일, slack id 만을 가져온다.

2. cron을 설정해 매일 오전 9시에 main.py를 실행하도록 설정한다. 
```bash
9 * * * * /home/{your_path}/python /home/eunbinpark/workspace/birthday_alarm_slackbot/main.py
```
