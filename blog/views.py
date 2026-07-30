from django.shortcuts import render, get_object_or_404
from .models import Blogpost
from django.http import HttpResponse

# ==================== MAIN BLOG HOME VIEW ====================
def index(request):
    myposts = Blogpost.objects.all()
    print(myposts)
    return render(request, 'blog/index.html', {'myposts': myposts})


# ==================== INDIVIDUAL POST VIEW ====================
def blogpost(request, id):
    # SECURE UPGRADE: Safely gets the post by ID, or displays a clean 404 if it doesn't exist
    post = get_object_or_404(Blogpost, post_id=id)
    print(post)
    return render(request, 'blog/blogpost.html', {'post': post})