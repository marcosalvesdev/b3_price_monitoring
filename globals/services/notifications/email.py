from django.core.mail import EmailMessage
from django.template.loader import render_to_string


class EmailNotificationService:
    """
    Simple email notification service using Django's send_mail.
    """

    def format_html_template(self, template_name: str, context: dict) -> str:
        """
        Converts a Django template into an HTML string for email content.
        :param template_name: The name of the Django template to render.
        :param context: A dictionary of context variables to pass to the template.
        :return: A string containing the rendered HTML content.
        """
        return render_to_string(template_name, context)

    def send_email_with_html_content(
        self,
        template_name: str,
        context: dict,
        subject: str,
        recipient_list: list,
        from_email: str = None,
    ):
        """
        Sends an email with HTML content rendered from a Django template.
        :param template_name: The name of the Django template to render for the email body.
        :param context: A dictionary of context variables to pass to the template.
        :param subject: The subject of the email.
        :param recipient_list: A list of recipient email addresses.
        :param from_email: The sender's email. If None, the default from_email will be used.
        """
        html_content = self.format_html_template(template_name, context)
        email = EmailMessage(
            subject=subject,
            body=html_content,
            to=recipient_list,
            from_email=from_email,
        )
        email.content_subtype = "html"
        return email.send()
