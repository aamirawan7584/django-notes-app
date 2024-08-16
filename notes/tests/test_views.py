from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

TEST_USER_DATA = {
    "username1": "user1",
    "password1": "1X<ISRUkw+tuK1X<ISRUkw+tuK",
    "username2": "user2",
    "password2": "2HJ1vRV0Z&3iD",
}


class NoteCreateUpdateBase(TestCase):
    """Base class for NoteCreate and NoteUpdate Tests"""

    def setUp(self) -> None:
        # create two users
        self.user1: User = User.objects.create_user(
            username=TEST_USER_DATA["username1"], password=TEST_USER_DATA["password1"]
        )
        self.user2: User = User.objects.create_user(
            username=TEST_USER_DATA["username2"], password=TEST_USER_DATA["password2"]
        )
        self.user1.save()
        self.user2.save()
        return super().setUp()


class NoteCreateTest(NoteCreateUpdateBase):
    def test_redirect_if_not_logged_in(self) -> None:
        """
        If user is not logged in, redirect to login page.
        """
        response = self.client.get(reverse("note-create"))
        self.assertRedirects(response, "/accounts/login/?next=/note-create/")

    def test_successful_note_creation_for_logged_in_user(self) -> None:
        _ = self.client.login(
            username=TEST_USER_DATA["username1"], password=TEST_USER_DATA["password1"]
        )

        notes = {"title": "test note", "description": "test note_description"}
        response = self.client.post(reverse("note-create"), notes)
        # after successful creation of note it should redirect back to notes
        self.assertRedirects(response, reverse("notes"))

        # lets check that this note has been created successfully

        response = self.client.get(reverse("notes"))
        self.assertEqual(response.status_code, 200)

        # Check our user is logged in
        self.assertEqual(str(response.context["user"]), TEST_USER_DATA["username1"])

        # count should be 1
        self.assertEqual(response.context["count"], 1)

    def test_each_user_should_get_his_own_notes(self) -> None:
        _ = self.client.login(
            username=TEST_USER_DATA["username1"], password=TEST_USER_DATA["password1"]
        )

        note_detail = {"title": "test note", "description": "test note_description"}

        # create 5 notes for user1
        for _ in range(5):
            _ = self.client.post(reverse("note-create"), note_detail)

        _ = self.client.login(
            username=TEST_USER_DATA["username2"], password=TEST_USER_DATA["password2"]
        )

        # create 5 notes for user2
        for _ in range(5):
            _ = self.client.post(reverse("note-create"), note_detail)

        # now both user should get their own notes created by them
        response = self.client.get(reverse("notes"))
        self.assertEqual(response.status_code, 200)

        # Check our user is logged in
        self.assertEqual(str(response.context["user"]), TEST_USER_DATA["username2"])

        # count should be 5
        self.assertEqual(response.context["count"], 5)


class TestUpdateNote(NoteCreateUpdateBase):
    """Test UpdateNote functionality.Update for logged in users should work properly"""

    def test_update_note(self) -> None:
        # lets create a note
        _ = self.client.login(
            username=TEST_USER_DATA["username1"], password=TEST_USER_DATA["password1"]
        )
        note_detail: dict[str, str] = {
            "title": "test note",
            "description": "test note_description",
        }

        # lets create a note
        _ = self.client.post(reverse("note-create"), note_detail)

        response = self.client.get(reverse("notes"))

        notes = response.context["notes"]
        note_absolute_url = ""
        note_id = 0
        for note in notes:
            # note belong to current user
            self.assertEqual(response.context["user"], note.user)
            note_absolute_url = note.get_absolute_url()
            note_id = note.id

        # lets update the note

        updated_note_detail: dict[str, str] = {
            "title": "test note_updated",
            "description": "test note_description_updated",
        }

        _ = self.client.post(note_absolute_url, updated_note_detail)

        response = self.client.get(reverse("notes"))

        updated_notes = response.context["notes"]

        for note in updated_notes:
            # confirm updated note id is same as original
            self.assertEqual(note.id, note_id)
            self.assertEqual(note.title, updated_note_detail["title"])
            self.assertEqual(note.description, updated_note_detail["description"])

    def test_update_note_should_work_for_only_author(self) -> None:
        # lets create a note
        _ = self.client.login(
            username=TEST_USER_DATA["username1"], password=TEST_USER_DATA["password1"]
        )
        note_detail: dict[str, str] = {
            "title": "test note",
            "description": "test note_description",
        }

        # lets create a note
        _ = self.client.post(reverse("note-create"), note_detail)

        response = self.client.get(reverse("notes"))
        notes = response.context["notes"]
        note_absolute_url = ""
        note_id = 0

        _ = self.client.login(
            username=TEST_USER_DATA["username2"], password=TEST_USER_DATA["password2"]
        )
        updated_note_detail: dict[str, str] = {
            "title": "test note_updated",
            "description": "test note_description_updated",
        }

        response = self.client.post(note_absolute_url, updated_note_detail)
        self.assertEqual(response.status_code, 405)
