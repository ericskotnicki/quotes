from django.test import TestCase
# from django.contrib.auth import get_user_model
from .models import User, UserProfile, Quote, Author, Category, Tag, Follow, Comment, Like
import datetime

"""
COMMANDS:
python manage.py test --keepdb (to keep the test database after running tests)
python manage.py test in the terminal to run all tests
or
python manage.py test quote.tests
python manage.py test quote.tests.QuoteModelTest 
python manage.py test quote.tests.QuoteModelTest.test_quote_content (to run a specific test)
python manage.py test quote.tests.UserProfileModelTest
python manage.py test quote.tests.AuthorModelTest
python manage.py test quote.tests.CategoryModelTest
python manage.py test quote.tests.TagModelTest
python manage.py test quote.tests.FollowModelTest
python manage.py test quote.tests.CommentModelTest
python manage.py test quote.tests.LikeModelTest

"""

class QuoteModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Non-modified objects used by all test methods
        user = User.objects.create(username='testuser')
        author = Author.objects.create(name='Test Author')
        category = Category.objects.create(name='Test Category')
        quote = Quote.objects.create(text='Test Quote', author=author, category=category, user=user)

    def test_quote_content(self):
        quote = Quote.objects.get(id=1)
        expected_object_name = f'{quote.text}'
        self.assertEquals(expected_object_name, 'Test Quote')

    def test_quote_author(self):
        quote = Quote.objects.get(id=1)
        expected_author = f'{quote.author.name}'
        self.assertEquals(expected_author, 'Test Author')

    def test_quote_category(self):
        quote = Quote.objects.get(id=1)
        expected_category = f'{quote.category.name}'
        self.assertEquals(expected_category, 'Test Category')

    def test_quote_user(self):
        quote = Quote.objects.get(id=1)
        expected_user = f'{quote.user.username}'
        self.assertEquals(expected_user, 'testuser')


class UserProfileModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        User.objects.create_user(username='testuser', password='12345')
        test_user = User.objects.get(username='testuser')
        UserProfile.objects.create(user=test_user, country_of_origin='Test Country', birthday=datetime.date(1990, 5, 4), interests='Coding')

    def test_user_label(self):
        userprofile = UserProfile.objects.get(id=1)
        field_label = userprofile._meta.get_field('user').verbose_name
        self.assertEqual(field_label, 'user')

    def test_country_of_origin_label(self):
        userprofile = UserProfile.objects.get(id=1)
        field_label = userprofile._meta.get_field('country_of_origin').verbose_name
        self.assertEqual(field_label, 'country of origin')

    def test_birthday_label(self):
        userprofile = UserProfile.objects.get(id=1)
        field_label = userprofile._meta.get_field('birthday').verbose_name
        self.assertEqual(field_label, 'birthday')

    def test_interests_label(self):
        userprofile = UserProfile.objects.get(id=1)
        field_label = userprofile._meta.get_field('interests').verbose_name
        self.assertEqual(field_label, 'interests')

    def test_country_of_origin_max_length(self):
        userprofile = UserProfile.objects.get(id=1)
        max_length = userprofile._meta.get_field('country_of_origin').max_length
        self.assertEqual(max_length, 200)

    def test_object_name_is_username_country_of_origin_birthday_interests(self):
        userprofile = UserProfile.objects.get(id=1)
        expected_object_name = f'User: {userprofile.user.username}, Country of Origin: {userprofile.country_of_origin}, Birthday: {userprofile.birthday}, Interests: {userprofile.interests}'
        self.assertEqual(str(userprofile), expected_object_name)


class AuthorModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Non-modified objects used by all test methods
        author = Author.objects.create(name='Test Author')

    def test_author_content(self):
        author = Author.objects.get(id=1)
        expected_object_name = f'{author.name}'
        self.assertEquals(expected_object_name, 'Test Author')


class CategoryModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Non-modified objects used by all test methods
        category = Category.objects.create(name='Test Category')

    def test_category_content(self):
        category = Category.objects.get(id=1)
        expected_object_name = f'{category.name}'
        self.assertEquals(expected_object_name, 'Test Category')


class TagModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Non-modified objects used by all test methods
        tag = Tag.objects.create(name='Test Tag')

    def test_tag_content(self):
        tag = Tag.objects.get(id=1)
        expected_object_name = f'{tag.name}'
        self.assertEquals(expected_object_name, 'Test Tag')


class FollowModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        User.objects.create_user(username='follower', password='12345')
        User.objects.create_user(username='followed', password='12345')
        follower = User.objects.get(username='follower')
        followed = User.objects.get(username='followed')
        Follow.objects.create(follower=follower, followed=followed)

    def test_follow(self):
        follow = Follow.objects.get(id=1)
        self.assertEqual(follow.follower.username, 'follower')
        self.assertEqual(follow.followed.username, 'followed')


class CommentModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        User.objects.create_user(username='commenter', password='12345')
        commenter = User.objects.get(username='commenter')
        author = Author.objects.create(name='author')
        category = Category.objects.create(name='category')
        quote = Quote.objects.create(text='quote', author=author, user=commenter, category=category)
        Comment.objects.create(text='comment', user=commenter, quote=quote)

    def test_comment(self):
        comment = Comment.objects.get(id=1)
        self.assertEqual(comment.text, 'comment')
        self.assertEqual(comment.user.username, 'commenter')
        self.assertEqual(comment.quote.text, 'quote')


class LikeModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        User.objects.create_user(username='liker', password='12345')
        liker = User.objects.get(username='liker')
        author = Author.objects.create(name='author')
        category = Category.objects.create(name='category')
        quote = Quote.objects.create(text='quote', author=author, user=liker, category=category)
        comment = Comment.objects.create(text='comment', user=liker, quote=quote)
        Like.objects.create(user=liker, quote=quote, comment=comment, author=author)

    def test_like(self):
        like = Like.objects.get(id=1)
        self.assertEqual(like.user.username, 'liker')
        self.assertEqual(like.quote.text, 'quote')
        self.assertEqual(like.comment.text, 'comment')
        self.assertEqual(like.author.name, 'author')