import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

# Email credentials and SMTP settings
sender_email = "beharamadhuprakash@gmail.com"
password = "xvethqhviqehchdh"
smtp_server = "smtp.gmail.com"
port = 587  # For starttls


def send_email(subject,receiver_email, html):
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = receiver_email
    # Attach HTML content to MIME object
    part = MIMEText(html, "html")
    message.attach(part)
    try:
        server = smtplib.SMTP(smtp_server, port)
        server.ehlo()  # Can be omitted
        server.starttls()  # Secure the connection
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error: {e}")


def generate_otp():
    return random.randint(100000, 999999)

def send_otp_via_email(student_id):
    current_timestamp = get_current_timestamp()
    GENERATED_OTP=generate_otp()
    # Write HTML content
    html = f"""\
    <!DOCTYPE html>
    <html>
    <head>
    <style>
    body {{
            font-family: Arial, sans-serif;
            background-color: #f0f0f0;
            margin: 0;
            padding: 0;
        }}
        .container {{
            background-color: #ffffff;
            width: 600px;
            margin: 20px auto;
            padding: 20px;
            border: 1px solid #dddddd;
        }}
        .header {{
            background-color: #007bff;
            color: white;
            padding: 10px;
            text-align: center;
            font-size: 24px;
        }}
        .content {{
            margin: 20px 0;
        }}
        .footer {{
            font-size: 12px;
            text-align: center;
            color: grey;
            margin-top: 20px;
        }}
        .signature {{
            margin-top: 20px;
        }}
    </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                Attendance Record Update
            </div>
            <div class="content">
                <p>Dear {student_id},</p>
                <p>This is the One Time Password: <b>{GENERATED_OTP}</b></p>
                <div class="signature">
                    <p>Warm regards,</p>
                    <p>Dr. Strange<br>Lecturer<br><a href="mailto:{sender_email}">{sender_email}</a></p>
                </div>
            </div>
            <div class="footer">
                © 2023, Cleveland State University
            </div>
        </div>
    </body>
    </html>
    """
    subject=f"ALERT OTP EMAIL-{current_timestamp}"
    receiver_email = f"{student_id}@vikes.csuohio.edu"
    send_email(subject,receiver_email, html)
    print(receiver_email,GENERATED_OTP)
    return GENERATED_OTP
    

def get_current_timestamp():
    # Get the current date and time
    now = datetime.now()
    # Format the date to match the desired format
    timestamp = now.strftime("%A, %d %B %Y %H:%M")
    return timestamp




def send_attendance_email(
    student_name,
    student_id,
    class_name="CIS 634-Software Engineering",
):
    current_timestamp = get_current_timestamp()
    # Write HTML content
    html = f"""\
    <!DOCTYPE html>
    <html>
    <head>
    <style>
    body {{
            font-family: Arial, sans-serif;
            background-color: #f0f0f0;
            margin: 0;
            padding: 0;
        }}
        .container {{
            background-color: #ffffff;
            width: 600px;
            margin: 20px auto;
            padding: 20px;
            border: 1px solid #dddddd;
        }}
        .header {{
            background-color: #007bff;
            color: white;
            padding: 10px;
            text-align: center;
            font-size: 24px;
        }}
        .content {{
            margin: 20px 0;
        }}
        .footer {{
            font-size: 12px;
            text-align: center;
            color: grey;
            margin-top: 20px;
        }}
        .signature {{
            margin-top: 20px;
        }}
    </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                Attendance Record Update
            </div>
            <div class="content">
                <p>Dear {student_name},</p>
                <p>I hope this email finds you well.</p>
                <p>I am writing to inform you about the recent update to your attendance record for the {class_name}. As of {current_timestamp}, your attendance has been marked as Present.</p>
                <p>It is essential to regularly check your attendance record and ensure you maintain a satisfactory attendance percentage throughout the academic session. Regular attendance not only reflects commitment but also significantly contributes to understanding the course material and academic success.</p>
                <p>If you believe there is an error or discrepancy regarding your attendance mark or have any extenuating circumstances that led to present, please contact me or the administrative office at your earliest convenience. We will do our best to address your concerns.</p>
                <p>Please remember that maintaining a good attendance record is crucial for your academic progress. If you are facing any challenges, do not hesitate to reach out. We are here to support and guide you throughout your academic journey.</p>
                <p>Thank you for your attention to this matter. Wishing you all the best in your studies.</p>
                <div class="signature">
                    <p>Warm regards,</p>
                    <p>Dr. Strange<br>Lecturer<br><a href="mailto:{sender_email}">{sender_email}</a></p>
                </div>
            </div>
            <div class="footer">
                © 2023, Cleveland State University
            </div>
        </div>
    </body>
    </html>
    """
    subject=f"Update Attendance-{class_name}-{current_timestamp}"
    receiver_email = f"{student_id}@vikes.csuohio.edu"
    send_email(subject,receiver_email, html)
    # Create a MIME object
    
   


