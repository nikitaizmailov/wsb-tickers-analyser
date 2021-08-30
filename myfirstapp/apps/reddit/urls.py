from django.urls import path

from . import views

# so that when you provide {url 'name of template'} it 
app_name = 'reddit'

urlpatterns = [
    path('analytics/', views.chart, name='chart'),

    path('', views.index, name = 'index'),
    path('<int:article_id>/', views.detail, name='detail'),
    path('<int:article_id>/leave_comment', views.leave_comment, name='leave_comment')
]