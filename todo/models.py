from ckeditor.fields import RichTextField
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return f"{self.name}"


class Task(models.Model):
    content = RichTextField()
    is_done = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField(blank=True, null=True)
    tags = models.ManyToManyField(Tag, related_name="tasks")

    class Meta:
        ordering = ["is_done", "-created_at"]

    def clean(self) -> None:
        if self.deadline and self.deadline < timezone.now():
            raise ValidationError("The deadline cannot be in the past.")

    def save(
        self, *args, **kwargs
    ) -> None:
        self.full_clean()
        return super().save(
            *args, **kwargs
        )
