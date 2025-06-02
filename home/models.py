from django.db import models
from django.utils import timezone
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel


class UserWeight(models.Model):
    telegram_user_id = models.BigIntegerField(unique=True)
    weight = models.FloatField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"User {self.telegram_user_id}: {self.weight} кг"


class HealthTip(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text[:50]


class HomePage(Page):
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        context['health_bot_page'] = HealthBotPage.objects.live().first()
        return context


class HealthBotPage(Page):
    intro = RichTextField(blank=True)

    parent_page_types = ['home.HomePage']
    subpage_types = []

    content_panels = Page.content_panels + [
        FieldPanel("intro", heading='Введение'),
    ]

    def get_template(self, request, *args, **kwargs):
        return "home/health_bot_page.html"  # обязательно совпадает с путём шаблона



class Advice(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:50]
