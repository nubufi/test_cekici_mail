from operator import concat
from fastapi import FastAPI
from models import Context
from send_mail import send_mail

app = FastAPI()


@app.post("/send-mail")
async def send_mail_handler(context: Context):
    status, message = send_mail(context.__dict__)
    return {"status": status, "message": message}
