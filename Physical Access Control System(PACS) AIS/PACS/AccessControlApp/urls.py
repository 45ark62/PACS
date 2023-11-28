from django.urls import path, re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

from . import views

"""
    Подключение URI для приложения weatherapp.
    Корневые URI представлены в базовом модуле application/urls.py
"""

#Метаданные Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="PACS API",
        default_version='v1',
        description="PACS API",
        terms_of_service="https://example.com",
        contact=openapi.Contact(email="contact@mail.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny]
)


urlpatterns = [
    path('person/<int:person_id>', views.GetDelPerson.as_view()), #Получить, удалить персону
    path('person', views.PersonCreateRest.as_view()),#Создать персону
    path('person/<int:person_id>/update_info', views.PersonInfoUpdateRest.as_view()), #Обновить информацию о персоне
    path('person/<int:person_id>/update_photo', views.PersonPhotoUpdateRest.as_view()), #Обновить фото персоны
    path('person/list', views.PersonListRest.as_view()), #Получить список всех персон
    path('device/<int:device_id>', views.GetDelDevice.as_view()), #Получить, удалить устройство
    path('device/list', views.DeviceListRest.as_view()), #Получить список всех устройств
    path('device', views.DeviceCreateRest.as_view()), #Создать устройство
    path('history', views.GetPostAccessLock.as_view()), #Получить всю историю посещений, добавить одну запись
    path('history/<int:device_id>', views.AccessLockListByDeviceRest.as_view()), #Получить историю посещений одного устройства
    path('history/interval_by_int', views.GetDelHistoryIntervalByInt.as_view()),
    path('history/interval_by_date/<slug:st_date>/<slug:end_date>', views.GetDelHistoryIntervalByDate.as_view()),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui')
]
