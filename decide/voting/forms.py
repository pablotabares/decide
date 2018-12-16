from django import forms
from voting.models import Question, QuestionOption, Voting


#TODO: agrupar en un solo formulario
class QuestionForm(forms.Form):
    name_voting = forms.CharField()
    desc_voting = forms.CharField()

    name_auth = forms.CharField()
    url_auth = forms.URLField()

    desc_question = forms.CharField()


class VotingForm2(forms.Form):

    CHOICES = [(True, 'True'), (False, 'False')]

    name_voting = forms.CharField()
    desc_voting = forms.CharField()
    is_weighted = forms.ChoiceField(choices=CHOICES)
    #start_date = forms.DateTimeField()
    #end_date = forms.DateTimeField()

    questions_ = forms.ModelMultipleChoiceField(queryset=Question.objects.all())

    name_auth = forms.CharField()
    url_auth = forms.URLField()


class QuestionOptionsForm(forms.ModelForm):
    class Meta:
        model = QuestionOption

        fields = [
            'question',
            'number',
            'weight',
            'option'
        ]
        labels = {
            'question': 'Question',
            'number': 'Number',
            'weight': 'Weight',
            'option': 'Option Text'
        }
        widgets = {
            'weight': forms.TextInput(),
            'option': forms.TextInput(),
            'number': forms.HiddenInput(),
            'question': forms.HiddenInput()
        }


class VotingForm(forms.ModelForm):
    class Meta:
        model = Voting

        fields = [
            'name',
            'desc',
            'isWeighted',
            'start_date',
            'end_date'
        ]

        labels = {
            'name' : 'Name',
            'desc' : 'Description',
            'isWeighted' : 'Is weighted',
            'start_date' : 'Start date',
            'end date' : 'End date'
        }
        widgets = {
            'name' : forms.TextInput(),
            'desc' : forms.TextInput(),
            'isWeighted' : forms.CheckboxInput(),
            'start date' : forms.DateInput(),
            'end date' : forms.DateInput()
        }


class someQuestionsOptions(forms.Form):
    description = forms.CharField()
    number = forms.CharField(widget=forms.HiddenInput)
    lista = list()
    option = QuestionOptionsForm()
    for i in range(0, 3):
        lista.append(option)
