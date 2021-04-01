from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect

from .models import TwitterUsers
from .forms import PostForm


def index(request):
    twitter_users = TwitterUsers.objects.all()
    context = {'twitter_users': twitter_users}
    return render(request, 'display/index.html', context)


def user_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.name = request.POST['name']
            post.comment = request.POST['comment']
            post.save()
            return redirect('/')
    else:
        form = PostForm()
    return render(request, 'display/user_new.html', {'form': form})


def delete(request, twitterusers_id):
    delete_user = get_object_or_404(TwitterUsers, pk=twitterusers_id)
    delete_user.delete()
    return redirect("/")

