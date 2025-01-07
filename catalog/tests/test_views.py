from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from catalog.models import Topic, Redactor, Newspaper

TOPICS_URL = reverse('catalog:topic-list')
REDACTORS_URL = reverse('catalog:redactor-list')
NEWSPAPERS_URL = reverse('catalog:newspaper-list')


TOPICS_LIST = [
    {
        "name": "Business",
    },
    {
        "name": "Sport"
    },
    {
        "name": "Technology",
    },
]


def make_a_custom_topics_objects() -> None:
    for topic in TOPICS_LIST:
        Topic.objects.create(**topic)


class PublicTestTopics(TestCase):
    def setUp(self):
        self.client = Client()

    def test_topics_page_for_unlogged_user(self):
        response = self.client.get(TOPICS_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateTestTopics(TestCase):
    def setUp(self):
        self.redactor = get_user_model().objects.create_user(
            username="test_redactor",
            password="Test1111",
        )
        self.client.force_login(self.redactor)

    def test_topics_page_for_logged_user(self):
        for topic in TOPICS_LIST:
            Topic.objects.create(**topic)

        response = self.client.get(TOPICS_URL)
        self.assertEqual(response.status_code, 200)
        topics = Topic.objects.all()
        self.assertEqual(
            list(topics),
            list(response.context["topic_list"]),
        )
        self.assertTemplateUsed(
            response,
            "catalog/topic_list.html",
        )


class PublicTestRedactor(TestCase):
    def setUp(self):
        self.client = Client()

    def test_redactors_page_for_unlogged_user(self):
        response = self.client.get(REDACTORS_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateTestRedactor(TestCase):
    def setUp(self):
        self.redactor = get_user_model().objects.create_user(
            username="test_redactor",
            password="Test1111",
        )
        self.client.force_login(self.redactor)

    def test_redactors_page_for_logged_in_user(self):
        redactors = [
            {
                "username": "test_redactor",
                "password": "Test1111",
                "first_name": "Test",
                "last_name": "Test",
                "years_of_experience": 2,
            },
            {
                "username": "test_redactor_2",
                "password": "Test2222",
                "first_name": "Test",
                "last_name": "Two",
                "years_of_experience": 2,
            },
            {
                "username": "test_redactor_3",
                "password": "Test3333",
                "first_name": "Test",
                "last_name": "Three",
                "years_of_experience": 3,
            },
        ]
        for redactor in redactors:
            Redactor.objects.create(**redactor)
            response = self.client.get(REDACTORS_URL)
            self.assertEqual(response.status_code, 200)
            redactors_list = Redactor.objects.all()
            response_redactors = response.context["redactor_list"]
            for response_redactor in response_redactors:
                self.assertIn(
                    response_redactor,
                    list(redactors_list),
                )
            search_username = "2"
            filter_redactors = Redactor.objects.filter(
                username__icontains=search_username
            )
            response = self.client.get(
                REDACTORS_URL,
                {
                    "username": search_username,
                }
            )
            self.assertEqual(
                list(filter_redactors),
                list(response.context["redactor_list"]),
            )
            self.assertTemplateUsed(
                response,
                "catalog/redactor_list.html",
            )
            self.assertEqual(
                response.context["search_form"].initial["username"],
                search_username,
            )


class PublicTestNewspaper(TestCase):
    def setUp(self):
        self.client = Client()

    def test_newspaper_page_for_unlogged_user(self):
        response = self.client.get(NEWSPAPERS_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateTestNewspaper(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="Test1111",
        )
        self.client.force_login(self.user)

    def test_newspaper_page_for_logged_in_user(self):
        make_a_custom_topics_objects()
        topics = {
            topic.name:
                topic for topic in Topic.objects.all()
        }
        newspapers = [
            {
                "title": "Test",
                "topic": topics["Business"],
            },
            {
                "title": "Test2",
                "topic": topics["Technology"],
            },
            {
                "title": "Test3",
                "topic": topics["Sport"],
            }
        ]
        for newspaper in newspapers:
            Newspaper.objects.create(**newspaper)
            response = self.client.get(NEWSPAPERS_URL)
            self.assertEqual(response.status_code, 200)
            newspaper_list = Newspaper.objects.all()
            res_newspapers = response.context["newspaper_list"]
            for res_newspaper in res_newspapers:
                self.assertIn(
                    res_newspaper,
                    list(newspaper_list),
                )
            search_title = "Test"
            filtered_newspapers = Newspaper.objects.filter(title__icontains=search_title)
            response = self.client.get(NEWSPAPERS_URL, {"title": search_title})
            self.assertEqual(
                list(filtered_newspapers),
                list(response.context["newspaper_list"]),
            )
            self.assertTemplateUsed(
                response,
                "catalog/newspaper_list.html",
            )
            self.assertEqual(
                response.context["search_form"].initial["title"],
                search_title,
            )
