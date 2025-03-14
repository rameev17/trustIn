from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.utils.timezone import now
from .models import Project

class ProjectAdminForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'

    def clean_ending_at(self):
        ending_at = self.cleaned_data.get('ending_at')
        if ending_at and ending_at < now().date():
            raise ValidationError("The ending date cannot be in the past.")
        return ending_at

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    form = ProjectAdminForm
    list_display = ('title', 'donated_money', 'ending_at', 'is_active')
    list_filter = ('is_active', 'ending_at')
    search_fields = ('title', 'description')