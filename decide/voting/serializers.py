from rest_framework import serializers
from .models import Question, QuestionOption, Voting
from base.serializers import KeySerializer, AuthSerializer

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
        fields = ('id','desc', 'options')


class VotingSerializer(serializers.HyperlinkedModelSerializer):
    questions = QuestionSerializer(many=True)
    pub_key = KeySerializer()
    auths = AuthSerializer(many=True)
    class Meta:
        model = Voting
        fields = ('id', 'name', 'desc', 'questions', 'start_date',
                  'end_date', 'pub_key', 'auths', 'tally', 'postproc')
