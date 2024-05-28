from typing import Any

from django.db.models import QuerySet
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import generic, View

from todo.forms import TaskForm, TagSearchForm, TaskSearchForm
from todo.models import Task, Tag


class TaskListView(generic.ListView):
    model = Task
    paginate_by = 5

    def get_context_data(
            self, *, object_list=None, **kwargs
    ) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        content = self.request.GET.get("content", "")
        context["search_form"] = TaskSearchForm(initial={"content": content})
        return context

    def get_queryset(self) -> QuerySet[Task]:
        queryset = Task.objects.prefetch_related("tags")
        form = TaskSearchForm(self.request.GET)
        if form.is_valid():
            queryset = queryset.filter(
                content__icontains=form.cleaned_data["content"]
            )
        return queryset


class TaskCreateView(generic.CreateView):
    model = Task
    form_class = TaskForm
    template_name = "todo/task_form.html"
    success_url = reverse_lazy("task-list")


class TaskUpdateView(generic.UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "todo/task_form.html"
    success_url = reverse_lazy("task-list")


class TaskDeleteView(generic.DeleteView):
    model = Task
    success_url = reverse_lazy("task-list")


class TaskCompleteView(View):
    def post(
            self, request, *args, **kwargs
    ) -> HttpResponsePermanentRedirect | HttpResponseRedirect:
        task = get_object_or_404(Task, pk=self.kwargs["pk"])

        task.is_done = not task.is_done

        task.save()
        return HttpResponseRedirect(reverse_lazy("task-list"))


class TagListView(generic.ListView):
    model = Tag
    context_object_name = "tag_list"
    paginate_by = 10

    def get_context_data(
            self, *, object_list=None, **kwargs
    ) -> dict[str, Any]:
        context = super(TagListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = TagSearchForm(initial={"name": name})
        return context

    def get_queryset(self) -> Any:
        queryset = Tag.objects
        form = TagSearchForm(self.request.GET)
        if form.is_valid():
            queryset = queryset.filter(
                name__icontains=form.cleaned_data["name"]
            )
        return queryset


class TagCreateView(generic.CreateView):
    model = Tag
    fields = ("name",)
    success_url = reverse_lazy("tag-list")


class TagUpdateView(generic.UpdateView):
    model = Tag
    fields = ("name",)
    success_url = reverse_lazy("tag-list")


class TagDeleteView(generic.DeleteView):
    model = Tag
    success_url = reverse_lazy("tag-list")
