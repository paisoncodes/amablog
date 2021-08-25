from django.urls import path
from . import views

app_name = 'blog'


urlpatterns = [
    path('<slug>/delete/', views.delete_post_view, name='delete'),
    path('create/', views.create_post_view, name='create'),
    path('<slug>/', views.post_detail_view, name='detail'),
    path('<slug>/edit/', views.edit_post_view, name='edit'),
    path('user/posts/', views.view_posts, name='posts')
]