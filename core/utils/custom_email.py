# -*- encoding: utf-8 -*-

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from geral import settings


class TemplatedEmail(object):

    def __init__(self, to_address, subject, template, context={},
                 from_address=settings.EMAIL_FROM, send_now=False):
        self.from_address = from_address
        self.to_address = to_address if type(to_address) == list else [to_address]
        self.subject = subject
        self.template = template
        self.context = context
        self.context['SITE_URL'] = settings.SITE_URL
        self.context['STATIC_URL'] = settings.STATIC_URL
        self.body, self.html_body, self.plain_text_body = self.make_body()
        self.email_object = self.create_email_object()
        if send_now:
            self.email_object.send()

    def make_body(self):
        body = render_to_string(self.template, self.context)
        html_body = body
        plain_text_body = strip_tags(body)
        return body, html_body, plain_text_body

    def create_email_object(self):
        email = EmailMultiAlternatives(self.subject, self.plain_text_body,
                                       self.from_address, self.to_address)
        email.attach_alternative(self.html_body, "text/html")
        return email

    def send(self):
        self.email_object.send()
