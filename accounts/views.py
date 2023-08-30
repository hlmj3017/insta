from django.shortcuts import render, redirect

from .forms import CustomUserCreationForm
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

