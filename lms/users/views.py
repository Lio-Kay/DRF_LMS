from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model


from users.serializers import UserOwnerSerializer, UserViewOnlySerializer
from users.permissions import IsOwner


User = get_user_model()


class UserCreateListAPIView(generics.ListCreateAPIView):
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        data = request.data
        user = User.objects.create_user(
            email=data.get('email'),
            password=data.get('password'),

        )

        serializer = self.get_serializer(user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserViewOnlySerializer
        return UserOwnerSerializer


class UserRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    lookup_field = 'pk'

    def get_serializer_class(self):
        if self.request.user.pk == self.get_object().pk:
            return UserOwnerSerializer
        return UserViewOnlySerializer

    def get_permissions(self):
        permission_classes = []
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            permission_classes = [IsOwner]
        return [permission() for permission in permission_classes]
