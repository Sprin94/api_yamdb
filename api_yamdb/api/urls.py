from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import CategoryViewSet, GenreViewSet, TitleViewSet


from users.views import TokenObtainView, UserRegistrationView
router_v1 = SimpleRouter()

router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register('genres', GenreViewSet, basename='genres')
router_v1.register('titles', TitleViewSet, basename='titles')

auth_patterns = [
    path(
        'token/',
        TokenObtainView.as_view(),
        name='token_obtain_pair'
    ),
    path(
        'signup/',
        UserRegistrationView.as_view(),
        name='signup'
    ),
]

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/', include(auth_patterns))
]
