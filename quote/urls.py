
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register, name='register'),
    path('about', views.about, name='about'),
    path('404', views.error_404, name='404'),
    path('post', views.post_view, name='post'),
    path('search', views.search, name='search'),
    # path('profile/<str:view>/', views.profile, name='profile'),
    path('profile/<int:id>/', views.profile, name='profile'),
    path('update_profile', views.update_profile, name='update_profile'),
    path('quote/<int:id>', views.quote, name='quote'),
    path('quote_of_the_day', views.quote_of_the_day, name='quote_of_the_day'),
    path('authors', views.authors, name='authors'),
    path('author/<int:id>', views.author, name='author'),
    path('categories', views.categories, name='categories'),
    path('category/<str:name>', views.category, name='category'),
    path('following', views.following, name='following'),

    # API Routes
    path('follow/<int:id>', views.follow, name='follow'),
    path('unfollow/<int:id>', views.unfollow, name='unfollow'),
    path('like/<int:id>', views.like, name='like'),
    path('comment/<int:id>', views.comment, name='comment'),
    path('edit/<int:id>', views.edit, name='edit'),
]