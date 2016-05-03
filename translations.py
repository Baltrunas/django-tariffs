from modeltranslation.translator import translator
from modeltranslation.translator import TranslationOptions

# from .models import TariffAddition
# from .models import Tariff


class TariffAdditionTranslationOptions(TranslationOptions):
	fields = ['name', 'description', 'price']

translator.register(TariffAddition, TariffAdditionTranslationOptions)


class TariffTranslationOptions(TranslationOptions):
	fields = ['title', 'sub_title', 'price_after', 'description', 'options']

translator.register(Tariff, TariffTranslationOptions)
