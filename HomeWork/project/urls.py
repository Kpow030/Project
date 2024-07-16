from django.urls import path
from .views import PostList, PostDetail, PostCreate, PostUpdate, PostDelete, UserResponseView, UserResponseList

urlpatterns = [
    path('', PostList.as_view(), name='posts'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('<int:pk>/edit/', PostUpdate.as_view(), name='post_edit'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('responses/', UserResponseList.as_view(), name='userresponses'),
    path('<int:pk>/response/', UserResponseView.as_view(), name='userresponse'),
]