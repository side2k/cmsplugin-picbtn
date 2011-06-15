from django.db import models
from django.utils.translation import ugettext_lazy as _
from cms.models import CMSPlugin, Page
	
# Create your models here.
class PicButton(CMSPlugin):
	PICBUTTON_AVAILABLE_BACKGROUNDS = (
		("blank", "Blank"),
		("globe", "Globe"),
		("checkboxes", "Checkboxes"),
		("lifering", "Lifering"))
	header = models.CharField(max_length=50)
	body = models.TextField(_("body"))
	def _set_body_admin(self, text):
		self.body = plugin_admin_html_to_tags(text)

	def _get_body_admin(self):
		return plugin_tags_to_admin_html(self.body)

	body_for_admin = property(
		_get_body_admin, _set_body_admin, None,
		"""
		body attribute, but with transformations
		applied to allow editing in the
		admin. Read/write.
		""")	
	
	page_link = models.ForeignKey(Page)
	background = models.CharField(
		max_length=50,
		verbose_name="Background", 
		choices=PICBUTTON_AVAILABLE_BACKGROUNDS)