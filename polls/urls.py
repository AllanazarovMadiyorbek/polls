from django.urls import path,include
from rest_framework.routers import SimpleRouter

from polls.views import QuestionViewSet,ChoiceViewSet,ActivePollsAPIView,AnswerViewSet,UserAnsweredPollsAPIView

router = SimpleRouter()

router.register('answers', AnswerViewSet)
router.register('choices', ChoiceViewSet)
router.register('', QuestionViewSet)

urlpatterns = [
    path('active-polls/', ActivePollsAPIView.as_view(), name='active-polls'),
    path('user-answered/<int:user_id>/', UserAnsweredPollsAPIView.as_view(), name='active-polls'),
    path('', include(router.urls)),
]
