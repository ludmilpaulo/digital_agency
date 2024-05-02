# translation.py

from modeltranslation.translator import register, TranslationOptions
from .models import AboutUs

@register(AboutUs)
class AboutUsTranslationOptions(TranslationOptions):
    fields = ('title')
