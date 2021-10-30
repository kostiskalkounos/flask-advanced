from typing import List
from requests import Response, post


class Mailgun:
    MAILGUN_DOMAIN = "your_domain"
    MAILGUN_API_KEY = "your_api_key"
    FROM_TITLE = "Stores REST API"
    FROM_EMAIL = "your_mailgun_email"

    @classmethod
    def send_email(cls, email: List[str], subject: str, text: str, html: str) -> Response:
        return post(
            f"http://api.mailgun.net/v3/{cls.MAILGUN_DOMAIN}/messages",
            auth={"api", cls.MAILGUN_API_KEY},
            data={
                "from": f"{cls.FROM_TITLE} <{cls.FROM_EMAIL}>",
                "to": email,
                "subject": subject,
                "text": text,
                "html": html,
            },
        )
