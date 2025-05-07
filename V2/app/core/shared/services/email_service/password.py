from V2.app.core.shared.services.email_service.base import EmailService

class PasswordEmailService:

    def __init__(self):
        self.service = EmailService()


    def send_password_change_notification(
            self, to_email: str, name: str
    ) -> bool:
        """Notify user (guardian and staff) their password has been changed successfully."""

        subject = "Your Kademia Password Has Been Changed"

        html_body = f"""
            <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
                    .container {{ padding: 20px; }}
                    .header {{ background-color: #003366; color: white; padding: 10px; text-align: center; }}
                    .content {{ padding: 20px; }}
                    .button {{
                        background-color: #222;
                        color: #fff;
                        padding: 12px 24px;
                        text-align: center;
                        text-decoration: none;
                        display: inline-block;
                        font-weight: bold;
                        border-radius: 4px;
                        margin-top: 20px;
                    }}
                    .footer {{ font-size: 12px; color: #666; text-align: center; margin-top: 20px; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>Password Change Confirmation</h1>
                    </div>
                    <div class="content">
                        <p>Dear {name},</p>

                        <p>This is a confirmation that your Kademia password has been successfully changed.</p>

                        <p>If you made this change, no further action is required.</p>

                        <p><strong>Didn't make this change?</strong> Please contact the IT support team immediately:</p>

                        <a href="https://support.kademia.com" class="button">Contact Support</a>

                        <p>Best regards,<br>Kademia Support Team</p>
                    </div>
                    <div class="footer">
                        <p>This is an automated message. Please do not reply to this email.</p>
                    </div>
                </div>
            </body>
            </html>
        """

        text_body = f"""
            Password Change Confirmation

            Dear {name},

            This is a confirmation that your Kademia password has been successfully changed.

            If you made this change, no further action is required.

            Didn't make this change? Contact IT support immediately:
            https://support.kademia.com

            Best regards,
            Kademia Support Team

            This is an automated message. Please do not reply to this email.
        """

        return self.service.send_email(to_email, subject, html_body, text_body)



    def send_ward_password_change_alert(
            self, to_email: str, guardian_name: str, ward_name: str) -> bool:
        """
        Sends a notification to the guardian that their ward changed their password.
        """

        subject = f"Password Change Alert for {ward_name}"

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
                        <h1>Password Change Alert</h1>
                    </div>
                    <div class="content">
                        <p>Dear {guardian_name},</p>

                        <p>This is to inform you that your ward, <strong>{ward_name}</strong>, has successfully changed their Kademia password.</p>

                        <p>If you did not expect this change or have any concerns, please contact our support team as soon as possible.</p>

                        <p>Best regards,<br>Kademia Support Team</p>
                    </div>
                    <div class="footer">
                        <p>This is an automated message. Please do not reply to this email.</p>
                    </div>
                </div>
            </body>
            </html>
        """

        text_body = f"""
            Password Change Alert

            Dear {guardian_name},

            This is to inform you that your ward, {ward_name}, has successfully changed their Kademia password.

            If you did not expect this change or have any concerns, please contact our support team.

            Best regards,
            Kademia Support Team

            This is an automated message. Please do not reply to this email.
        """

        return self.service.send_email(to_email, subject, html_body, text_body)


    def send_guardian_new_password(
            self, to_email: str, full_name: str, password: str
    ) -> bool:
        """Send email_service with guardian's new password after a reset."""

        subject = "Your new Kademia Password"

        html_body = f"""
            <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
                    .container {{ padding: 20px; }}
                    .header {{ background-color: #003366; color: white; padding: 10px; text-align: center; }}
                    .content {{ padding: 20px; }}
                    .button {{
                        background-color: #222;
                        color: #fff;
                        padding: 12px 24px;
                        text-align: center;
                        text-decoration: none;
                        display: inline-block;
                        font-weight: bold;
                        border-radius: 4px;
                        margin-top: 20px;
                    }}
                    .footer {{ font-size: 12px; color: #666; text-align: center; margin-top: 20px; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>Your new Kademia Password</h1>
                    </div>
                    <div class="content">
                        <p>Dear {full_name},</p>

                        <p>Your Kademia password has been changed. You can log in with the following password:</p>

                        <p><strong>Temporary Password:</strong> {password}</p>

                        <p><strong>Important:</strong> Please change your password immediately after your first login for security reasons.</p>

                        <p>If you have any questions or did not authorize this change, please click the button below to contact our support team:</p>

                        <a href="https://support.kademia.com" class="button">Get Help from Support</a>

                        <p>Best regards,<br>Kademia Support Team</p>
                    </div>
                    <div class="footer">
                        <p>This is an automated message. Please do not reply to this email_service.</p>
                    </div>
                </div>
            </body>
            </html>
        """

        text_body = f"""
            Your new Kademia Password

            Dear {full_name},

            Your Kademia password has been changed. You can log in with the following password:

            Email: {to_email}
            Temporary Password: {password}

            Important: Please change your password immediately after your first login for security reasons.

            If you have any questions or did not authorize this change, please visit https://support.kademia.com to contact the support team.

            Best regards,
            Kademia Administration Team

            This is an automated message. Please do not reply to this email_service.
        """

        return self.service.send_email(to_email, subject, html_body, text_body)



    def send_ward_new_password(
            self, to_email: str, full_name: str, password: str,
            ward_first_name: str, ward_last_name: str
    ) -> bool:

        """Send email student's new email to their guardian ."""

        subject = f"Password Reset for {ward_first_name} {ward_last_name}"

        html_body = f"""
            <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
                    .container {{ padding: 20px; }}
                    .header {{ background-color: #003366; color: white; padding: 10px; text-align: center; }}
                    .content {{ padding: 20px; }}
                    .button {{
                        background-color: #222;
                        color: #fff;
                        padding: 12px 24px;
                        text-align: center;
                        text-decoration: none;
                        display: inline-block;
                        font-weight: bold;
                        border-radius: 4px;
                        margin-top: 20px;
                    }}
                    .footer {{ font-size: 12px; color: #666; text-align: center; margin-top: 20px; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>Password Reset Notification</h1>
                    </div>
                    <div class="content">
                        <p>Dear {full_name},</p>

                        <p>This is to inform you that the password for your ward, <strong>{ward_first_name} {ward_last_name}</strong>, has been reset.</p>

                        <p><strong>Temporary Password:</strong> {password}</p>

                        <p><strong>Important:</strong> Please ensure your ward changes their password immediately after their next login for security reasons.</p>

                        <p>If you did not request this change, or need help, click the button below to reach our support team:</p>

                        <a href="https://support.kademia.com" class="button">Get Help from Support</a>

                        <p>Best regards,<br>Kademia Support Team</p>
                    </div>
                    <div class="footer">
                        <p>This is an automated message. Please do not reply to this email_service.</p>
                    </div>
                </div>
            </body>
            </html>
        """

        text_body = f"""
            Password Reset Notification

            Dear {full_name},

            This is to inform you that the password for your ward, {ward_first_name} {ward_last_name}, has been reset.

            Temporary Password: {password}

            Important: Please ensure your ward changes their password immediately after their next login for security reasons.

            If you have any questions or did not authorize this change, visit https://support.kademia.com to contact our support team.

            Best regards,
            Kademia Support Team

            This is an automated message. Please do not reply to this email_service.
        """

        return self.service.send_email(to_email, subject, html_body, text_body)


    def send_staff_reset_link(self, to_email: str, name: str, reset_url: str) -> bool:
        """Send email to staff with a password reset link."""

        subject = "Reset Your Kademia Password"

        html_body = f"""
            <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
                    .container {{ padding: 20px; }}
                    .header {{ background-color: #003366; color: white; padding: 10px; text-align: center; }}
                    .content {{ padding: 20px; }}
                    .button {{
                        background-color: #003366;
                        color: #fff;
                        padding: 12px 24px;
                        text-align: center;
                        text-decoration: none;
                        display: inline-block;
                        font-weight: bold;
                        border-radius: 4px;
                        margin-top: 20px;
                    }}
                    .footer {{ font-size: 12px; color: #666; text-align: center; margin-top: 20px; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>Password Reset Request</h1>
                    </div>
                    <div class="content">
                        <p>Dear {name},</p>

                        <p>We received a request to reset your Kademia account password.</p>

                        <p>If you made this request, please click the button below to reset your password. This link will expire in 15 minutes.</p>

                        <a href="{reset_url}" class="button">Reset Password</a>

                        <p>If you did not request a password reset, you can ignore this email_service. No changes have been made to your account.</p>

                        <p>Best regards,<br>Kademia Support Team</p>
                    </div>
                    <div class="footer">
                        <p>This is an automated message. Please do not reply to this email_service.</p>
                    </div>
                </div>
            </body>
            </html>
        """

        text_body = f"""
            Password Reset Request

            Dear {name},

            We received a request to reset your Kademia account password.

            If you made this request, use the link below to reset your password. This link will expire in 15 minutes:

            {reset_url}

            If you did not request a password reset, you can safely ignore this message. No changes have been made to your account.

            Best regards,
            Kademia Support Team

            This is an automated message. Please do not reply to this email_service.
        """

        return self.service.send_email(to_email, subject, html_body, text_body)



