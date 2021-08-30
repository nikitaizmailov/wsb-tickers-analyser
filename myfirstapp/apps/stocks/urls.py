from django.urls import path

from . import views

# adding namespace and also specifying it in the templates so that
# the template brings up the correct url path.
app_name = 'stocks'

urlpatterns = [
    
    # ex: /stocks/
    path('', views.index, name='index'),

    # ex: /stocks/5
    path('<int:question_id>/', views.detail, name='detail'),

    # ex: /stocks/5/results
    path('<int:question_id>/results/', views.results, name='results'),

    # ex: /stocks/5/vote
    path('<int:question_id>/vote/', views.vote, name='vote'),
]