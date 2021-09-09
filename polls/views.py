from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from utility.paginations import DefaultLimitOffsetPagination
from utility.permissions import IsAdminOrReadOnly
from .models import Question,Choice,Answer
from .serializers import QuestionSerializer, ChoiceSerializer, AnswerSerializer, QuestionUpdateSerializer, \
    AnswerListSerializer
from rest_framework.views import APIView
import datetime


class QuestionViewSet(ModelViewSet):
    """## Endoint to manage Questions: [CRUD, ]
        - Permissions:
            - Admins: [GET, GET(id), POST, PUT, PATCH, DELETE]
            - Anybody: [GET, GET(id), ]
        - FYI: this endpoint uses limit offset pagination. By defaultlimit = 10
        - Created instance's start_date can't be updated
    """
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = DefaultLimitOffsetPagination

    def get_serializer_class(self):
        if self.action == 'update' or self.action == 'partial_update':
            return QuestionUpdateSerializer
        else:
            return QuestionSerializer


class ChoiceViewSet(ModelViewSet):
    """## Endoint to manage Choices: [CRUD, ]
        - Permissions:
            - Admins: [GET, GET(id), POST, PUT, PATCH, DELETE]
            - Anybody: [GET, GET(id), ]
        - FYI: this endpoint uses limit offset pagination. By defaultlimit = 10
    """
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = DefaultLimitOffsetPagination

class AnswerViewSet(ModelViewSet):
    """## Endoint to manage Answers: [CRUD, ]
        - Permissions:
            - Anybody: [GET, GET(id), POST, PUT, PATCH, DELETE]
        - FYI: this endpoint uses limit offset pagination. By defaultlimit = 10
    """
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = (AllowAny,)
    pagination_class = DefaultLimitOffsetPagination

    def create(self, request, *args, **kwargs):
        """
        To create Answer instance: please provide with:
            'question':1
            'choice':[1,2] - choosed choices
            'user_id': 15 - given unique id from client side
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        answer = Answer.objects.get(id=serializer.data.get('id'))
        question = answer.question
        question.answered_count+=1
        question.save(update_fields=['answered_count'])
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        question = instance.question
        question.answered_count-=1
        question.save(update_fields=['answered_count'])
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ActivePollsAPIView(APIView):

    def get(self,request):
        today = datetime.datetime.today()
        active_polls = Question.objects.filter(end_date__gte=today)
        serializer = QuestionSerializer(active_polls,many=True)
        return Response(serializer.data)


class UserAnsweredPollsAPIView(APIView):
    """
        Enpoind gives you all user answered polls
    """
    def get(self,request,user_id):
        user_answered_polls = Answer.objects.filter(user_id=user_id)
        paginator = DefaultLimitOffsetPagination()
        return paginator.generate_response(user_answered_polls, AnswerListSerializer, request)


