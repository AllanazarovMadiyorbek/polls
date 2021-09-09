from django.db import models
from django.utils.translation import ugettext_lazy as _


class Question(models.Model):
    QUESTION_ANSWER_CHOICES = [
        ("T", 'TEXT ANSWER'),
        ("S", "SINGLE CHOICE ANSWER"),
        ("M", "MULTIPLE CHOICE"),
    ]

    title = models.CharField(max_length=255,verbose_name='Название')
    description = models.TextField(blank=True,null=True,verbose_name='описание')
    type = models.CharField(max_length=5, choices=QUESTION_ANSWER_CHOICES, default="S",verbose_name='тип')
    start_date = models.DateTimeField(verbose_name='дата старта')
    end_date = models.DateTimeField(verbose_name='дата окончания')
    answered_count = models.PositiveIntegerField(default=0)
    def __str__(self):
        return self.title

class Choice(models.Model):
    question = models.ForeignKey(Question,on_delete=models.CASCADE,related_name='choices')
    text = models.CharField(max_length=512,verbose_name='текст')


class Answer(models.Model):
    question = models.ForeignKey(Question,on_delete=models.CASCADE,related_name='answers')
    choice = models.ManyToManyField(Choice,related_name='answers')
    user_id = models.IntegerField(verbose_name='числовой ID')

    class Meta:
        unique_together = ('question', 'user_id')
        verbose_name = _('ответ')
        verbose_name_plural = _('ответы')

    def __str__(self):
        return f"ответ- {self.question.title}"