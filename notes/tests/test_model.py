from django.test import TestCase

from notes.models import Note


class AuthorModelTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        # Set up non-modified objects used by all test methods
        Note.objects.create(title="Test Title", description="Test Description")

    def test_title_label(self) -> None:
        note: Note = Note.objects.get(id=1)
        title: str = note._meta.get_field("title").verbose_name
        self.assertEqual(title, "title")

    def test_description_label(self) -> None:
        note: Note = Note.objects.get(id=1)
        description: str = note._meta.get_field("description").verbose_name
        self.assertEqual(description, "description")

    def test_title_max_length(self) -> None:
        note: Note = Note.objects.get(id=1)
        max_length: int = note._meta.get_field("title").max_length
        self.assertEqual(max_length, 200)

    def test_get_absolute_url(self) -> None:
        note: Note = Note.objects.get(id=1)
        self.assertEqual(note.get_absolute_url(), "/note/1/")
