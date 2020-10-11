from django.urls import path
from knox import views as knox_views

from .views import signup, Login, Update_Delete_User
urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),

    path('update/<int:pk>/', Update_Delete_User.as_view(), name='update_user'),
]
