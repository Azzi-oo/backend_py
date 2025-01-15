from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticated, AllowAny
from general.api.serializers import UserListSerializer, UserRegistrationSerializer
from general.models import User


class UserViewSet(
    CreateModelMixin,
    ListModelMixin,
    GenericViewSet,
    ):
    queryset = User.objects.all().order_by("-id")
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "create":
            return UserRegistrationSerializer
        return UserListSerializer
    
    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [AllowAny]
        return super().get_permissions()