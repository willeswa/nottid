from ctypes import cast
import datetime
import schedule
import time
from email.mime.multipart import MIMEMultipart
import smtplib
from email.mime.text import MIMEText
import random

from config import Config
from models import Profile, JournalEntry, db

def last_one_day_entry():
    current_time = datetime.datetime.utcnow()
    last_24_hours = current_time - datetime.timedelta(hours=24)
    entries = db.session.query(JournalEntry).filter(
        JournalEntry.created_at > last_24_hours).all()

    if len(entries) == 0:
        return None
    else:
        return entries

def email_out_entries():
    entries = last_one_day_entry()
    if entries != None:
        rand = random.randint(0, len(entries) - 1)
        user_from_random_entry = entries[rand]
        user = db.session.query(Profile).filter(
            Profile.author_id == user_from_random_entry.author_id
        ).first()

        for entry in entries:
            send_email(user, entry)

def send_email(user, entry):
    sender = "@gmail.com"
    password = ""

    msg = MIMEMultipart()
    msg["Subject"] = "Here's an entry from another Nottider"
    msg["From"] = sender
    msg["To"] = user.email

    body = entry.text

    msg.attach(MIMEText(body,  'plain'))
    
    server = smtplib.SMTP(Config.EMAIL_HOST, 587)
    server.ehlo()
    server.starttls()
    server.login(sender, password)
    text = msg.as_string()
    server.sendmail(sender, user.email, text)
    server.quit()


schedule.every().day.at("18:02").do(email_out_entries)

def start_schedule():
    starttime = time.time()
    while True:
        schedule.run_pending()
        time.sleep(60 - ((time.time() - starttime) % 60))


    