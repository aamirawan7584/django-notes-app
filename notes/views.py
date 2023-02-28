from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Note

import logging

logger = logging.getLogger(__name__)


class NoteList(LoginRequiredMixin, ListView):
    model = Note
    context_object_name = "notes"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["notes"] = context["notes"].filter(user=self.request.user)
        # total notes for this user
        context["count"] = context["notes"].count()

        search_input = self.request.GET.get("search-area") or ""
        if search_input:
            context["notes"] = context["notes"].filter(title__contains=search_input)

        context["search_input"] = search_input

        return context


class NoteDetail(LoginRequiredMixin, DetailView):
    model = Note
    context_object_name = "note"
    template_name = "notes/note.html"


class NoteCreate(LoginRequiredMixin, CreateView):
    model = Note
    fields = ["title", "description"]
    success_url = reverse_lazy("notes")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(NoteCreate, self).form_valid(form)


class NoteUpdate(LoginRequiredMixin, UpdateView):
    model = Note
    fields = ["title", "description"]
    success_url = reverse_lazy("notes")


class NoteDelete(LoginRequiredMixin, DeleteView):
    model = Note
    context_object_name = "notes"
    success_url = reverse_lazy("notes")

    def get_queryset(self):
        owner = self.request.user
        return self.model.objects.filter(user=owner)
