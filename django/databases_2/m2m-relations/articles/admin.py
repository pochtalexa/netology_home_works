from django.contrib import admin
from .models import Article, Tag, ArticleTag
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet
import json


class RelationshipInlineFormset(BaseInlineFormSet):
    def clean(self):
        is_main_counter = 0
        for form in self.forms:
            # В form.cleaned_data будет словарь с данными
            # каждой отдельной формы, которые вы можете проверить
            is_main = form.cleaned_data.get('is_main')
            if is_main:
                is_main_counter += 1
            # вызовом исключения ValidationError можно указать админке о наличие ошибки
            # таким образом объект не будет сохранен,
            # а пользователю выведется соответствующее сообщение об ошибке
        if is_main_counter != 1:
            raise ValidationError('Должен быть только один основной раздел!')

        return super().clean()  # вызываем базовый код переопределяемого метода


class ArticleInline(admin.TabularInline):
    # model = Article.tag.through
    model = ArticleTag
    formset = RelationshipInlineFormset
    extra = 1


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [
        ArticleInline
    ]
    exclude = ('tag',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    inlines = [
        ArticleInline
    ]
