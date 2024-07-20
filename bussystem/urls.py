"""
URL configuration for bussystem project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include, re_path

from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.documentation import include_docs_urls

schema_view = get_schema_view(
    openapi.Info(
        title="Bus System API",
        default_version='v1',
        description="Bus system APIs description",
    ),
    validators=['ssv', 'flex'],
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),

    path('api/v1/account/', include('apps.account.urls', namespace='account')),
    path('api/v1/bus/', include('apps.bus.urls', namespace='bus')),


    path('api-doc/', include_docs_urls(title='File Maker Documentation')),
    path('', schema_view.with_ui('swagger', cache_timeout=0),name='schema-swagger-ui'),
    path('api-auth/', include(('rest_framework.urls','rest_framework'), namespace='rest_framework')),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',schema_view.without_ui(cache_timeout=0), name='schema-json'),

]
