import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from ...errors.auth_errors import EmailFailedToSendError
from ....config import email_settings

class EmailService:
    def __init__(self):
        self.username = email_settings.MAIL_USERNAME
        self.password = email_settings.MAIL_PASSWORD
        self.server = email_settings.MAIL_SERVER
        self.port = email_settings.MAIL_PORT
        self.sender = email_settings.MAIL_FROM
        self.use_tls = email_settings.MAIL_TLS
        self.use_ssl = email_settings.MAIL_SSL

    def send_email(self, recipient: str, subject: str, body_html: str,
                                body_text: str = None) -> bool:
        """Send email to a recipient with a given subject and body."""
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = self.sender
        message["To"] = recipient

        if body_text:
            message.attach(MIMEText(body_text, "plain"))

        message.attach(MIMEText(body_html, "html"))
        try:
            with smtplib.SMTP(self.server, self.port) as server:
                if self.use_tls:
                    server.starttls()
                server.login(self.username, self.password)
                server.sendmail(self.sender, recipient, message.as_string())
                return True
        except Exception as e:
            raise EmailFailedToSendError(detail = str(e))


    def send_staff_onboarding_email(self, to_email: str, first_name: str, last_name: str, password: str) -> bool:
        """Send an onboarding email with temporary password to a new staff member."""
        subject = "Welcome to Kademia - Your Account Information"

        html_body = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
                .container {{ padding: 20px; }}
                .header {{ background-color: #003366; color: white; padding: 10px; text-align: center; }}
                .content {{ padding: 20px; }}
                .footer {{ font-size: 12px; color: #666; text-align: center; margin-top: 20px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Welcome to Kademia</h1>
                </div>
                <div class="content">
                    <p>Dear {first_name} {last_name},</p>
                    
                    <p>Your Kademia account has been created. You can log in with the following credentials:</p>
                    
                    <p><strong>Email:</strong> {to_email}</p>
                    <p><strong>Temporary Password:</strong> {password}</p>
                    
                    <p><strong>Important:</strong> Please change your password immediately after your first login for security reasons.</p>
                    
                    <p>If you have any questions, please contact the IT department.</p>
                    
                    <p>Best regards,<br>Kademia Admin Team</p>
                </div>
                <div class="footer">
                    <p>This is an automated message. Please do not reply to this email.</p>
                </div>
            </div>
        </body>
        </html>
        """

        text_body = f"""
        Welcome to Kademia!
        
        Dear {first_name} {last_name},
        
        Your Kademia account has been created. You can log in with the following credentials:
        
        Email: {to_email}
        Temporary Password: {password}
        
        Important: Please change your password immediately after your first login for security reasons.
        
        If you have any questions, please contact the IT department.
        
        Best regards,
        Kademia Administration Team
        
        This is an automated message. Please do not reply to this email.
        """

        return self.send_email(to_email, subject, html_body, text_body)