from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import PasswordChangeForm
from django.core import serializers
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.db import models, IntegrityError
from django.core.files.images import ImageFile
import json
import pycountry

# Import Models & Forms
from .models import User, Quote, Author, UserProfile, Category, Follow, Comment, Like
from .forms import SearchForm


# Views

def index(request):
    # Get all posted quotes and paginate
    quotes = Quote.objects.all().order_by('-timestamp')

    paginator = Paginator(quotes, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "quote/index.html", {
        'page_obj': page_obj,
    })


def register(request):
    if request.method == "POST":
        # If user submits empty forms, display error message
        if not request.POST["username"] or not request.POST["email"] or not request.POST["password"] or not request.POST["confirmation"]:
            messages.error(request, "All fields must be filled out.")
            return HttpResponseRedirect(reverse("register"))
        
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "quote/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user for User and UserProfile models
        try:
            user = User.objects.create_user(username, email, password)
            userprofile = UserProfile(user=user)
            userprofile.save()
            user.save()
        except IntegrityError:
            return render(request, "quote/register.html", {
                "message": "Username already taken."
            })
        
        # If user is created successfully, log them in and redirect to index page
        messages.success(request, f"Welcome to Quotes, {username}!")
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    
    else:
        return render(request, "quote/register.html")


def login_view(request):
    if request.method == "POST":
        # If user submits empty forms, display error message
        if not request.POST["username"] or not request.POST["password"]:
            messages.error(request, "All fields must be filled out.")
            # return render(request, "network/login.html")
            return HttpResponseRedirect(reverse("login"))

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            # If user is authenticated, log them in and redirect to index page
            messages.success(request, f"Welcome back, {username}!")
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            messages.error(request, "Invalid username and/or password.")
            return HttpResponseRedirect(reverse("login"))
            # return render(request, "quote/login.html", {
            #     "message": "Invalid username and/or password."
            # })
    else:
        return render(request, "quote/login.html")


def logout_view(request):
    messages.success(request, "Logged out successfully!")
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def error_404(request):
    return render(request, "quote/404.html")


def about(request):
    return render(request, "quote/about.html")


@login_required
def post_view(request):
    if request.method == "POST":
        user = request.user
        text = request.POST["text"]
        author_name = request.POST["author"]
        categories_input = request.POST["categories"]

        # Split the tags_input string by commas and strip whitespace
        categories = [category.strip() for category in categories_input.split(',')]

        # If bio or image is not provided, set to None
        bio = request.POST["bio"] if request.POST["bio"] else None
        image = request.FILES['author_image'] if 'author_image' in request.FILES else None

        author, created = Author.objects.get_or_create(name=author_name)

        # If author was just created, set additional fields
        if created:
            author.bio = bio
            if image:
                author.image = ImageFile(image) # Assigns image file directly to the author's image field
            author.save()

        # Create a post object and insert post into database
        post = Quote(user=user, text=text, author=author)
        post.save()

        # Add categories to the Category model and add them to the post
        for category_name in categories:
            category, created = Category.objects.get_or_create(name=category_name)
            post.categories.add(category)

        messages.success(request, "Successful post!")

        return HttpResponseRedirect(reverse("index"))
    
    else:
        return render(request, "quote/post.html")
    

def search(request):
    form = SearchForm(request.GET)
    if form.is_valid():
        query = form.cleaned_data['query']
        quotes = Quote.objects.filter(content__icontains=query)
        authors = Author.objects.filter(name__icontains=query)
        users = User.objects.filter(username__icontains=query)
        return render(request, 'quote/search.html', {'quotes': quotes, 'authors': authors, 'users': users, 'query': query})
    else:
        return render(request, 'quote/search.html', {'form': form})

"""
@login_required
def profile(request, view):

    # Filter content returned based on view
    if view == "following":
        # Get the logged in user's following
        user = request.user
        following = user.following.all()
        quotes = Quote.objects.filter(user__in=following).order_by('-timestamp')

    elif view == "followers":
        # Get the logged in user's followers
        user = request.user
        followers = user.followers.all()
        quotes = Quote.objects.filter(user__in=followers).order_by('-timestamp')

    elif view == "liked":
        # Get the logged in user's liked quotes
        user = request.user
        quotes = Quote.objects.filter(likes__user=user).order_by('-timestamp')

    else:
        # Get the user's profile
        user = User.objects.get(pk=view)
        quotes = Quote.objects.filter(user=user).order_by('-timestamp')
"""


def profile(request, id):
    # Get the user's profile
    userprofile = User.objects.get(pk=id)

    quotes = Quote.objects.filter(user=userprofile).order_by('-timestamp')

    paginator = Paginator(quotes, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Get count of quotes, comments, and likes
    quote_count = Quote.objects.filter(user=userprofile).count()
    comment_count = Comment.objects.filter(user=userprofile).count()
    like_count = Like.objects.filter(user=userprofile).count()

    return render(request, "quote/profile.html", {
        'page_obj': page_obj,
        'userprofile': userprofile,
        'quote_count': quote_count,
        'comment_count': comment_count,
        'like_count': like_count,
    })


@login_required
def update_profile(request):
    if request.method == "POST":
        # Get the current user's profile
        user = request.user
        userprofile, created = UserProfile.objects.get_or_create(user=user)

        # Update user profile fields if changed
        if request.POST.get('username'):
            new_username = request.POST.get('username')
            # Check if username is taken
            if User.objects.filter(username=new_username).exists() and new_username != user.username:
                messages.error(request, "Username already taken!")
                return render(request, "quote/update_profile.html")
            else:
                user.username = new_username

        if request.POST.get('email'):
            user.email = request.POST.get('email', user.email)

        if request.POST.get('birthday'):
            userprofile.birthday = request.POST.get('birthday', userprofile.birthday)
        
        if request.POST.get('country_of_origin'):
            userprofile.country_of_origin = request.POST.get('country_of_origin', userprofile.country_of_origin)

        # Handle the uploaded image file if input is not empty
        if 'profile_picture' in request.FILES:
            userprofile.profile_picture = request.FILES['profile_picture']

        # Update password if both password fields are filled and match
        password = request.POST.get('password')
        confirmation = request.POST.get('confirmation')
        if password and confirmation and password == confirmation:
            user.set_password(password)
        elif password or confirmation:
            messages.error(request, "Passwords must match!")
            return render(request, "quote/update_profile.html")

        # Save the changes
        user.save()
        userprofile.save()

        messages.success(request, "Profile updated successfully!")
        return HttpResponseRedirect(reverse("profile", args=(user.id,)))

    else:
        countries = [country.name for country in pycountry.countries]
        return render(request, "quote/update_profile.html", {
            'countries': countries,
        })


def quote(request, id):
    # Get quote from a post that a user clicked on. Display the quote, its comments, like button, like count, and comment form.
    quote = Quote.objects.get(id=id)
    comments = Comment.objects.filter(quote=quote)
    likes = Like.objects.filter(quote=quote)
    user = request.user
    
    return render(request, "quote/quote.html", {
        'quote': quote,
        'comments': comments,
        'likes': likes,
        'user': user,
    })


def quote_of_the_day(request):
    # If a quote is liked more than 5 times in one day, it becomes the quote of the day; otherwise, a random quote is chosen.
    if Quote.objects.filter(likes__gte=5).exists():
        quote_of_the_day = Quote.objects.filter(likes__gte=5).order_by('?').first()
        print(f'Quote liked more than 5 times: {quote_of_the_day}')
    else:
        quote_of_the_day = Quote.objects.order_by('?').first()
        print(f'Random quote: {quote_of_the_day}')

    return render(request, "quote/quote_of_the_day.html", {
        'quote_of_the_day': quote_of_the_day,
    })


def authors(request):
    # Get names of all authors and put in alphabetical order
    authors = Author.objects.all().order_by('name')

    return render(request, "quote/authors.html", {
        'authors': authors,
    })


def author(request, id):
    # Get author info
    author = Author.objects.get(id=id)

    # Get all quotes by author and paginate
    quotes = Quote.objects.filter(author=author).order_by('-timestamp')

    paginator = Paginator(quotes, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "quote/author.html", {
        'author': author,
        'page_obj': page_obj,
    })


def categories(request):
    # Display all quotes in a category
    categories = Category.objects.all().order_by('name')
    
    return render(request, "quote/categories.html", {
        'categories': categories,
    })
    

def category(request, name):
    # Get category info
    category = Category.objects.get(name=name)

    # Get all quotes by category and paginate
    quotes = Quote.objects.filter(categories=category).order_by('-timestamp')

    paginator = Paginator(quotes, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "quote/category.html", {
        'category': category,
        'page_obj': page_obj,
    })


@login_required
def following(request):
    user = request.user

    # Get the logged in user's following
    following = user.following.all()

    # Get following count
    following_count = user.following.all().count()

    # Get all quotes by the users that the logged in user is following and paginate
    try:
        quotes = Quote.objects.filter(user__in=following).order_by('-timestamp')

        paginator = Paginator(quotes, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, "quote/following.html", {
            'page_obj': page_obj,
        })
    except:
        quotes = None
    
    return render(request, "quote/following.html", {
        'quotes': quotes,
        'following_count': following_count,
    })


@csrf_exempt
@login_required
def follow(request, id):
    if request.method == 'POST':
        user = request.user    # user that is following
        followed = User.objects.get(id=id)   # user that is being followed

        # Create a follow object and insert into database
        follow = Follow(follower=user, followed=followed)
        follow.save()

        return JsonResponse({"message": f"You are now following {followed.username}!"}, status=201)
    
    else:
        return JsonResponse({"error": "POST request required."}, status=400)


@csrf_exempt
@login_required
def unfollow(request, id):
    if request.method == 'POST':
        user = request.user    # user that is unfollowing
        unfollowed = User.objects.get(id=id)  # user that is being unfollowed

        # Find the follow object and delete it from the database
        unfollow = Follow.objects.get(follower=user, followed=unfollowed)
        unfollow.delete()

        return JsonResponse({"message": f"You have unfollowed {unfollowed.username}"}, status=201)
    
    else:
        return JsonResponse({"error": "POST request required."}, status=400)
    

@csrf_exempt
@login_required
def like(request, id):
    # Get quote id from AJAX request
    quote_id = json.loads(request.body)['quote_id']

    # Get the quote object from the database
    quote = Quote.objects.get(id=quote_id)
    
    # Set initial user liked quote state to False
    user_liked = False

    # Check if logged in user has already liked the quote
    if quote.likes.filter(id=request.user.id).exists():
        quote.likes.remove(request.user)
    else:
        quote.likes.add(request.user)
        user_liked = True
    
    # Get the users that liked the post
    liked_by = [user.username for user in quote.likes.all()]

    # Create a JSON response to send back to the client
    data = {
        'likes': quote.likes.count(),   # Updated likes count
        'liked_by': liked_by,          # List of users that liked the post
        'user_liked': user_liked,       # Boolean value to determine if user liked the post
    }

    return JsonResponse(data)