
from django.urls import path, re_path
from django.contrib.auth import views as auth_views
import users.views as userView

from users.api import UserAPI

app_name = 'users'

urlpatterns = [

    # User API
    path('api/users/', UserAPI.as_view()),




]
