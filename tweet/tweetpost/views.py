from django.shortcuts import render
from .models import tweet,Like,Comment
from .forms import TweetForm
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.http import require_POST
from django.db.models import Q

# Create your views here.
def index(request):
    return render(request,'index.html')



def tweet_list(request):
    query = request.GET.get('q', '').strip()

    tweets = tweet.objects.select_related('user').all()

    if query:
        tweets = tweets.filter(
            Q(text__icontains=query) |
            Q(user__username__icontains=query)
        )

    tweets = tweets.order_by('-created_at')

    for tweet_obj in tweets:
        tweet_obj.liked_by_user = tweet_obj.likes.filter(
            user=request.user
        ).exists()

    return render(request, 'tweet_list.html', {
        'tweets': tweets,
        'query': query,
    })


@login_required
def tweet_create(request):
    if request.method=="POST":
        form =TweetForm(request.POST,request.FILES)
        if form.is_valid():
            tweet_obj=form.save(commit=False)
            tweet_obj.user=request.user
            tweet_obj.save()
            return redirect('tweet_list')
        
    else:
        form = TweetForm()
    return render(request,'tweet_from.html',{'form':form ,'page_title':'Create Tweet'})


@login_required
def tweet_update(request,tweet_id):
    tweet_obj=get_object_or_404(tweet,pk=tweet_id,user=request.user)
    if request.method=='POST':
        form=TweetForm(request.POST,request.FILES,instance=tweet_obj)
        if form.is_valid():
            form.save()
            return redirect('tweet_list')
    else:
        form=TweetForm(instance=tweet_obj)
    return render(request,'tweet_form.html',{'form':form,'tweet':tweet_obj,'page_title':'Update Tweet'})


@login_required
def tweet_delete(request,tweet_id):
    tweet_obj=get_object_or_404(tweet,pk=tweet_id,user=request.user)

    if  request.method=='POST':
        tweet_obj.delete()
        return redirect('tweet_list')
    return render(request,'tweet_conform_delete.html',{'tweet': tweet_obj})



@login_required
@require_POST
def toggle_like(request, tweet_id):

    tweet_obj = get_object_or_404(tweet, pk=tweet_id)

    like_obj = Like.objects.filter(
        user=request.user,
        post=tweet_obj
    )

    if like_obj.exists():
        like_obj.delete()
    else:
        Like.objects.create(
            user=request.user,
            post=tweet_obj
        )

    return redirect('tweet_list')



@login_required
@require_POST
def add_comment(request, tweet_id):
    tweet_obj = get_object_or_404(tweet, pk=tweet_id)

    content = request.POST.get('content', '').strip()

    if content:
        Comment.objects.create(
            user=request.user,
            post=tweet_obj,
            content=content
        )

    return redirect('tweet_list')


def register_view(request):

    if request.user.is_authenticated:
        return redirect('tweet_list')

    if request.method == 'POST':

        form = UserCreationForm(request.POST)

        if form.is_valid():

            user = form.save()
            login(request, user)

            messages.success(
                request,
                'Your account has been created successfully!'
            )

            return redirect('tweet_list')

    else:
        form = UserCreationForm()

    # IMPORTANT: Keep this return outside the POST condition
    return render(request, 'register.html', {
        'form': form
    })


def login_view(request):
    if request.user.is_authenticated:
        return redirect('tweet_list')

    if request.method=='POST':
        form=AuthenticationForm(
            request,
            data=request.POST
        )
        if form.is_valid():
            user=form.get_user()
            login(request,user)

            messages.success(
                request,
                f'Credential Successfully Varified, Welcome back {user.username}'
            )
            return redirect('tweet_list')
    else:
        form=AuthenticationForm()
    return render(request,'login.html',{'form':form})

@login_required
@require_POST
def logout_view(request):
    logout(request)

    messages.success(
        request,
        "Account Logout Successfully"
    )
    return redirect ('index')
