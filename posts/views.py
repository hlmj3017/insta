from django.shortcuts import render, redirect
from .models import Post

from .forms import PostForm, CommentForm

from django.contrib.auth.decorators import login_required
# Create your views here.

def index(request):
    posts = Post.objects.all().order_by('-id')
    comment_form = CommentForm()

    context = {
        'posts': posts,
        'comment_form': comment_form,
    }

    return render(request, 'index.html', context)


@login_required
def create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user # 로그인한 사람 정보 출력
            post.save()
            return redirect('posts:index')

    
    else:
        form = PostForm()

    context = {
        'form': form,
    }

    return render(request, 'form.html', context)

@login_required
def comment_create(request, post_id):
    comment_form = CommentForm(request.POST) # 인스턴스화

    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        # 현재 로그인 유저
        comment.user = request.user
        # post_id를 기준으로 찾은 post
        post = Post.objects.get(id=post_id)
        comment.post = post

        # comment.post_id = post_id : 빠르게 하고 싶은 경우

        comment.save()

        return redirect('posts:index')

