from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from foodgram.pagination import CustomPagination
from users.models import CustomUser, SubscribeModel
from users.serializers import (SetNewPasswordSerializer, SubscribeSerializer,
                               UserCreateSerializer, UserSerializer)


class UserViewSet(viewsets.ModelViewSet):
    '''Отображение пользователей.'''

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
            methods=['post'],
            permission_classes=[IsAuthenticated])
    def subscribe(self, request, pk=None):
        user = request.user
        author = get_object_or_404(CustomUser, id=pk)
        if user == author:
            return Response(
                {'detail': 'Вы не можете подписаться на самого себя.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        # Сохраняем сериализатор с обновленными данными и контекстом.
        serializer = SubscribeSerializer(
            data={'user': user.id, 'author': author.id},
            context={'request': request}
        )

        if serializer.is_valid():
            serializer.save(user=user, author=author)

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    @subscribe.mapping.delete
    def delete_subscribe(self, request, pk=None):
        """Удаляем подписку."""

        user = request.user
        author = get_object_or_404(CustomUser, id=pk)
        if not SubscribeModel.objects.filter(
            user=user,
            author=author
        ).exists():
            return Response(
                {'detail': 'У вас нет такой подписки.'},
                status=status.HTTP_400_BAD_REQUEST
            )
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
            permission_classes=[IsAuthenticated],
            pagination_class=CustomPagination)
    def subscriptions(self, request):
        user = request.user
        queryset = user.subscriber.all().order_by('id')
        page = self.paginate_queryset(queryset)

        # Передаем объект запроса в контексте,
        # чтобы при необходимости получить лимит
        subscribe_serializer = SubscribeSerializer(
            page, many=True, context={'request': request}
        )
        return self.get_paginated_response(subscribe_serializer.data)
