"""mdrs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from utility_matrix.urls import urlpatterns as utility_matrix_urls
from aggregations.urls import urlpatterns as aggregations_urls
from dempster_shafer_structure.urls import urlpatterns as ds_url_patterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('dempster-shafer/', include(ds_url_patterns)),
    path('utility-matrix/', include(utility_matrix_urls)),
    path('aggregations/', include(aggregations_urls)),
]
