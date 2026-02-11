from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ConversationViewSet, MessageViewSet

router = DefaultRouter()
router.register("conversations", ConversationViewSet, basename="conversations")

message_list_create = MessageViewSet.as_view(
    {
        "get": "list",
        "post": "create",
    }
)

urlpatterns = [
    path("", include(router.urls)),

    # Nested endpoint:
    path(
        "conversations/<int:conversation_pk>/messages/",
        message_list_create,
        name="conversation-messages",
    ),
]