from django.contrib import admin
from .models import Question,Choice,Answer
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class ChoiceAdminInlineAdmin(admin.TabularInline):
    model = Choice
    extra = 0
    show_change_link = True


class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description','start_date','end_date']

    fieldsets = (
        (None, {'fields': ('title', 'description',
                           'type', 'end_date')}),

    )
    inlines = [ChoiceAdminInlineAdmin, ]


admin.site.register(Question,QuestionAdmin)
admin.site.register(Choice)