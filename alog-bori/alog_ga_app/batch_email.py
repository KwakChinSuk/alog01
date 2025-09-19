import boto3
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# SES v1 클라이언트 사용
ses = boto3.client("ses", region_name="ap-northeast-2")

msg = MIMEMultipart()
msg["Subject"] = "로그 파일 내용 전송"
msg["From"] = "alog@jskwak.pe.kr"
msg["To"] = "kjs819@gmail.com"

# 로그 파일 내용 합치기
file_paths = [
    "/home/ec2-user/alog/log/alog-bori.clean.log",
    "/home/ec2-user/alog/log/git-auto-commit.log",
    "/usr/share/nginx/html/auto_commit_wwwjskwakpekr.log"
]

body_text = "EC2 → SES 로그 파일 내용 전송\n\n"
for path in file_paths:
    try:
        with open(path, "r") as f:
            content = f.read()
        body_text += f"===== {path} =====\n{content}\n\n"
    except Exception as e:
        body_text += f"===== {path} 읽기 실패 =====\n{str(e)}\n\n"

msg.attach(MIMEText(body_text, "plain"))

# SES v1: send_raw_email 호출 (Source 사용)
ses.send_raw_email(
    Source="alog@jskwak.pe.kr",   # 발신자 주소
    Destinations=["kjs819@gmail.com"],  # 수신자 주소
    RawMessage={"Data": msg.as_string()}
)