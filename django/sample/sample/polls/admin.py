from django.contrib import admin
from .models import Question, Choice

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3  # Shows 3 empty choice fields by default

class QuestionAdmin(admin.ModelAdmin):
    list_filter=["pub_date"]
    search_fields = ["question_text"]
    list_per_page=2
    inlines = [ChoiceInline]

admin.site.register(Question, QuestionAdmin)