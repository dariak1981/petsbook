from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
User = settings.AUTH_USER_MODEL
Profile = settings.AUTH_PROFILE_MODULE
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
User = get_user_model()

from .models import Post, Themes, Message
from analysis.mixins import ObjectViewedMixin

class PostListView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'allposts'
    ordering = ['-created']
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        context['featuredthreads'] = Post.objects.all().filter(is_featured=True)
        context['searchthreads'] = Themes.objects.all()
        return context


class FilterPostListView(ListView):
    model = Post
    ordering = ['-created']
    paginate_by = 5


    def get_context_data(self, **kwargs):
        context = super(FilterPostListView, self).get_context_data(**kwargs)
        filter_set = Post.objects.all().order_by('-created')
        page_size = self.get_paginate_by(filter_set)
        context_object_name = self.get_context_object_name(filter_set)

        if self.request.GET.get('keywords'):
            keywords = self.request.GET.get('keywords') or None
            if keywords:
                filter_set = filter_set.filter(content__icontains=keywords)

        if self.request.GET.get('title'):
            title = self.request.GET.get('title') or None
            if title:
                filter_set = filter_set.filter(title__icontains=title)

        if self.request.GET.get('theme'):
            theme = self.request.GET.get('theme')
            if theme:
                filter_set = filter_set.filter(theme_id=theme)
        if page_size:
            paginator, page, filter_set, is_paginated = self.paginate_queryset(filter_set, page_size)

            context['paginator'] = paginator
            context['page_obj'] = page
            context['is_paginated'] = is_paginated
            context['allposts'] = filter_set
            context['searchthreads'] = Themes.objects.all()
            context['featuredthreads'] = Post.objects.all().filter(is_featured=True)
            context['values']:request.GET
            return context

        else:
            context['paginator'] = None
            context['page_obj'] = None
            context['is_paginated'] = False
            context['allposts'] = filter_set
            context['searchthreads'] = Themes.objects.all()
            context['featuredthreads'] = Post.objects.all().filter(is_featured=True)
            context['values']:request.GET
            return context

        if context_object_name is not None:
            context[context_object_name] = filter_set
        context.update(kwargs)
        return super().get_context_data(**context)



class PostDetailView(ObjectViewedMixin, DetailView):
    model = Post
    paginate_by = 20

    def get_context_data(self, **kwargs):
            context = super(PostDetailView, self).get_context_data(**kwargs)
            messages = Message.objects.filter(post=self.kwargs.get('pk'))
            paginator = Paginator(messages, self.paginate_by)

            page = self.request.GET.get('page')

            try:
                replies = paginator.page(page)
            except PageNotAnInteger:
                replies = paginator.page(1)
            except EmptyPage:
                replies = paginator.page(paginator.num_pages)

            context['messages'] = replies
            return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'theme', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


@login_required
def createnewpost(request):
    threads = Themes.objects.all()
    posts = Post.objects.all()

    context = {
    'threads': threads,
    'posts': posts,
    }

    if request.method == "POST":
        author = request.user
        title = request.POST['title']
        theme = Themes.objects.get(id=request.POST['theme'])
        content = request.POST['content']
        photo = request.FILES.get('photo')

        newpost = Post(
        author=author, title=title, theme=theme, content=content, photo=photo)
        newpost.id
        newpost.save()

        # return redirect(reverse('blog', kwargs={'newpost':newpost.pk}))
        return redirect('post-detail', newpost.id)


    return render(request, 'blog/post_form.html', context)


@login_required
def updatepost(request, pk):
    editpost = Post.objects.get(pk=pk)
    threads = Themes.objects.all()

    context = {
    'threads': threads,
    'editpost': editpost,
    }

    if request.method == "POST":
        editpost.author = request.user
        editpost.title = request.POST['title']
        editpost.theme = Themes.objects.get(id=request.POST['theme'])
        editpost.content = request.POST['content']
        if 'image-clear' in request.POST:
            editpost.photo = None
        else:
            if request.FILES.get('photo'):
                editpost.photo = request.FILES.get('photo')
            else:
                editpost.photo = editpost.photo

        editpost.save()

        # return redirect(reverse('blog', kwargs={'newpost':newpost.pk}))
        return redirect('post-detail', editpost.id)


    return render(request, 'blog/post_edit.html', context)



class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/blog/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    fields = ['message']

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post_id = self.kwargs['post_id']
        return super().form_valid(form)

class MessageUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Message
    fields = ['message']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class MessageDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Message

    def get_success_url(self):
        post = self.object.post
        return reverse('post-detail', kwargs={'pk': post.id})

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False



class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'allposts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, email=self.kwargs.get('email'))
        return Post.objects.filter(author=user).order_by('-created')

    def get_context_data(self, **kwargs):
        context = super(UserPostListView, self).get_context_data(**kwargs)
        context['searchthreads'] = Themes.objects.all()
        context['featuredthreads'] = Post.objects.all().filter(is_featured=True)
        return context
