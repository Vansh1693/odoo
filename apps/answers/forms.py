from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit
from .models import Answer


class AnswerForm(forms.ModelForm):
    """
    Form for creating and editing answers.
    """
    class Meta:
        model = Answer
        fields = ['content']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('content'),
            Submit('submit', 'Post Answer', css_class='btn btn-primary')
        )
