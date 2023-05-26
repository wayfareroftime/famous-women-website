from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from ..models import Women, Categories

User = get_user_model()


class URLTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.category = Categories.objects.create(
            name='Тестовая категория',
            slug='testovaya-categoriya'
        )
        Women.objects.create(
            title='Тестовый заголовок',
            slug='testoviy-zagolovok',
            cat=cls.category
        )

    def setUp(self):
        # Создаем неавторизованный клиент
        self.guest_client = Client()
        # Создаем пользователя
        self.user = User.objects.create_user(username='HasNoName')
        # Создаем второй клиент
        self.authorized_client = Client()
        # Авторизуем пользователя
        self.authorized_client.force_login(self.user)

    def test_urls_exist_at_desired_location(self):
        urls = ['/', '/about/', '/contact/', '/register/', '/login/', '/post/testoviy-zagolovok/',
                '/category/testovaya-categoriya/']
        for url in urls:
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertEqual(response.status_code, 200)

    def test_url_exist_at_desired_location_authorized(self):
        response = self.authorized_client.get('/addpage/')
        self.assertEqual(response.status_code, 200)

    def test_urls_uses_correct_template(self):
        templates_url_names = {
            'women/index.html': '/',
            'women/about.html': '/about/',
            'women/contact.html': '/contact/',
            'women/register.html': '/register/',
            'women/login.html': '/login/',
            'women/post.html': '/post/testoviy-zagolovok/',
            'women/index.html': '/category/testovaya-categoriya/'
        }
        for template, address in templates_url_names.items():
            with self.subTest(adress=address):
                response = self.authorized_client.get(address)
                self.assertTemplateUsed(response, template)
