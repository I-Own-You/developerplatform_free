from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from .forms import RegisterForm, UserEditForm, ProjCreateForm, MessageCreateForm
from .models import Developer, Message
from project.models import Project
import re
from django.contrib import messages
from django.db.models import Q
from .models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views.decorators.debug import sensitive_post_parameters
# Create your views here.

@sensitive_post_parameters('email', 'password')
def register_user(request):

    if request.user.is_authenticated:
        return redirect('dev-page')
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            User.objects.create_user(
                email=form.cleaned_data['email'].lower(),
                password=form.cleaned_data['password']
            )
            developer = Developer(
                user=User.objects.get(email=form.cleaned_data.get('email')),
                email=form.cleaned_data['email'].lower(),
                password=form.cleaned_data['password']
            )
            developer.save()
            user = authenticate(
                email=form.cleaned_data['email'], password=form.cleaned_data['password']
            )
            if user is not None:
                login(request, user)
                return redirect('my-account' if request.POST else 'my-account')
            else:
                messages.error(request, 'User doesn\'t exist')

    else:
        form = RegisterForm()

    context = {
        'form': form,
    }
    return render(request, 'register.html', context)

@sensitive_post_parameters('email', 'password')
def login_user(request):

    if request.user.is_authenticated:
        return redirect('dev-page')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('dev-page' if request.POST else 'dev-page')
        else:
            messages.error(request, 'User doesn\'t exist')

    return render(request, 'login.html')


def logout_user(request):
    logout(request)
    return redirect('dev-page')


def dev_page(request):
    devs = []
    for dev in Developer.objects.all():
        if dev.first_name and dev.last_name and dev.short_bio and dev.work_position:
            devs.append(dev)

    if request.method == 'GET':
        search_dev = request.GET.get('search-dev')
        if bool(search_dev):
            search_dev = search_dev.strip()
            devs = Developer.objects.filter(
                Q(first_name__contains=search_dev) | Q(
                    last_name__contains=search_dev) | Q(
                        work_position__contains=search_dev
                )
            )

    if 'next' in request.GET:
        id = int(request.GET['next'])
        project = Project.objects.get(id=id)
        side_dev = Developer.objects.get(email=project.owner.email)
        devs = [side_dev]

    paginator = Paginator(devs, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        # 'devs': devs,
        'page_obj': page_obj,
    }
    return render(request, 'dev_page.html', context)


@login_required(login_url='login')
def my_account(request):

    developer = Developer.objects.get(email=request.user.email)
    data = {
        'first_name': developer.first_name,
        'last_name': developer.last_name,
        'username': developer.username,
        'work_position': developer.work_position,
        'short_bio': developer.short_bio,
        'social_link_github': developer.social_link_github,
        'social_link_linkedIn': developer.social_link_linkedIn,
    }
    form = UserEditForm(initial=data)
    if request.method == 'POST':
        form = UserEditForm(request.POST)
        if form.is_valid():
            developer.first_name = form.cleaned_data['first_name']
            developer.last_name = form.cleaned_data['last_name']
            developer.work_position = form.cleaned_data['work_position']
            developer.short_bio = form.cleaned_data['short_bio']
            developer.social_link_github = form.cleaned_data['social_link_github']
            developer.social_link_linkedIn = form.cleaned_data['social_link_linkedIn']

            answer = Developer.objects.filter(
                username=form.cleaned_data['username']).exists()
            if not answer:
                developer.username = form.cleaned_data['username']

            developer.save()

    context = {
        'form': form,
        'project': Project.objects.all(),
    }

    return render(request, 'account.html', context)


@login_required(login_url='login')
def proj_create(request):

    if request.method == 'POST':
        form = ProjCreateForm(request.POST)
        if form.is_valid():
            project = Project(
                owner=Developer.objects.get(email=request.user.email),
                title=form.cleaned_data.get('title'),
                description=form.cleaned_data.get('description'),
                source_link=form.cleaned_data.get('source_link'),
            )
            project.save()
            return redirect('proj-create')

    else:
        form = ProjCreateForm()

    projects = Project.objects.filter(
        owner=Developer.objects.get(email=request.user.email))

    context = {
        'form': form,
        'projects': projects,
    }
    return render(request, 'proj_creation.html', context)


@login_required(login_url='login')
def inbox(request):
    msgs = Message.objects.filter(
        recipient=Developer.objects.get(email=request.user.email))
    unread_msgs = Message.objects.filter(recipient=Developer.objects.get(
        email=request.user.email), is_read=False).count()

    context = {
        'msgs': msgs,
        'unread_msg': unread_msgs,
    }
    return render(request, 'inbox.html', context)


@login_required(login_url='login')
def message(request, id):
    msg = Message.objects.get(id=id)

    msg.is_read = True
    msg.save()
    context = {
        'msg': msg,
    }
    return render(request, 'message.html', context)


@login_required(login_url='login')
def create_message(request, id):
    dev = Developer.objects.get(id=id)
    if request.method == 'POST':
        form = MessageCreateForm(request.POST)
        if form.is_valid():
            msg = Message(
                sender=Developer.objects.get(email=request.user.email),
                recipient=dev,
                subject=form.cleaned_data.get('subject'),
                content=form.cleaned_data.get('content'),
            )
            msg.save()
            return redirect('create-message', id)
    else:
        form = MessageCreateForm()

    context = {
        'form': form,
    }

    return render(request, 'create_message.html', context)
