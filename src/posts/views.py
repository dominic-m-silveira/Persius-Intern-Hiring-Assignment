from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from .forms import PostModelForm
from .mixins import FormUserNeededMixin, UserOwnerMixin
from .models import Post


class PostListAndCreateView(FormUserNeededMixin, CreateView):
    template_name = "posts/post_list_create_view.html"
    form_class = PostModelForm
    # queryset = Post.objects.all()
    # success_url = reverse_lazy("post:list")
    login_url = reverse_lazy("account_login")
    model=Post

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object_list"] = self.model.objects.all()
        return context


class PostUpdateView(LoginRequiredMixin, UserOwnerMixin, UpdateView):
    queryset = Post.objects.all()
    template_name = "posts/post_update_view.html"
    form_class = PostModelForm
    # success_url = reverse_lazy("post:list")


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = "posts/post_delete_view.html"
    success_url = reverse_lazy("post:list")

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.user == self.request.user:
            self.object.delete()
            return HttpResponseRedirect(self.get_success_url())
        else:
            raise PermissionDenied


class PostDetailView(DetailView):
    template_name = 'posts/post_detail_view.html'
    queryset = Post.objects.all()

    def get_object(self):
        print(self.kwargs)
        pk = self.kwargs.get("pk")
        obj = get_object_or_404(Post, id=pk)
        return obj

    def get_context_data(self, *args, **kwargs):
        context = super(PostDetailView, self).get_context_data(*args, **kwargs)
        print(context)
        return context

