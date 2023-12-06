from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    '''Разрешено только админу остальным только чтение.'''

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or (
                request.user.is_authenticated
                and request.user.is_staff
            )
        )


class IsAuthorOrReadOnly(BasePermission):
    '''Допустимые действия только для автора или пользователя.'''

    def has_permission(self, request, view):
        '''Допустимые типы запросов.'''
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        '''Определяем допустимые действия с объектом.'''
        return (
            request.method in SAFE_METHODS
            or obj.author == request.user
        )
