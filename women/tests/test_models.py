from django.test import TestCase

from ..models import Women, Categories


class WomenModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.category = Categories.objects.create(
            name='Тестовая категория',
            slug='testovaya-categoriya'
        )
        cls.woman = Women.objects.create(
            title='Тестовый заголовок',
            slug='testoviy-zagolovok',
            cat=cls.category
        )

    def test_verbose_name(self):
        woman = WomenModelTest.woman
        verbose_names = {
            'title': 'Заголовок',
            'slug': 'URL',
            'content': 'Текст статьи',
            'photo': 'Фото',
            'time_create': 'Время создания',
            'time_update': 'Время изменения',
            'is_published': 'Публикация',
            'cat': 'Категории'
        }
        for field, expected_value in verbose_names.items():
            with self.subTest(field=field):
                self.assertEqual(
                    woman._meta.get_field(field).verbose_name, expected_value)

    def test_object_name_is_title(self):
        woman = WomenModelTest.woman
        expected_object_name = woman.title
        self.assertEqual(expected_object_name, str(woman))

    def test_get_absolute_url(self):
        woman = WomenModelTest.woman
        self.assertEqual(woman.get_absolute_url(), '/post/testoviy-zagolovok/')


class CategoriesModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.category = Categories.objects.create(
            name='Тестовая категория',
            slug='testovaya-categoriya'
        )

    def test_verbose_name(self):
        category = CategoriesModelTest.category
        verbose_names = {
            'name': 'Категория',
            'slug': 'URL'
        }
        for field, expected_value in verbose_names.items():
            with self.subTest(field=field):
                self.assertEqual(
                    category._meta.get_field(field).verbose_name, expected_value)

    def test_object_name_is_title(self):
        category = CategoriesModelTest.category
        expected_object_name = category.name
        self.assertEqual(expected_object_name, str(category))

    def test_get_absolute_url(self):
        category = CategoriesModelTest.category
        self.assertEqual(category.get_absolute_url(), '/category/testovaya-categoriya/')
