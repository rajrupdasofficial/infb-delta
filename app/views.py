from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import ListView,DetailView,TemplateView,UpdateView,CreateView,DeleteView,RedirectView
from .models import BlogPost,UserDetail
from blogapp.models import Contact,Image,About
from django.contrib import messages
from django.urls import reverse_lazy
from .forms import PostForm,SignUpForm
from django.contrib.auth.models import User
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator
from django.http import Http404
class HomeView(ListView):
    model=BlogPost
    template_name='home.html'
    slug_field='slug'
    ordering=['-created']
    paginate_by=5
    paginate_orphans=1
    #def get_context_data(self,*args,**kwargs):
    #    try:
    #        return super(HomeView,self).get_context_data(*args,**kwargs)
    #    except Http404:
    #        self.kwargs['page']=1
    #        return super(HomeView,self).get_context_data(*args,**kwargs)
    
    def paginate_queryset(self,queryset,page_size):
        try:
            return super(HomeView,self).paginate_queryset(queryset,page_size)
        except Http404:
            self.kwargs['page']=1
            return super(HomeView,self).paginate_queryset(queryset,page_size)
class HomePageView(ListView):
    model=BlogPost
    template_name='home.html'
    slug_field='slug'
    ordering=['-created']
    paginate_by=5
    paginate_orphans=1
    def paginate_queryset(self,queryset,page_size):
        try:
            return super(HomePageView,self).paginate_queryset(queryset,page_size)
        except Http404:
            self.kwargs['page']=1
            return super(HomePageView,self).paginate_queryset(queryset,page_size)

class BlogDetailView(DetailView):
    model=BlogPost
    template_name='index.html'


class AboutView(TemplateView):
    def get(self,request):
        about=About.objects.all()
        context={
            'about':about,
        }
        return render(request,'aboutus.html',context )
class LinkPage(DetailView):
    def get(self,request):
        return render(request,'link_details.html')
class IndexPageView(TemplateView):
    template_name='index.html'

class IndexView(TemplateView):
    template_name='index.html'
class ContactPageView(TemplateView):
    template_name='contactdetail.html'
    def get(self,request):
        image=Image.objects.all()
        context={
            'image':image,
        }
        return render(request,'contactdetail.html',context)
    def post(self,request,*args,**kwargs):
        if request.method=="POST":
            name=request.POST['name']
            email=request.POST['email']
            phone=request.POST['phone']
            description=request.POST['description']
            if len(name)<2 or len(email)<3 or len(phone)<9 or len(description)<4:
                messages.error(request,"You have entered wrong Information")
            else:
                contact=Contact(name=name,email=email,phone=phone,description=description)
                contact.save()
                messages.success(request,"Your message hasbeen send successfully")
        return render(request,'contactdetail.html')

class SearchView(TemplateView):
    def get(self,request):
        query=request.GET['query']
        if len(query)>70:
            searchdetails=BlogPost.objects.none()
        else:
            searchtitle=BlogPost.objects.filter(post_title__icontains=query)
            searchcontent=BlogPost.objects.filter(content__icontains=query)
            searchdetails=searchtitle.union(searchcontent)
        if  searchdetails.count()==0:
            messages.warning(request,"Please refine your  query")
        context={
            'query':query,
            'search':searchdetails,
            
        }
        return render(request,'search.html',context)


class AddPostView(CreateView):
    model=BlogPost
    form_class=PostForm
    template_name='addpost.html'


class UpdatePostView(UpdateView):
    model=BlogPost
    slug_field='slug'
    form_class=PostForm
    template_name='update_post.html'
    #fields=['post_title','post_image','thumbnail','content','intro']

class DeletePostView(DeleteView):
    model=BlogPost
    slug_field='slug'
    template_name='delete_post.html'
    success_url=reverse_lazy('home')

class UserRegisterView(generic.CreateView):
    form_class=SignUpForm
    template_name='registration/register.html'
    success_url=reverse_lazy('login')







class PostLikeView(RedirectView):
    def get_redirect_url(self,*args,**kwargs):
        slug=self.kwargs.get("slug")
        obj=get_object_or_404(BlogPost,slug=slug)
        url_ =obj.get_absolute_url()
        user=self.request.user
        if user.is_authenticated:
            if user in obj.likes.all():
                obj.likes.remove(user)
            else:
                obj.likes.add(user)
        return  url_

class PostUnLikeView(RedirectView):
    def get_redirect_url(self,*args,**kwargs):
        slug=self.kwargs.get("slug")
        qs=get_object_or_404(BlogPost,slug=slug)
        url=qs.get_absolute_url()
        user=self.request.user
        if user.is_authenticated:
            if user in qs.unlikes.all():
                qs.unlikes.remove(user)
            else:
                qs.unlikes.add(user)
        return url


def CategoryView(request,cats):
    catrgory_posts=BlogPost.objects.filter(category=cats)
    context={
        'category':catrgory_posts,
        'cats':cats.title(),
    }
    return render(request,'categories.html',context)





