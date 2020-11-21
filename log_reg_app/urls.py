from django.urls import path
from . import views

urlpatterns=[
    path('', views.index),
    path('create_user', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('success', views.success),
    path('create_message', views.create_mess),
    path('user/<int:user_id>', views.profile),
    path('create_comment', views.create_comm),
    path('delete/<int:message_id>', views.delete_mess),
    path('comm_delete/<int:comm_id>', views.delete_comm),
    path('like/<int:message_id>', views.like_post)
]