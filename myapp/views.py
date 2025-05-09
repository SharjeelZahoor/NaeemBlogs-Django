from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib.auth import authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .models import *

from .models import Comment,Post, SocialMediaLink
# Create your views here.
def index(request):
    social_links = SocialMediaLink.objects.all()
    return render(request, "index.html", {
        'posts': Post.objects.filter(user_id=request.user.id).order_by("-id"),  # User's posts, reversed order
        'top_posts': Post.objects.all().order_by("-likes"),  # Top posts by likes
        'recent_posts': Post.objects.all().order_by("-id"),  # Recent posts
        'social_links': social_links,  # Social media links
        'user': request.user,  # Current user
        'media_url': settings.MEDIA_URL,  # Media URL for static files
    })

from myapp.utils import get_online_user_count

@login_required
def home(request):
    online_users = None
    if request.user.is_staff:  # Only show to admin users
        online_users = get_online_user_count()
    return render(request, 'home.html', {'online_users': online_users})


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        
        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,"Username already Exists")
                return redirect('signup')
            if User.objects.filter(email=email).exists():
                messages.info(request,"Email already Exists")
                return redirect('signup')
            else:
                User.objects.create_user(username=username,email=email,password=password).save()
                return redirect('signin')
        else:
            messages.info(request,"Password should match")
            return redirect('signup')
            
    return render(request,"signup.html")

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect("index")
        else:
            messages.info(request,'Username or Password is incorrect')
            return redirect("signin")
            
    return render(request,"signin.html")

def logout(request):
    auth.logout(request)
    return redirect('index')

def blog(request):
    social_links = SocialMediaLink.objects.all()  # Get social media links
    return render(request, "blog.html", {
        'posts': Post.objects.filter(user_id=request.user.id).order_by("-id"),  # User's posts, reversed order
        'top_posts': Post.objects.all().order_by("-likes"),  # Top posts by likes
        'recent_posts': Post.objects.all().order_by("-id"),  # Recent posts
        'social_links': social_links,  # Social media links
        'user': request.user,  # Current user
        'media_url': settings.MEDIA_URL,  # Media URL for static files
    })




def create(request):
    if request.method == 'POST':
        try:
            postname = request.POST['postname']
            content = request.POST['content']
            category = request.POST['category']
            image = request.FILES['image']
            Post(postname=postname,content=content,category=category,image=image,user=request.user).save()
        except:
            print("Error")
        return redirect('index')
    else:
        return render(request,"create.html")
    
def profile(request,id):
    
    return render(request,'profile.html',{
        'user':User.objects.get(id=id),
        'posts':Post.objects.all(),
        'media_url':settings.MEDIA_URL,
    })
    
    
def profileedit(request,id):
    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
    
        user = User.objects.get(id=id)
        user.first_name = firstname
        user.email = email
        user.last_name = lastname
        user.save()
        return profile(request,id)
    return render(request,"profileedit.html",{
        'user':User.objects.get(id=id),
    })


@login_required
def togglelike(request, post_id):
    post = Post.objects.get(id=post_id)
    user = request.user

    if user in post.likes.all():
        post.likes.remove(user)
        liked = False
    else:
        post.likes.add(user)
        liked = True

    return JsonResponse({
        'liked': liked,
        'total_likes': post.likes.count()
    })

def post(request,id):
    post = Post.objects.get(id=id)
    
    return render(request,"post-details.html",{
        "user":request.user,
        'post':Post.objects.get(id=id),
        'recent_posts':Post.objects.all().order_by("-id"),
        'media_url':settings.MEDIA_URL,
        'comments':Comment.objects.filter(post_id = post.id),
        'total_comments': len(Comment.objects.filter(post_id = post.id))
    })
    
def savecomment(request,id):
    post = Post.objects.get(id=id)
    if request.method == 'POST':
        content = request.POST['message']
        Comment(post_id = post.id,user_id = request.user.id, content = content).save()
        return redirect("index")
    
def deletecomment(request,id):
    comment = Comment.objects.get(id=id)
    postid = comment.post.id
    comment.delete()
    return post(request,postid)
    
def editpost(request,id):
    post = Post.objects.get(id=id)
    if request.method == 'POST':
        try:
            postname = request.POST['postname']
            content = request.POST['content']
            category = request.POST['category']
            
            post.postname = postname
            post.content = content
            post.category = category
            post.save()
        except:
            print("Error")
        return profile(request,request.user.id)
    
    return render(request,"postedit.html",{
        'post':post
    })
    
def deletepost(request,id):
    Post.objects.get(id=id).delete()
    return profile(request,request.user.id)

from django.shortcuts import get_object_or_404, redirect
from .models import SocialMediaLink
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def update_social_link(request, link_id):
    # Ensure the request method is POST
    if request.method == 'POST':
        new_link = request.POST.get('new_link')
        
        # Get the social media link object or 404
        social_link = get_object_or_404(SocialMediaLink, id=link_id)
        
        # Update the link and save
        social_link.link = new_link
        social_link.save()
        
        # Add a success message
        messages.success(request, f"{social_link.name} link updated successfully!")
        
        # Redirect back to the same page
        return redirect(request.META.get('HTTP_REFERER', '/'))
    
    # If not POST, return an error or redirect
    messages.error(request, "Invalid request method.")
    return redirect('/')

# terms and conditions
#privacy
from django.shortcuts import render

def terms_view(request):
    return render(request, 'terms.html')

def privacy_view(request):
    return render(request, 'privacy.html')
