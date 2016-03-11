"""DjangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
# from prontand.views import HomePageView, PostDetailView, TaxView, AddMessageView, PostSearchView
from pront.views import HomePageView, PostDetailView, TaxView, AddMessageView, PostSearchView
# from pront.views import HomePageView as Home
urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^wysiwyg/', include('wysiwyg.urls')),

    url(r'^$', HomePageView.as_view(), name='home'),

    # url(r'^$', HomePageView.as_view(), name='home'),
    url(r'^(?P<tax>[\w-]+)$', TaxView.as_view(), name='page'),
    url(r'^(?P<tax>[\w-]+)$', TaxView.as_view(), name='post'),
    url(r'^(?P<tax>[\w-]+)$', TaxView.as_view(), name='tags'),
    url(r'^(?P<tax>[\w-]+)/(?P<slug>[-\w\d]+)$', PostDetailView.as_view(), name='post-detail'),
    url(r'^add-message/$', AddMessageView.as_view(), name='add_message'),
    url(r'^search/$', PostSearchView.as_view(), name='search_post'),

    # url(r'^pront/$', Home.as_view(), name='pront_home'),

    # url(r'^categories/(?P<tax>[\w-]+)/$', CategoriesView.as_view(), name='categories'),
    # url(r'^test/$', TestView.as_view(), name='test'),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
