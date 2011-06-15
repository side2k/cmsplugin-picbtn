from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from models import PicButton
from forms import PicButtonForm
from django.utils.translation import ugettext as _
from cms.plugins.text.settings import USE_TINYMCE
from cms.plugins.text.widgets.wymeditor_widget import WYMEditor
from django.forms.fields import CharField
from django.conf import settings
from cms.plugins.text.utils import plugin_tags_to_user_html

class PicButtonPlugin(CMSPluginBase):
	model = PicButton
	name = _("Picture button")
	render_template = "plugins/cmsplugin_picbtn/picbtn.html"
	
	def get_editor_widget(self, request, plugins):
		"""
		Returns the Django form Widget to be used for
		the text area
		"""
		if USE_TINYMCE and "tinymce" in settings.INSTALLED_APPS:
			from cms.plugins.text.widgets.tinymce_widget import TinyMCEEditor
			return TinyMCEEditor(installed_plugins=plugins)
		else:
			return WYMEditor(installed_plugins=plugins)
			
	def get_form_class(self, request, plugins):
		"""
		Returns a subclass of Form to be used by this plugin
		"""
		# We avoid mutating the Form declared above by subclassing
		class PicButtonForm(self.form):
			pass
		widget = self.get_editor_widget(request, plugins)
		PicButtonForm.declared_fields["body"] = CharField(widget=widget, required=False)
		return PicButtonForm
		
	def get_form(self, request, obj=None, **kwargs):
		page = None
		if obj:
			page = obj.page
		plugins = plugin_pool.get_text_enabled_plugins(self.placeholder)
		form = self.get_form_class(request, plugins)
		kwargs['form'] = form # override standard form
		return super(CMSPluginBase, self).get_form(request, obj, **kwargs)			
		
	def render(self, context, instance, placeholder):
		context.update({
			'button': instance,
			'placeholder': placeholder,
			'body':plugin_tags_to_user_html(instance.body, context, placeholder),
			'link': instance.page_link.get_absolute_url()})
		return context

plugin_pool.register_plugin(PicButtonPlugin)