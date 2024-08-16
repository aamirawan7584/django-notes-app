from django.urls import path
from .views import NoteDelete, NoteList, NoteDetail, NoteCreate, NoteUpdate


urlpatterns = [
    path("", NoteList.as_view(), name="notes"),
    path("note/<int:pk>/", NoteDetail.as_view(), name="note"),
    path("note-create/", NoteCreate.as_view(), name="note-create"),
    path("note-update/<int:pk>/", NoteUpdate.as_view(), name="note-update"),
    path("note-delete/<int:pk>/", NoteDelete.as_view(), name="note-delete"),
]
