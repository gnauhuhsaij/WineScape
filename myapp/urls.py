# myapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('process-form/', views.process_form, name='process_form'),
    path('wine_details/<str:wine_name>/<str:customize>', views.wine_details, name='wine_details'),
    path('wine_details/<str:wine_name>/<str:feature_name>/<str:feature_value>/', views.feature_details, name='feature_details'),
    path('features/<str:wine_name>/<str:feature_name>/<str:feature_value>/', views.features, name='features'),
    path('quality/<str:wine_name>', views.quality, name='quality'),
    path('customize/', views.customize, name='customize'),
    path('predict/<str:wine_name>/<str:feature_values>', views.predict, name='predict'),

]
