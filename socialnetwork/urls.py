from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from socialnetwork.views import register,profile,otherProfile,addPost,timeline,about,settings,follow,following,unfollow,photo,addComment,refreshGlobal,confirm_registration


urlpatterns = [
    url(r'^login$', auth_views.login, {'template_name':'login.html'}, name='login'),
    url(r'^logout$', auth_views.logout_then_login, name='logout'),
    url(r'^register$', register, name='register'),
    url(r'^follow$', follow, name='follow'),
    url(r'^unfollow$', unfollow, name='unfollow'),
    url(r'^timeline/', timeline, name="timeline"),
    url(r'^following/', following, name="following"),
    url(r'^profile/', profile, name="profile"),
    url(r'^settings/', settings, name="settings"),
    url(r'^addPost/', addPost, name="addPost"),
    url(r'^addComment/', addComment, name="addComment"),
    url(r'^about/', about, name="about"),
    url(r'^refreshGlobal/', refreshGlobal, name="refreshGlobal"),
    url(r'^(?P<username>[^/]+)/$', otherProfile, name='otherProfile'),
    url(r'^photo/(?P<id>\d+)$', photo, name="photo"),
     url(r'^confirm-registration/(?P<username>[a-zA-Z0-9_@\+\-]+)/(?P<token>[a-z0-9\-]+)$',
        confirm_registration, name='confirm'),
    url(r'^', profile),
]