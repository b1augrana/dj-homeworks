from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Article, Tag, Scope


class ScopeInlineFormset(BaseInlineFormSet):
    def clean(self):
        is_main = False
        for form in self.forms:
            if form.cleaned_data['is_main']:
                if is_main:
                    raise ValidationError('Только один раздел может быть основным')
                is_main = True
        return super().clean() 


class ScopeInline(admin.TabularInline):
    model = Scope
    formset = ScopeInlineFormset
    extra = 0



@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'text', 'published_at', 'image',]
    inlines = [ScopeInline,]
    
@admin.register(Tag)    
class TagAdmin(admin.ModelAdmin):
    list_display = ['name',]    
