from fastapi import FastAPI, Form
from pydantic import BaseModel
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
# تنظیمات CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # مبدا frontend شما
    allow_credentials=True,
    allow_methods=["*"],  # اجازه همه متدهای HTTP (GET, POST, OPTIONS, و غیره)
    allow_headers=["*"],  # اجازه همه هدرها
)

class Feedback(BaseModel):
    name: str
    lastName: str
    email: str
    feedback: str

@app.post("/api/justis-feedback/")
async def send_feedback(name: str = Form(...), lastName: str = Form(...), email: str = Form(...), feedback: str = Form(...)):
    try:
        # تنظیمات ایمیل
        sender_email = "m10551691@gmail.com"  # ایمیل فرستنده (حساب Gmail شما)
        receiver_email = "tibaismartcompany@gmail.com"  # ایمیل گیرنده
        app_password = "qjhurpqqaaeokjzb"  # App Password تولیدشده از حساب گوگل

        # ایجاد پیام ایمیل
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = "New Feedback Submission"

        # متن ایمیل
        body = f"Name: {name}\nLast Name: {lastName}\nEmail: {email}\nFeedback: {feedback}"
        msg.attach(MIMEText(body, 'plain'))

        # اتصال به سرور SMTP گوگل
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # فعال‌سازی TLS
        server.login(sender_email, app_password)

        # ارسال ایمیل
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()

        return JSONResponse(status_code=200, content={"message": "Feedback sent successfully"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": f"Error sending feedback: {str(e)}"})