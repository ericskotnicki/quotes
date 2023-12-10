from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
# from django.db.models.signals import post_save
# from django.dispatch import receiver


class User(AbstractUser):
    """username, password, date_joined, email, first_name, last_name, is_active, is_staff, is_superuser, last_login"""
    
    # Helper methods
    
    # Checks if user has liked a quote
    def has_liked(self, quote):
        return self.likes.filter(quote=quote).exists()


class UserProfile(models.Model):
    """User profile model for additional user information (optional input)"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    country_of_origin = models.CharField(max_length=200, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True)
    birthday = models.DateField(blank=True, null=True)

    def __str__(self):
        return f'User: {self.user.username}, Country of Origin: {self.country_of_origin}, Birthday: {self.birthday}'


class Author(models.Model):
    """Represents an author for quotes including the author's name, bio, and image."""
    name = models.CharField(max_length=200)
    bio = models.TextField(blank=True)
    image = models.ImageField(upload_to='authors/', blank=True)

    def __str__(self):
        return f'Authors name: {self.name}, bio: {self.bio}'
    

class Category(models.Model):
    """Represents a category for quotes."""
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Quote(models.Model):
    """Represents a quote containing the quote itself, author, categories, the user that posted the quote, and the timestamp."""
    text = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='quotes')
    categories = models.ManyToManyField(Category, related_name='quotes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quotes')    # user that posted the quote
    timestamp = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f'"{self.text}" - {self.author}'
    
    # Helper methods
    def is_liked_by_user(self, user):
        return self.likes.filter(user=user).exists()
    

class Follow(models.Model):
    """Represents user's followers and following."""
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    timestamp = models.DateTimeField(auto_now_add=True)

    # user.following.all() -> returns all users that the user is following
    # user.followers.all() -> returns all users that are following the user


class Comment(models.Model):
    """Represents comments on quotes."""
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE, related_name='comments')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'"{self.text}" - {self.user.username}'

    # user = User.objects.get(username='username') -> get user object
    # comments = user.comment_set.all() -> returns all comments posted by the user ('comment_set' is a default related name)

    # comment.user -> returns the user that posted the comment
    # quote.comments.all() -> returns all comments on the quote


class Like(models.Model):
    """Represents likes on quotes, comments, and authors."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE, related_name='likes', null=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='likes', null=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='likes', null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    # user = User.objects.get(username='username') -> get user object
    # likes = user.like_set.all() -> returns all likes by the user ('like_set' is a default related name)

    # like.user -> returns the user that liked the quote
    # quote.likes.all() -> returns all likes on the quote


class Bookmark(models.Model):
    """Represents bookmarks on posted quotes."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmarks')
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE, related_name='bookmarks', null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
