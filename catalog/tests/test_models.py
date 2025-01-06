from django.test import TestCase
from django.urls import reverse
from catalog.models import Topic, Redactor, Newspaper
from django.utils import timezone

class TestTopic(TestCase):
    def setUp(self):
        self.topic1 = Topic.objects.create(name="Politics")
        self.topic2 = Topic.objects.create(name="Sports")

    def test_topic_str(self):
        """Test the string representation of the Topic model"""
        self.assertEqual(str(self.topic1), "Politics")
        self.assertEqual(str(self.topic2), "Sports")

    def test_topic_creation(self):
        """Test that topics are created correctly"""
        topic = Topic.objects.create(name="Technology")
        self.assertEqual(topic.name, "Technology")
        self.assertTrue(Topic.objects.filter(name="Technology").exists())


class TestRedactor(TestCase):
    def setUp(self):
        self.redactor = Redactor.objects.create_user(
            username="johndoe", password="password123", years_of_experience=5
        )

    def test_redactor_str(self):
        """Test the string representation of the Redactor model"""
        self.assertEqual(str(self.redactor), "johndoe")

    def test_redactor_get_absolute_url(self):
        """Test the URL returned by get_absolute_url"""
        url = self.redactor.get_absolute_url()
        expected_url = reverse("catalog:redactor-detail", kwargs={"pk": self.redactor.pk})
        self.assertEqual(url, expected_url)

    def test_redactor_creation(self):
        """Test that Redactor is created with the correct fields"""
        redactor = Redactor.objects.create_user(
            username="janedoe", password="password123", years_of_experience=3
        )
        self.assertEqual(redactor.username, "janedoe")
        self.assertEqual(redactor.years_of_experience, 3)


class TestNewspaper(TestCase):
    def setUp(self):
        self.topic = Topic.objects.create(name="Technology")
        self.redactor1 = Redactor.objects.create_user(
            username="redactor1", password="password123"
        )
        self.redactor2 = Redactor.objects.create_user(
            username="redactor2", password="password123"
        )

        self.newspaper = Newspaper.objects.create(
            title="Tech News Daily",
            content="The latest updates in technology.",
            published_date=timezone.now(),
            topic=self.topic
        )
        # Add redactors to the newspaper
        self.newspaper.publishers.add(self.redactor1, self.redactor2)

    def test_newspaper_str(self):
        """Test the string representation of the Newspaper model"""
        self.assertEqual(str(self.newspaper), "Tech News Daily")

    def test_newspaper_creation(self):
        """Test that a Newspaper is created correctly"""
        self.assertEqual(self.newspaper.title, "Tech News Daily")
        self.assertEqual(self.newspaper.topic.name, "Technology")
        self.assertEqual(self.newspaper.publishers.count(), 2)

    def test_newspaper_publishers(self):
        """Test the ManyToMany relationship between Newspaper and Redactor"""
        # Check if the redactors are correctly associated with the newspaper
        self.assertIn(self.redactor1, self.newspaper.publishers.all())
        self.assertIn(self.redactor2, self.newspaper.publishers.all())

    def test_newspaper_topic(self):
        """Test the ForeignKey relationship between Newspaper and Topic"""
        self.assertEqual(self.newspaper.topic.name, "Technology")


