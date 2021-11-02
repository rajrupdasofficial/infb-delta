from django.urls import path
from .views import *
from app.sitemaps import BlogPostSitemap
from django.contrib.sitemaps.views import sitemap

sitemaps={
    'blogposts':BlogPostSitemap,
}


urlpatterns=[
   # path('',IndexPageView.as_view(),name='index'),
   # path('index/',IndexView.as_view(),name='indexpage'),
    path('',HomeView.as_view(),name='home'),
    path('article/<slug:slug>',BlogDetailView.as_view(),name='article-detail'),
    path('links/',LinkPage.as_view(),name='links'),
    path('homepage/',HomePageView.as_view(),name='homepage'),
    path('contact/',ContactPageView.as_view(),name='contacts'),
    path('search/',SearchView.as_view(),name='search'),
    path('addpost/',AddPostView.as_view(),name='addpost'),
    path('updatepost/edit/<slug:slug>',UpdatePostView.as_view(),name='update'),
    path('article/<slug:slug>/remove',DeletePostView.as_view(),name='delete'),
    path('userregister/registration',UserRegisterView.as_view(),name='signup'),
    path('likes/<slug:slug>/',PostLikeView.as_view(),name="liked"),
    path('unlikes/<slug:slug>/',PostUnLikeView.as_view(),name="unliked"),
    path('category/<str:cats>',CategoryView,name='category'),
    path('about/aboutus/',AboutView.as_view(),name="about"),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
                        name='django.contrib.sitemaps.views.sitemap'),

]