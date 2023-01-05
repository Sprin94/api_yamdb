from django.urls import include, path
from rest_framework.routers import SimpleRouter

from api.views import CommentViewSet, ReviewViewSet
from users.views import TokenObtainView, UserRegistrationView
from .views import UserViewSet, ProfileUserView

router_v1 = SimpleRouter()

router_v1.register('users', UserViewSet)
router_v1.register(r'titles/(?P<title_id>\d+)/reviews',
                   ReviewViewSet, basename='reviews')
router_v1.register(r'titles/(?P<title_id>\d+)/reviews'
                   r'/(?P<review_id>)\d+/comments',
                   CommentViewSet, basename='comments')

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
    path('v1/users/me/', ProfileUserView.as_view()),
    path('v1/', include(router_v1.urls)),
    path('v1/auth/', include(auth_patterns))]