from rest_framework import serializers
from .models import Question, QuestionOption, Voting
from base.serializers import KeySerializer, AuthSerializer
"""
class UnlockQuestionOptionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = QuestionOption
        fields = ('number', 'option')
class UnlockQuestionSerializer(serializers.HyperlinkedModelSerializer):
    options = UnlockQuestionOptionSerializer(many=True)
    class Meta:
        model = Question
        fields = ('desc', 'options')
class QuestionOptionSerializer(serializers.HyperlinkedModelSerializer):
    unlockquestion= UnlockQuestionSerializer(many=True)
    class Meta:
        model = QuestionOption
        fields = ('number', 'option', 'unlockquestion')
class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    options = QuestionOptionSerializer(many=True)
    class Meta:
        model = Question
        fields = ('desc', 'options')"""
class UnlockQuestionOptionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = QuestionOption
        fields = ('number', 'option', 'weight', 'importance')
class UnlockQuestionSerializer(serializers.HyperlinkedModelSerializer):
    options = UnlockQuestionOptionSerializer(many=True)
    class Meta:
        model = Question
        fields = ('desc', 'options')
class QuestionOptionSerializer(serializers.HyperlinkedModelSerializer):
    unlockquestion= UnlockQuestionSerializer(many=True)
    class Meta:
        model = QuestionOption
        fields = ('number', 'option', 'weight', 'importance', 'unlockquestion')
class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    options = QuestionOptionSerializer(many=True)
    class Meta:
        model = Question
        fields = ('desc', 'options')
"""class Question(models.Model):
    desc = models.TextField()
    def __str__(self):
        return self.desc
class QuestionOption(models.Model):
    question = models.ForeignKey(Question, related_name='options', on_delete=models.CASCADE)
    unlockquestion = models.ManyToManyField(Question, related_name='unlockquestion', null=True, blank=True)
    number = models.PositiveIntegerField(blank=True, null=True)
    #Adding the weight of this option
    weight = models.IntegerField( blank=False, null=True)
    importance = models.FloatField(choices=IMPORTANCE_CHOICES, default=0)
    option = models.TextField()
    def save(self):
        if not self.number:
            self.number = self.question.options.count() + 2
        return super().save()
    def __str__(self):
        return '{} ({})'.format(self.option, self.number)"""
class VotingSerializer(serializers.HyperlinkedModelSerializer):
    questions = QuestionSerializer(many=True)
    pub_key = KeySerializer()
    auths = AuthSerializer(many=True)
    class Meta:
        model = Voting
        fields = ('id', 'name', 'desc', 'isWeighted', 'questions', 'start_date',
                  'end_date', 'pub_key', 'auths', 'tally', 'postproc')