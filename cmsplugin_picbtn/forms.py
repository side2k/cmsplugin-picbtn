from django.forms.models import ModelForm
from models import PicButton
from django import forms


class PicButtonForm(ModelForm):
	body = forms.CharField()

	class Meta:
		model = PicButton
		#exclude = ('page', 'position', 'placeholder', 'language', 'plugin_type')