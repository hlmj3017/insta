from django.shortcuts import render, redirect

from .forms import CustomUserCreationForm, CustomAuthenticationForm

from django.contrib.auth import login as auth_login
# from .models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES) # 아이디, 패스워드 / 사진, 프로필 이미지
        if form.is_valid():
            form.save()
            return redirect('posts:index')


    else:
        form = CustomUserCreationForm()

    context = {
        'form': form,
    }

    return render(request, 'accounts/form.html', context) # 이름 중복 충돌 제거 

    # 'form.html' 안 만들었는데 동작을 하는 이유
    # -> posts의 form.html이 먼저 만들어서 우선순위로 작동함


def login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('posts:index')


    else:
        form = CustomAuthenticationForm()

    context = {
        'form': form,
    }

    return render(request, 'accounts/form.html', context)
    

def profile(request, username):
    User = get_user_model()

    user_info = User.objects.get(username=username)

    context ={
        'user_info' : user_info,
    }

    return render(request, 'accounts/profile.html', context)


@login_required
def follow(request, username):
    User = get_user_model()

    me = request.user  # 내가 팔로우하고 싶은
    you = User.objects.get(username=username) # 내가 팔로우하고 싶은 상대방

    # 팔로잉이 이미 되어있는 경우
    # if me in you.followers.all(): # 당신을 따르고 있는 사람들에 내가 있는지
    if you in me.followings.all(): # 내가 팔로잉하는 사람에 너가 있는지
        me.followings.remove(you)  # 나 너 지울거


    # 팔로잉이 아직 안 된 경우

    else:
        me.followings.add(you)


    return redirect('accounts:profile', username=username)


    