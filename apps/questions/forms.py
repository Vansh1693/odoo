from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Row, Column
from .models import Question


class QuestionForm(forms.ModelForm):
    """
    Form for creating and editing questions.
    """
    class Meta:
        model = Question
        fields = ['title', 'content', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Be specific and imagine you\'re asking a question to another person'
            }),
            'tags': forms.TextInput(attrs={
                'placeholder': 'e.g. python django javascript (max 5 tags)'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('title', css_class='form-control-lg'),
            Field('content'),
            Field('tags', css_class='form-control'),
            Submit('submit', 'Post Question', css_class='btn btn-primary btn-lg')
        )

    def clean_tags(self):
        tags = self.cleaned_data.get('tags')
        if tags:
            tag_list = [tag.strip() for tag in tags.split(',') if tag.strip()]
            if len(tag_list) > 5:
                raise forms.ValidationError("Maximum 5 tags allowed.")
            return ','.join(tag_list)
        return tags
