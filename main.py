import pandas
import datetime as dt
import random
import os
import smtplib

LETTER_TEMPLATES_FOLDER = "letter_templates"
PLACEHOLDER = "[NAME]"
EMAIL = "<SENDER EMAIL>"
PASSWORD = "<RECEIVER EMAIL>"

birthdays_data = pandas.read_csv("birthdays.csv")
birthdays_list = birthdays_data.to_dict(orient="records")


def generate_birthday_message(name):
    letter_templates_files = os.listdir(
        os.path.join(os.getcwd(), LETTER_TEMPLATES_FOLDER))

    random_template = random.choice(letter_templates_files)

    with open(f"{LETTER_TEMPLATES_FOLDER}/{random_template}", "r") as letter_file:
        template_content = letter_file.read()
        return template_content.replace(PLACEHOLDER, name)


def send_email(recipient_email, content):
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=EMAIL, password=PASSWORD)
        connection.sendmail(from_addr=EMAIL, to_addrs=recipient_email,
                            msg=f"Subject:Happy Birthday\n\n{content}")


now = dt.datetime.now()
current_month = now.month
current_day = now.day

for birthday in birthdays_list:
    if birthday["month"] == current_month and birthday["day"] == current_day:
        try:
            birthday_message = generate_birthday_message(birthday["name"])
            send_email(birthday["email"], birthday_message)
        except Exception:
            print(Exception)
        else:
            print(f"Succeeded in sending birthday email to {birthday['name']}")
