from django.urls import path
from userauthentication import views

app_name = "userauthentication"

urlpatterns = [
    path('register_page/',views.register_view,name="register_page"),
    path('login/',views.login_view,name="login"),
    path('sign-out/',views.logout_view,name="sign-out"),

    path('profile/update/',views.profile_update,name="profile-update"),
]