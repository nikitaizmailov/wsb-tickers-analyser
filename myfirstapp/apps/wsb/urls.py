from . import views
from django.urls import path

# adding namespace and also specifying it in the templates so that
# the template brings up the correct url path.
app_name = 'wsb'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('create_q/', views.create_q, name='create_q'),
    path('<int:subreddit_id>/', views.detail, name='detail'),
    path('<int:subreddit_id>/leave_comment', views.leave_comment, name='leave_comment'),
    path('results/', views.results, name='results'),
    path('about_me/', views.about_me, name='about_me'),
]