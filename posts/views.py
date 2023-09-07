from django.shortcuts import render, redirect
from .models import Post, Comment

from .forms import PostForm, CommentForm

from django.contrib.auth.decorators import login_required

from django.http import JsonResponse
# Create your views here.

def index(request):
    posts = Post.objects.all().order_by('-id') # 최신순
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


def comment_delete(request, post_id, id):
    comment = Comment.objects.get(id=id)

    comment.delete()

    return redirect('posts:index')


def comment_edit(request, post_id, id):
    comment = Comment.objects.get(id=id)

    context = {
        'comment': comment,
        'post_id': post_id
    }

    return render(request, 'comment_edit.html', context)


def comment_update(request, post_id, id):
    # new data
    updated_content = request.POST.get('content')

    # old data
    comment = Comment.objects.get(id=id)

    comment.content = updated_content
    comment.save()

    return redirect('posts:index')




@login_required
def like(request, post_id):

    # 좋아요 버튼을 누른 유저
    user = request.user # 로그인한 사람
    post = Post.objects.get(id=post_id) # 어떤 게시물 선택

    # 이미 좋아요버튼을 누른 경우
    # if user in post.like_users.all():
    if post in user.like_posts.all():
        post.like_users.remove(user) # 좋아요 누른 사람 제거
        # user.like_posts.remove(post)

    # 좋아요버튼을 아직 안누른 경우
    else:
        post.like_users.add(user) # 게시물에 좋아요 누른 사람 추가.. 게시물을 기준으로 나를 추가
        # user.like_posts.add(post) # 나를 기준으로 게시물 추가

    return redirect('posts:index')


@login_required
def comment_like(request, post_id, comment_id):
    user = request.user 
    comment = Comment.objects.get(id=comment_id)  

    if comment in user.liked_comments.all():
        comment.likes.remove(user) 
 
    else:
        comment.likes.add(user) 

    return redirect('posts:index')



def like_async(request, post_id):
    # context = {
    #     'message': post_id,
    # }

    user = request.user
    post = Post.objects.get(id=post_id)

    if user in post.like_users.all():
        post.like_users.remove(user)
        status = False
    else:
        post.like_users.add(user)
        status = True

    context = {
        'status': status,
        'count': len(post.like_users.all())
    }

    return JsonResponse(context)



def comment_like_async(request, post_id, comment_id):
    user = request.user 
    comment = Comment.objects.get(id=comment_id)  
    

    if comment in user.liked_comments.all():
        comment.likes.remove(user) 
        status = False
        
 
    else:
        comment.likes.add(user) 
        status = True

    # likes_count = comment.likes.count()

    context = {
        'status': status,
        # 'count': likes_count
        'count': len(comment.likes.all())
    }

    return JsonResponse(context)

