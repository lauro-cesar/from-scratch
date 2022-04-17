from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class RestfilesConfig(AppConfig):
	name = 'restfiles'
	verbose_name=_('Restfiles')

	def ready(self):
		import restfiles.signals
