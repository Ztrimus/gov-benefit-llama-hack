from restack_ai.function import function, log
from mailersend import emails

# Initialize MailerSend email client
mailer = emails.NewEmail()

@function.defn(name="send_email")
def send_email(to_email: str, to_name: str, subject: str, html_content: str, text_content: str, from_email: str = "your@domain.com", from_name: str = "Your Name") -> str:
    """
    Sends an email with the specified details using MailerSend.
    
    Args:
        to_email (str): Recipient's email address.
        to_name (str): Recipient's name.
        subject (str): Subject of the email.
        html_content (str): HTML content of the email.
        text_content (str): Plain text content of the email.
        from_email (str): Sender's email address.
        from_name (str): Sender's name.
        
    Returns:
        str: Status message of the email sending operation.
    """
    try:
        # Prepare the mail body
        mail_body = {}
        
        # Set sender details
        mail_from = {
            "name": from_name,
            "email": from_email,
        }
        mailer.set_mail_from(mail_from, mail_body)

        # Set recipient details
        recipients = [
            {
                "name": to_name,
                "email": to_email,
            }
        ]
        mailer.set_mail_to(recipients, mail_body)

        # Set email subject and content
        mailer.set_subject(subject, mail_body)
        mailer.set_html_content(html_content, mail_body)
        mailer.set_plaintext_content(text_content, mail_body)

        # Optional: Set reply-to address
        reply_to = {
            "name": from_name,
            "email": from_email,
        }
        mailer.set_reply_to(reply_to, mail_body)

        # Send the email and log the response
        response = mailer.send(mail_body)
        log.info("send_email", extra={"status": "Email sent successfully", "to_email": to_email, "subject": subject})

        return response

    except Exception as e:
        # Log any exceptions and return an error message
        log.error("send_email function failed", extra={"error": str(e), "to_email": to_email, "subject": subject})
        return f"Error occurred while sending email: {e}"
