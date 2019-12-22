from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import DetailView, UpdateView, DeleteView
from django.contrib.auth import get_user_model
from django.views import View
from .models import Profile
from django.urls import reverse_lazy
from django.forms.utils import ErrorList
from django import forms
from django.core.exceptions import PermissionDenied
from .forms import UpdateProfileForm, UpdateUserForm
from django import http

User = get_user_model()
toggle_user = None


class UserDetailsUpdateView(UpdateView):
    template_name = "user/user_update.html"
    form_class = UpdateUserForm
    model = User
    slug_field = 'username'

    def get_context_data(self, *args, **kwargs):
        context = super(UserDetailsUpdateView,
                        self).get_context_data(*args, **kwargs)
        if context['user'] != self.request.user:
            raise PermissionDenied
        return context

    def get_success_url(self, *args, **kwargs):
        return reverse_lazy("upd-user", kwargs={'slug': self.request.user.username})


class UserProfileDetailsUpdateView(UpdateView):
    template_name = "user/user_profile_update.html"
    form_class = UpdateProfileForm
    model = Profile

    def get_context_data(self, *args, **kwargs):
        context = super(UserProfileDetailsUpdateView,
                        self).get_context_data(*args, **kwargs)
        print(context)
        if str(context['profile']) != str(int(self.request.user.pk)):
            raise PermissionDenied
        return context

    def get_success_url(self, *args, **kwargs):
        # context['profile']
        return reverse_lazy("upd-profile", kwargs={'pk': self.request.user.profile.user.id})


class UserDeleteView(DeleteView):
    model = User
    template_name = "user/user_delete_view.html"
    slug_field = 'username'
    success_url = reverse_lazy("account_login")

    def delete(self, request, *args, **kwargs):
        print("Users for delete are ", self.kwargs['slug'], self.request.user)
        if str(self.kwargs['slug']) == str(self.request.user.username):
            u = User.objects.get(username=self.request.user.username)
            u.delete()
            return redirect("account_login")
        else:
            # raise PermissionDenied
            return http.HttpResponseForbidden("Cannot delete other's account")


class UserDetailView(DetailView):
    queryset = User.objects.all()
    template_name = "user/user_profile.html"
    slug_field = 'username'

    def get_context_data(self, *args, **kwargs):
        context = super(UserDetailView, self).get_context_data(*args, **kwargs)
        context['following'] = Profile.objects.is_following(
            self.request.user, self.kwargs['slug'])
        user_profile = Profile.objects.get(user=self.request.user)
        context["followusers"] = [
            user.username for user in user_profile.following.all()]
        print("Followed by:", context["followusers"])
        # print("get_context_data",self.args, self.kwargs,self.request.user,self.kwargs['slug'])
        print(context)
        return context


class UserFollowView(View):
    def get(self, request, slug, *args, **kwargs):
        print(*args, **kwargs)
        toggle_user = get_object_or_404(User, username__iexact=slug)
        if request.user.is_authenticated:
            print("Hey", request.user, toggle_user)
            is_following = Profile.objects.toggle_follow(
                request.user, toggle_user)
        return redirect("user-profile", slug=self.request.user.username)


class UserFollowRemoveView(View):
    def get(self, request, slug, *args, **kwargs):
        print(*args, **kwargs)
        toggle_user = get_object_or_404(User, username__iexact=slug)
        if request.user.is_authenticated:
            print("Hey", request.user, toggle_user)
            is_following = Profile.objects.toggle_remove_follow(
                request.user, toggle_user)
        return redirect("user-profile", slug=self.request.user.username)


def home(request):
    count = User.objects.count()
    # return render(request,'home.html',{
    #     'user_count':count
    # })
    return redirect("account_login")


@login_required(login_url='account_login')
def secret_page(request):
    return render(request, 'secret_page.html')


@login_required(login_url='account_login')
def settings(request):
    return HttpResponseRedirect(reverse("upd-user", kwargs={'slug': request.user.username}))
