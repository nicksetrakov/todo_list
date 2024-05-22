from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
from todo.models import Task, Tag


class Command(BaseCommand):
    help = 'Generate fake data'

    def handle(self, *args, **kwargs) -> None:
        fake = Faker()

        total_tags = 20
        total_tasks = 100

        for _ in range(total_tags):
            name = fake.word()
            tag, create = Tag.objects.get_or_create(name=name)
            if create:
                tag.save()

        for _ in range(total_tasks):
            content = fake.text()
            is_done = fake.boolean(chance_of_getting_true=50)
            created_at = timezone.now()
            deadline = fake.future_datetime(
                end_date='+30d', tzinfo=timezone.get_current_timezone()
            ) if not is_done else None
            task = Task.objects.create(
                content=content,
                is_done=is_done,
                created_at=created_at,
                deadline=deadline
            )
            task.tags.add(
                *Tag.objects.order_by("?")[:fake.random_int(min=1, max=3)]
            )
            task.save()

        self.stdout.write(self.style.SUCCESS(
            "Successfully generated fake data"
        ))
