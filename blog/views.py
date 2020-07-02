from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, RedirectView
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
from tags.models import Tag

class PostListView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'allposts'
    ordering = ['-created']
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        context['searchthreads'] = Themes.objects.all()
        return context

class PostSearchView(ListView):
    model = Post
    context_object_name = 'allposts'
    paginate_by = 9

    def get_context_data(self, *args, **kwargs):
        context = super(PostSearchView, self).get_context_data(*args, **kwargs)
        context['tags'] = Tag.objects.all()
        context['searchthreads'] = Themes.objects.all()
        context['query'] = self.request.GET.get('q')
        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        method_dict = request.GET
        query = method_dict.get('q', None)
        if query is not None:
            return Post.objects.search(query)
        return Post.objects.all()

class PostTagView(ListView):
    model = Post
    context_object_name = 'allposts'
    paginate_by = 9

    def get_context_data(self, *args, **kwargs):
        context = super(PostTagView, self).get_context_data(*args, **kwargs)
        context['tags'] = Tag.objects.all()
        context['searchthreads'] = Themes.objects.all()
        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        slug = self.kwargs.get('tag_slug')
        return Post.objects.get_by_tag(slug)


class PostThemesView(ListView):
    template_name = 'blog/index.html'
    context_object_name = 'allposts'
    paginate_by = 9

    def get_context_data(self, *args, **kwargs):
        context = super(PostThemesView, self).get_context_data(*args, **kwargs)
        context['tags'] = Tag.objects.all()
        # q = self.kwargs.get('category_slug')
        # context['categories'] = Themes.objects.filter(slug=q).first()
        context['searchthreads'] = Themes.objects.all()
        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        slug = self.kwargs.get('category_slug')
        return Post.objects.get_by_category(slug)

class PostDetailView(ObjectViewedMixin, DetailView):
    model = Post
    paginate_by = 20

    def get_context_data(self, **kwargs):
            context = super(PostDetailView, self).get_context_data(**kwargs)
            q = self.kwargs.get('slug')
            post = Post.objects.get(slug=q)
            messages = Message.objects.filter(post=post.id)
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

class PostLikeToggle(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        slug = self.kwargs.get('slug')
        obj = get_object_or_404(Post, slug=slug)
        url_ = obj.get_absolute_url()
        user = self.request.user
        if user.is_authenticated:
            if user in obj.likes.all():
                obj.likes.remove(user)
            else:
                obj.likes.add(user)
        return url_

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
        return redirect('post-detail', newpost.slug)


    return render(request, 'blog/post_form.html', context)


@login_required
def updatepost(request, slug):
    editpost = Post.objects.get(slug=slug)
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
        return redirect('post-detail', editpost.slug)


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
        form.instance.post_id = self.kwargs['id']
        return super().form_valid(form)

class MessageUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Message
    fields = ['message']
    slug_field = 'id'
    slug_url_kwarg = 'id'

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
    template_name = 'blog/message_confirm_delete.html'
    slug_field = 'id'
    slug_url_kwarg = 'id'

    def get_success_url(self):
        post = self.get_object()
        return post.get_absolute_url()

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
        # user = get_object_or_404(User, email=self.kwargs.get('email'))
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-created')

    def get_context_data(self, **kwargs):
        context = super(UserPostListView, self).get_context_data(**kwargs)
        context['searchthreads'] = Themes.objects.all()
        context['tags'] = Tag.objects.all()
        return context
