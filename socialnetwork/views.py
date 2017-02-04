from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.utils import timezone
from django.db import transaction
from socialnetwork.models import *
from socialnetwork.forms import *
from django.http import HttpResponse, Http404
from datetime import datetime, date, timedelta
from django.core import serializers
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail


@login_required
def timeline(request):
    context = {}
    context['posts'] = Post.objects.filter(public=True).order_by('-date','-time')
    context['comment_form'] = CommentForm()
    return render(request, 'timeline.html', context)

@login_required
def following(request):
    context = {}
    postlist = []
    user = get_object_or_404(User, username=request.user.username)
    user_profile = get_object_or_404(Profile, user=user)
    following = user_profile.following.all()
    posts =  Post.objects.filter(user__in=following).order_by('-date','-time')
    context['posts'] = posts
    context['comment_form'] = CommentForm()
    return render(request, 'timeline.html', context)

@login_required
def profile(request):
    context = {}
    context['post_form'] = PostForm()
    user = get_object_or_404(User, username=request.user.username)
    user_profile = get_object_or_404(Profile, user=user)
    context['user_profile'] = user_profile
    context['posts'] = Post.objects.filter(user=user_profile).order_by('-date','-time')
    context['comment_form'] = CommentForm()
    return render(request, 'profile.html', context)


@login_required
def otherProfile(request,username):
    context = {}
    me = get_object_or_404(Profile,user=request.user)
    followings = me.following.all()
    user = get_object_or_404(User, username=username)
    user_profile = get_object_or_404(Profile, user=user)
    context['user_profile'] = user_profile
    context['posts'] = Post.objects.filter(user=user_profile).filter(public=True).order_by('-date','-time')
    following = user_profile in followings 
    myself = user_profile == me
    context['following'] = not following
    context['notfollowing'] = following
    context['myself'] = myself
    context['comment_form'] = CommentForm()
    return render(request, 'profile.html', context)


@login_required
@transaction.atomic
def addPost(request):
    context = {}
    errors = []

    if 'public' in request.POST:
        public = False
    else:
        public = True

    if not 'content' in request.POST or not request.POST['content']:
        errors.append('You must enter a post to add.')
    else:
        user_profile = get_object_or_404(Profile, user=request.user)
        new_post = Post(user=user_profile,content=request.POST['content'])
        new_post.userId = user_profile.id
        new_post.date = timezone.now()
        new_post.time = timezone.now()
        new_post.public = public
        new_post.username = request.user.username
        new_post.save()

    context['post_form'] = PostForm()
    user = get_object_or_404(User, username=request.user.username)
    user_profile = get_object_or_404(Profile, user=user)
    context['user_profile'] = user_profile
    context['posts'] = Post.objects.filter(user=user_profile).order_by('-date')
    context['comment_form'] = CommentForm()
    return redirect(reverse('profile'))
    

@login_required
@transaction.atomic
def deletePost(request, id):
    errors = []
    try:
        post_to_delete = Post.objects.get(id=id, user=request.user)
        post_to_delete.delete()
    except ObjectDoesNotExist:
        errors.append('The post did not exist in your profile.')
    
    user_profile = get_object_or_404(Profile, user=request.user)
    posts = Post.objects.filter(user=user_profile)
    context = {'posts' : posts, 'errors' : errors}
    return render(request, 'profile.html', context)


@login_required
def addComment(request):
    postId = request.POST['post_id']
    post = Post.objects.get(id=postId)
    author = get_object_or_404(Profile,user=request.user)
    comment = Comment()
    comment.body = request.POST['body']
    comment.post = post
    comment.author = author
    comment.datetime = timezone.now()
    comment.save()

    response = serializers.serialize('json', [comment,request.user,author])
    return HttpResponse(response, content_type='application/json')


@transaction.atomic
def register(request):
    context = {}

    if request.method == 'GET':
        context['form'] = RegistrationForm()
        return render(request, 'register.html', context)

    # Creates a bound form from the request POST parameters and makes the 
    # form available in the request context dictionary.
    form = RegistrationForm(request.POST)
    context['form'] = form

    # Validates the form.
    if not form.is_valid():
        return render(request, 'register.html', context)

    # If we get here the form data was valid.  Register and login the user.
    new_user = User.objects.create_user(username=form.cleaned_data['username'], 
                                        email=form.cleaned_data['email'],
                                        first_name=form.cleaned_data['first_name'],
                                        last_name=form.cleaned_data['last_name'],
                                        password=form.cleaned_data['password1'])
    new_user.birthday = timezone.now()
    new_user.is_active = False
    new_user.save()

    new_profile = Profile(user=new_user)
    new_profile.save()

        # Generate a one-time use token and an email message body
    token = default_token_generator.make_token(new_user)

    email_body = """
    Welcome to the Social Network.  Please click the link below to
    verify your email address and complete the registration of your account:
    http://%s%s
    """ % (request.get_host(), 
            reverse('confirm', args=(new_user.username, token)))

    send_mail(subject="Verify your email address",
              message= email_body,
              from_email="johnlee1@andrew.cmu.edu",
              recipient_list=[new_user.email])

    context['email'] = form.cleaned_data['email']
    return render(request, 'needs-confirmation.html', context)


@transaction.atomic
def confirm_registration(request, username, token):
    user = get_object_or_404(User, username=username)

    # Send 404 error if token is invalid
    if not default_token_generator.check_token(user, token):
        raise Http404

    # Otherwise token was valid, activate the user.
    user.is_active = True
    user.save()
    return render(request, 'confirmed.html', {})


@login_required
def about(request):
    context = {}
    return render(request, 'about.html', context)


@login_required
def settings(request):
    context = {}

    user = get_object_or_404(User, username=request.user.username)
    user_profile = get_object_or_404(Profile, user=user)

    if request.method == 'GET':
        context['form'] = SettingsForm()
        user = get_object_or_404(User, username=request.user.username)
        user_profile = get_object_or_404(Profile, user=user)
        context['user_profile'] = user_profile
        return render(request, 'settings.html', context)

    form = SettingsForm(request.POST,request.FILES)
    context['form'] = form

    # Validates the form.
    if not form.is_valid():
        return render(request, 'settings.html', context)

    if form.cleaned_data['birthday'] != '':
        birthday = form.cleaned_data['birthday']
        born = datetime.strptime(birthday, '%Y-%m-%d').date()
        today = date.today()
        age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
        user_profile.age = age

    if form.cleaned_data['profile_picture'] != '':
        user_profile.profile_picture = form.cleaned_data['profile_picture']

    if form.cleaned_data['first_name'] != '':
        user.first_name = form.cleaned_data['first_name']

    if form.cleaned_data['last_name'] != '':
        user.last_name = form.cleaned_data['last_name']

    if form.cleaned_data['bio'] != '':
        user_profile.bio = form.cleaned_data['bio']

    user.save();
    user_profile.save();

    context['post_form'] = PostForm()
    user = get_object_or_404(User, username=request.user.username)
    user_profile = get_object_or_404(Profile, user=user)
    context['user_profile'] = user_profile
    context['posts'] = Post.objects.filter(user=user_profile).order_by('-date','-time')
    context['comment_form'] = CommentForm()
    return render(request, 'profile.html', context)

@login_required
def follow(request):
    username = request.POST.get('username')
    target_user = get_object_or_404(User, username=username)
    target_user_profile = get_object_or_404(Profile, user=target_user)

    user_profile = get_object_or_404(Profile, user=request.user)
    user_profile.following.add(target_user_profile)
    user_profile.save()

    context = {}
    user = get_object_or_404(User, username=username)
    user_profile = get_object_or_404(Profile, user=user)
    context['user_profile'] = user_profile
    context['posts'] = Post.objects.filter(user=user_profile).filter(public=True).order_by('-date','-time')

    followings = user_profile.following.all()
    following = user_profile in followings
    context['following'] = following
    context['notfollowing'] = not following
    context['comment_form'] = CommentForm()
    return render(request, 'profile.html', context)

@login_required
def unfollow(request):
    username = request.POST.get('username')
    target_user = get_object_or_404(User, username=username)
    target_user_profile = get_object_or_404(Profile, user=target_user)

    user_profile = get_object_or_404(Profile, user=request.user)
    user_profile.following.remove(target_user_profile)
    user_profile.save()

    context = {}
    user = get_object_or_404(User, username=username)
    user_profile = get_object_or_404(Profile, user=user)
    context['user_profile'] = user_profile
    context['posts'] = Post.objects.filter(user=user_profile).filter(public=True).order_by('-date','-time')
    
    followings = user_profile.following.all()
    following = user_profile in followings
    context['following'] = not following
    context['notfollowing'] = following
    context['comment_form'] = CommentForm()
    return render(request, 'profile.html', context)

@login_required
def photo(request, id):
    user_profile = get_object_or_404(Profile,id=id)
    print user_profile.profile_picture
    if not user_profile.profile_picture:
        return Http404
    return HttpResponse(user_profile.profile_picture, content_type=user_profile.profile_picture)

@login_required
def refreshGlobal(request):
    time_threshold = datetime.now() - timedelta(seconds=5)
    posts = Post.objects.filter(public=True).filter(time__gte=time_threshold).filter(date=datetime.now()).order_by('-date','-time')
    response = serializers.serialize('json', posts)
    return HttpResponse(response, content_type='application/json')