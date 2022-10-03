from django.urls import re_path, path
from apps.kinopark import views
from .views import RegisterView, LoginView, UserView, LogoutView

app_name = 'kinopark'

urlpatterns = [
    re_path(r'api/kinopark/films$', views.movies_list),
    re_path(r'api/kinopark/film/(?P<pk>[0-9]+)', views.movie_by_id),
    re_path(r'api/kinopark/films/unpublished', views.unpublished_movies),
    path('api/register', RegisterView.as_view()),
    path('api/login', LoginView.as_view()),
    path('api/user', UserView.as_view()),
    path('api/logout', LogoutView.as_view()),
    path('api/get_login', views.get_login),
    re_path(r'api/order/(?P<pk>[0-9]+)', views.order),
    re_path(r'api/order', views.create_order)
]