from ..services.mailer import SendEmailTemplate
from typing import List

def SendGeneratedPasswordMail(password: str, recipient_list: List[str]):
    with open("../services/mail_templates/generated_pass.html", "r") as f:
      html_template = f.read()

    html_content = html_template.replace("{{password}}", password)
    subject = "Welcome to TrueFace"
    
    SendEmailTemplate(subject, html_content, recipient_list)
