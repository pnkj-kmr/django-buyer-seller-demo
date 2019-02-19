from django.urls import path
from .views import *


urlpatterns = [
    path('', home, name='home'),
    path('add_post/', new_post_add, name='post_add'),
    path('all/', all_posts, name='all_posts'),

]