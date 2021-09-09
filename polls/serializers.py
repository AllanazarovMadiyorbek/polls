from rest_framework import serializers
from .models import Question,Choice,Answer


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = [
            'id','question','text'
        ]

class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True,read_only=True)
    class Meta:
        model = Question
        fields = [
            'id','title','description','type','start_date','end_date','choices','answered_count'
        ]


class QuestionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = [
            'id','title','description','type','end_date'
        ]




class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = [
            'id','question','choice','user_id'
        ]

class AnswerListSerializer(serializers.ModelSerializer):
    question = QuestionUpdateSerializer(read_only=True)
    chosen_choices_by_user = ChoiceSerializer(read_only=True,many=True,source='choice')
    class Meta:
        model = Answer
        fields = [
            'id','question','chosen_choices_by_user','user_id'
        ]