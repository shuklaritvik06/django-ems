from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import BooksModel
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin


class BooksListView(LoginRequiredMixin, ListView):
    model = BooksModel
    context_object_name = "books"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = context['books'].filter(user=self.request.user)
        return context


class BooksDetailView(LoginRequiredMixin, DetailView):
    model = BooksModel
    context_object_name = "book"


class BooksCreateView(LoginRequiredMixin, CreateView):
    model = BooksModel
    fields = ["name", "description"]
    success_url = reverse_lazy("books")
    template_name = "create.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "The book was created successfully.")
        return super(BooksCreateView, self).form_valid(form)


class BookUpdateView(LoginRequiredMixin, UpdateView):
    model = BooksModel
    fields = ["name", "description"]
    success_url = reverse_lazy("books")
    template_name = "update.html"
    slug_field = "slug"
    context_object_name = "book"

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "The book was updated successfully.")
        return super(BookUpdateView, self).form_valid(form)


class BookDeleteView(LoginRequiredMixin, DeleteView):
    model = BooksModel
    success_url = reverse_lazy("books")
    slug_field = "slug"
    # Change the name of the template to be rendered (default -> book_confirmation_delete)
    template_name = "delete_confirm.html"
    # Which name object is passed to the template
    context_object_name = "book"
