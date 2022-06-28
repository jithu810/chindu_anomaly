from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post
import operator
from django.urls import reverse_lazy
from django.contrib.staticfiles.views import serve
from django.shortcuts import render,redirect

from django.core.cache.backends.base import DEFAULT_TIMEOUT
from ipware import get_client_ip
from django.conf import settings
from django.db.models import Q
import blacklist
lst=[]
bls_ip=[]
from users.models import Space


def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)

def search(request):
    template='blog/home.html'

    query=request.GET.get('q')

    result=Post.objects.filter(Q(title__icontains=query) | Q(author__username__icontains=query) | Q(content__icontains=query))
   
    paginate_by=2
    context={ 'posts':result }
    print(context)
    return render(request,template,context)
   


def getfile(request):
   return serve(request, 'File')


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 2


  # <app>/<model>_<viewtype>.html
 




class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 2
    
    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        
        return Post.objects.filter(author=user).order_by('-date_posted')
        

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content', 'file']
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        status = Space.objects.get(name=form.instance.author)
        approved=(status.status)
        if approved==str("Approved"):
            return super().form_valid(form)
        elif approved==str("pending"):
            return  JsonResponse({'status':501,'message':'not approved by admin'})


      


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content', 'file']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'
    template_name = 'blog/post_confirm_delete.html'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            c=(post.file)
            try:
                import os 
                os.remove("./media/"+str(c))
            except :
                pass
            return True
        return False


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})


def Next(request):
        return JsonResponse({'status':501,'message':'time out','ip':bls_ip})


CACHE_TTL= getattr(settings,'CACHE_TTL',DEFAULT_TIMEOUT)

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    lst.append(ip)
    return ip
def rate_limiting(request):
    current=get_client_ip(request)

    if lst.count(current)>=5:
        if current not in bls_ip:
            bls_ip.append(current)
            Timer(20.0, hello).start() 
        

        return JsonResponse({'status':501,'message':'time out','ip':bls_ip})
    else:
        return redirect('home/')


from threading import Timer

def hello():
    if not bls_ip:
        pass
    else:
        lst.clear()
        Timer(20.0, hello).start()
