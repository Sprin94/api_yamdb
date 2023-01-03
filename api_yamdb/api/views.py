from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework import filters
from rest_framework.decorators import action
from users.serializers import UserSerializer
from .permission import IsAdmin

User = get_user_model()


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'username'
    http_method_names = ['get', 'post', 'patch', 'delete',
                         'head', 'options', 'trace']
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=username',)
    permission_classes = (IsAdmin,)

    @action(detail=False, methods=['GET', 'PATCH'], url_path='me',
            permission_classes=(IsAuthenticated,))
    def me(self, request):
        if request.method == 'GET':
            serializer = self.serializer_class(request.user)
            return Response(serializer.data)
        if request.method == 'PATCH':
            serializer = self.serializer_class(
                instance=request.user,
                data=request.POST,
                partial=True
            )
            serializer.fields.pop('role')
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
