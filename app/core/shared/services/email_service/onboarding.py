from app.core.shared.services.email_service.base import EmailService


class OnboardingService:

    def __init__(self):
        self.service = EmailService()

    def send_staff_onboarding_email(
        self, to_email: str, full_name: str, password: str
    ) -> bool:
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
                    <p>Dear {full_name},</p>

                    <p>Your Kademia account has been created and you can log in with the following credentials:</p>

                    <p><strong>Email:</strong> {to_email}</p>
                    <p><strong>Temporary Password:</strong> {password}</p>

                    <p><strong>You will be asked change your password immediately after your first login for security reasons.</strong></p>

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

        Dear {full_name},

        Your Kademia account has been created and you log in with the following credentials:

        Email: {to_email}
        Temporary Password: {password}

        You will be asked change your password immediately after your first login for security reasons.

        If you have any questions, please contact the IT department.

        Best regards,
        Kademia Administration Team

        This is an automated message. Please do not reply to this email.
        """

        return self.service.send_email(to_email, subject, html_body, text_body)

    def send_guardian_onboarding_email(
        self, to_email: str, full_name: str, password: str
    ) -> bool:
        """Send an onboarding email_service with temporary password to a guardian."""

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
                    <p>Dear {full_name},</p>

                    <p>Your Kademia account has been created and you can log in with the following credentials:</p>

                    <p><strong>Email:</strong> {to_email}</p>
                    <p><strong>Temporary Password:</strong> {password}</p>

                    <p><strong>You will be asked change your password immediately after your first login for security reasons.</strong> </p>

                    <p>If you have any questions, please contact the IT department.</p>

                    <p>Best regards,<br>Kademia Admin Team</p>
                </div>
                
                <div class="footer">
                    <p>This is an automated message. Please do not reply to this email_service.</p>
                </div>
            </div>
        </body>
        </html>
        """

        text_body = f"""
        Welcome to Kademia!

        Dear {full_name},

        Your Kademia account has been created and you can log in with the following credentials:

        Email: {to_email}
        Temporary Password: {password}

       You will be asked change your password immediately after your first login for security reasons..

        If you have any questions, please contact the IT department.

        Best regards,
        Kademia Administration Team

        This is an automated message. Please do not reply to this email_service.
        """

        return self.service.send_email(to_email, subject, html_body, text_body)
