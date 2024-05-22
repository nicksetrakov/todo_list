from ckeditor.widgets import CKEditorWidget
from django import forms

from todo.models import Task, Tag


class TaskSearchForm(forms.Form):
    content = forms.CharField(
        max_length=63,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by content"}),
    )


class TagSearchForm(forms.Form):
    name = forms.CharField(
        max_length=63,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by name"}),
    )


class TaskForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())

    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    deadline = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={"class": "form-control", "type": "datetime-local"}
        ),
        input_formats=["%Y-%m-%dT%H:%M"],
        required=False
    )

    class Meta:
        model = Task
        fields = [
            "content",
            "deadline",
            "tags",
        ]
