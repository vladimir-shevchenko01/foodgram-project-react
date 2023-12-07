from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from foodgram.pagination import CustomPagination
from users.models import CustomUser, SubscribeModel
from users.serializers import (
    SubscribeSerializer,
    SubscriptionsSerializer,
    UserSerializer,
    UserCreateSerializer,
    SetNewPasswordSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    '''_______________________________'''

    queryset = CustomUser.objects.all()
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return UserSerializer
        return UserCreateSerializer

    @action(detail=False,
            methods=['get'],
            permission_classes=(IsAuthenticated,))
    def me(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data,
                        status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'],
            permission_classes=(IsAuthenticated,))
    def set_password(self, request):
        serializer = SetNewPasswordSerializer(request.user, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(
            {'detail': 'Вы успешно сменили пароль.'},
            status=status.HTTP_204_NO_CONTENT
        )

    @action(detail=True,
            methods=['post', 'delete'],
            permission_classes=[IsAuthenticated])
    def subscribe(self, request, pk=None):
        user = request.user
        author = get_object_or_404(CustomUser, id=pk)

        if request.method == 'POST':
            # Проверяем, существует ли уже подписка от пользователя на автора.
            # Если подписка не существует, создаем новую запись.
            if SubscribeModel.objects.filter(user=user, author=author).exists():
                return Response(
                    {"message": "Вы уже подписаны на этого автора"},
                    status=status.HTTP_200_OK,
                )
            # Сохраняем сериализатор с обновленными данными.
            serializer = SubscribeSerializer(
                data={'user': user.id, 'author': author.id}
            )
            if serializer.is_valid():
                serializer.save()
                author_serializer = UserSerializer(
                    author,
                    context={'request': request},
                )
                return Response(
                    author_serializer.data,
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )

        if request.method == 'DELETE':
            subscription = get_object_or_404(
                SubscribeModel,
                user=user,
                author=author
            )
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False,
            methods=['get'],
            url_path='subscriptions',
            permission_classes=[IsAuthenticated])
    def subscriptions(self, request):
        user = request.user
        queryset = SubscribeModel.objects.filter(user=user).order_by('id')

        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(queryset, request)

        subscribe_serializer = SubscriptionsSerializer(result_page, many=True)
        return paginator.get_paginated_response(subscribe_serializer.data)
