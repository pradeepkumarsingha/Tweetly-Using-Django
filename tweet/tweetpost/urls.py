from . import views
from django.urls import path

urlpatterns = [
   path('',views.index,name='index'),
   path('register/',views.register_view,name='register'),
   path('login/',views.login_view,name='login'),
   path('logout/',views.logout_view,name='logout'),
   path('tweets/',views.tweet_list,name='tweet_list'),
   path('tweets/create/',views.tweet_create,name='tweet_create'),
   path('tweets/  <int:tweet_id>/update/',views.tweet_update,name='tweet_update'),
   path('tweets/<int:tweet_id>/delete/',views.tweet_delete,name='tweet_delete'),
   path('tweets/<int:tweet_id>/like/',views.toggle_like,name='toggle_like'),
   path('tweets/<int:tweet_id>/comment/',views.add_comment,name='add_comment')
]