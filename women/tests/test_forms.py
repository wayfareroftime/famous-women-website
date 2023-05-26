from ..forms import AddPostForm, ContactForm, RegisterUserForm, LoginUserForm
from django.http import HttpRequest
from ..models import Women, Categories
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

User = get_user_model()


class AddPostFormTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Создаем запись в базе данных для проверки сушествующего slug
        cls.category = Categories.objects.create(
            name='Тестовая категория',
            slug='testovaya-categoriya'
        )
        cls.woman = Women.objects.create(
            title='Тестовый заголовок',
            slug='first',
            cat=cls.category
        )

    def test_create_post(self):
        # Подсчитаем количество записей в Task
        posts_count = Women.objects.count()
        # Отправляем POST-запрос
        request = HttpRequest()
        request.POST = {
            'title': 'Тестовый заголовок',
            'slug': 'testoviy-zagolovok',
            'content': 'Тестовая биография',
            'cat': AddPostFormTest.category.pk
        }
        form = AddPostForm(request.POST)
        if form.is_valid():
            form.save()
        # Проверяем, увеличилось ли число постов
        self.assertEqual(Women.objects.count(), posts_count + 1)
        # Проверяем, что создалась запись с заданным слагом
        self.assertTrue(
            Women.objects.filter(
                title='Тестовый заголовок',
                slug='testoviy-zagolovok',
                content='Тестовая биография',
                cat=AddPostFormTest.category.pk
            ).exists()
        )

    def test_cant_create_existing_slug(self):
        posts_count = Women.objects.count()
        # Отправляем POST-запрос
        request = HttpRequest()
        request.POST = {
            'title': 'Тестовый заголовок',
            'slug': 'first',
            'content': 'Тестовая биография',
            'cat': AddPostFormTest.category.pk
        }
        form = AddPostForm(request.POST)
        if form.is_valid():
            form.save()
        # Убедимся, что запись в базе данных не создалась
        self.assertEqual(Women.objects.count(), posts_count)

    def test_cant_create_long_title(self):
        posts_count = Women.objects.count()
        # Отправляем POST-запрос
        request = HttpRequest()
        request.POST = {
            'title': '6'*266,
            'slug': 'testoviy-zagolovok',
            'content': 'Тестовая биография',
            'cat': AddPostFormTest.category.pk
        }
        form = AddPostForm(request.POST)
        if form.is_valid():
            form.save()
        # Убедимся, что запись в базе данных не создалась
        self.assertEqual(Women.objects.count(), posts_count)


class ContactFormTest(TestCase):

    def setUp(self):
        # Создаем неавторизованный клиент
        self.client = Client()

    def test_redirect_after_post(self):
        form_data = {
            'name': 'Тестовый пользователь',
            'email': 'test@test.ru',
            'content': 'Тестовое сообщение',
        }
        # Отправляем POST-запрос
        response = self.client.post(
            reverse('contact'),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, reverse('home'))

    def test_label(self):
        form = ContactForm()
        labels = {
            'name': 'Имя',
            'email': 'Почта',
            'content': 'Сообщение',
        }
        for field, expected_value in labels.items():
            with self.subTest(field=field):
                self.assertEqual(form.fields[field].label, expected_value)


class RegisterUserFormTest(TestCase):

    def setUp(self):
        # Создаем неавторизованный клиент
        self.client = Client()

    def test_redirect_after_post(self):
        form_data = {
            'username': 'testuser',
            'email': 'test@test.ru',
            'password1': 'testpasswd',
            'password2': 'testpasswd',
        }
        # Отправляем POST-запрос
        response = self.client.post(
            reverse('register'),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, reverse('home'))

    def test_label(self):
        form = RegisterUserForm()
        labels = {
            'username': 'Логин',
            'email': 'Почта',
            'password1': 'Пароль',
            'password2': 'Повтор пароля',
        }
        for field, expected_value in labels.items():
            with self.subTest(field=field):
                self.assertEqual(form.fields[field].label, expected_value)


class LoginUserFormTest(TestCase):

    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'testpasswd'}
        User.objects.create_user(**self.credentials)

    def test_redirect_after_post(self):
        # Отправляем POST-запрос
        response = self.client.post(
            reverse('login'),
            self.credentials,
            follow=True
        )
        self.assertRedirects(response, reverse('home'))

    def test_label(self):
        form = LoginUserForm()
        labels = {
            'username': 'Логин',
            'password': 'Пароль',
        }
        for field, expected_value in labels.items():
            with self.subTest(field=field):
                self.assertEqual(form.fields[field].label, expected_value)





