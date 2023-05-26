from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Women, Categories

User = get_user_model()


class WomenPagesTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Создадим запись в БД
        cls.category = Categories.objects.create(
            name='Тестовая категория',
            slug='testovaya-categoriya'
        )
        cls.woman = Women.objects.create(
            title='Тестовый заголовок',
            slug='testoviy-zagolovok',
            cat=cls.category
        )
        cls.authorized_menu = [{'title': "О сайте", 'url_name': 'about'},
                {'title': "Добавить статью", 'url_name': 'add_page'},
                {'title': "Обратная связь", 'url_name': 'contact'}
                ]
        cls.guest_menu = [{'title': "О сайте", 'url_name': 'about'},
                {'title': "Обратная связь", 'url_name': 'contact'}
                ]

    def setUp(self):
        # Создаем неавторизованный клиент
        self.guest_client = Client()
        # Создаем авторизованный клиент
        self.user = User.objects.create_user(username='NickTse')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    # Проверяем используемые шаблоны
    def test_pages_uses_correct_template(self):
        # Собираем в словарь пары "имя_html_шаблона: reverse(name)"
        templates_pages_names = {
            'women/index.html': reverse('home'),
            'women/about.html': reverse('about'),
            'women/contact.html': reverse('contact'),
            'women/register.html': reverse('register'),
            'women/login.html': reverse('login'),
            'women/post.html': reverse('post', kwargs={'post_slug': 'testoviy-zagolovok'}),
            'women/index.html': reverse('category', kwargs={'cat_slug': 'testovaya-categoriya'})
        }
        # Проверяем, что при обращении к name вызывается соответствующий HTML-шаблон
        for template, reverse_name in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    # Проверяем, что словарь context страницы /
    # в первом элементе списка posts содержит ожидаемые значения
    def test_home_page_show_correct_context(self):
        auth_response = self.authorized_client.get(reverse('home'))

        # Взяли первый элемент из списка и проверили, что его содержание
        # совпадает с ожидаемым
        first_post = auth_response.context['posts'][0]
        self.assertEqual(first_post.title, 'Тестовый заголовок')

        first_cat = auth_response.context['cats'][0]
        self.assertEqual(first_cat.name, 'Тестовая категория')

        authorized_menu = auth_response.context['menu']
        self.assertEqual(authorized_menu, WomenPagesTest.authorized_menu)

        guest_response = self.guest_client.get(reverse('home'))

        guest_menu = guest_response.context['menu']
        self.assertEqual(guest_menu, WomenPagesTest.guest_menu)

    def test_post_page_show_correct_context(self):
        auth_response = self.authorized_client.get(reverse('post', kwargs={'post_slug': 'testoviy-zagolovok'}))

        post = auth_response.context.get('post')
        self.assertEqual(post.title, 'Тестовый заголовок')

        first_cat = auth_response.context['cats'][0]
        self.assertEqual(first_cat.name, 'Тестовая категория')

        authorized_menu = auth_response.context['menu']
        self.assertEqual(authorized_menu, WomenPagesTest.authorized_menu)

        guest_response = self.guest_client.get(reverse('post', kwargs={'post_slug': 'testoviy-zagolovok'}))

        guest_menu = guest_response.context['menu']
        self.assertEqual(guest_menu, WomenPagesTest.guest_menu)

    def test_category_page_show_correct_context(self):
        auth_response = self.authorized_client.get(reverse('category', kwargs={'cat_slug': 'testovaya-categoriya'}))

        first_post = auth_response.context['posts'][0]
        self.assertEqual(first_post.title, 'Тестовый заголовок')

        first_cat = auth_response.context['cats'][0]
        self.assertEqual(first_cat.name, 'Тестовая категория')

        title = auth_response.context.get('title')
        self.assertEqual(title, 'Категория - Тестовая категория')

        cat_selected = auth_response.context.get('cat_selected')
        self.assertEqual(cat_selected, 'testovaya-categoriya')

        authorized_menu = auth_response.context['menu']
        self.assertEqual(authorized_menu, WomenPagesTest.authorized_menu)

        guest_response = self.guest_client.get(reverse('category', kwargs={'cat_slug': 'testovaya-categoriya'}))
        guest_menu = guest_response.context['menu']
        self.assertEqual(guest_menu, WomenPagesTest.guest_menu)


class PaginatorViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_posts = 4

        cls.category = Categories.objects.create(
            name=f'Тестовая категория',
            slug=f'testovaya-categoriya'
        )

        for post_id in range(number_of_posts):
            Women.objects.create(
                title=f'Тестовый заголовок {post_id}',
                slug=f'testoviy-zagolovok-{post_id}',
                cat=cls.category
            )

    def setUp(self):
        self.client = Client()

    def test_first_page_contains_three_records(self):
        response = self.client.get(reverse('home'))
        # Проверка: количество постов на первой странице равно 3.
        self.assertEqual(len(response.context['object_list']), 3)

    def test_second_page_contains_three_records(self):
        # Проверка: на второй странице должен быть 1 пост.
        response = self.client.get(reverse('home') + '?page=2')
        self.assertEqual(len(response.context['object_list']), 1)

