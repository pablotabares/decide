from django import forms
from voting.models import Question


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question

        fields = [
            'desc',
            'referendum'
        ]
        labels = {
            'desc': 'Descripcion',
            'referendum': 'Referendum'
        }
        widgets = {
            'desc': forms.TextInput(),
            'referendum': forms.HiddenInput()
        }
