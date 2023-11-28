from django.shortcuts import render, redirect
from rest_framework.generics import (ListAPIView, CreateAPIView, DestroyAPIView, UpdateAPIView, RetrieveAPIView,
                                     GenericAPIView)
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework import status
from datetime import date

from .serializers import *
from .services.AccessControl_service import AccessControlService


service = AccessControlService()


class PersonDetailRest(RetrieveAPIView):
    serializer_class = PersonSerializer
    renderer_classes = [JSONRenderer]

    def get(self, request: Request, person_id: int) -> Response:
        """Выборка одной записи о персоне по идентификатору"""
        response = service.get_person(person_id)
        if response is not None:
            return Response(data=response.data)
        return Response(status=status.HTTP_204_NO_CONTENT)


class DeviceDetailRest(RetrieveAPIView):
    serializer_class = DeviceSerializer
    renderer_classes = [JSONRenderer]

    def get(self, request: Request, device_id: int) -> Response:
        """Выборка одной записи об устройстве по идентификатору"""
        response = service.get_device(device_id)
        if response is not None:
            return Response(data=response.data)
        return Response(status=status.HTTP_204_NO_CONTENT)


class PersonListRest(ListAPIView):
    serializer_class = PersonSerializer
    renderer_classes = [JSONRenderer]

    def get(self, request: Request) -> Response:
        """Выборка всех записей о всех персонах"""
        response = service.get_persons()
        return Response(data=response.data)


class DeviceListRest(ListAPIView):
    serializer_class = DeviceSerializer
    renderer_classes = [JSONRenderer]

    def get(self, request: Request) -> Response:
        """Выборка всех записей о всех устройствах"""
        response = service.get_devices()
        return Response(data=response.data)


class AccessLockListRest(ListAPIView):
    serializer_class = AccessLockSerializer
    renderer_classes = [JSONRenderer]

    def get(self, request: Request) -> Response:
        """Выборка всей истории посещений"""
        response = service.get_access_lock_history()
        return Response(data=response.data)


class AccessLockListByDeviceRest(ListAPIView):
    serializer_class = AccessLockSerializer
    renderer_classes = [JSONRenderer]

    def get(self, request: Request, device_id: int) -> Response:
        """Выборка истории посещений по устройству"""
        response = service.get_access_lock_history_in_device(device_id)
        return Response(data=response.data)


class PersonCreateRest(CreateAPIView):
    serializer_class = PersonSerializer
    renderer_classes = [JSONRenderer]

    def post(self, request: Request, *args, **kwargs) -> Response:
        """Добавление новой персоны"""
        serializer = PersonSerializer(data=request.data)
        if serializer.is_valid():
            service.add_person_info(serializer)
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeviceCreateRest(CreateAPIView):
    serializer_class = DeviceSerializer
    renderer_classes = [JSONRenderer]

    def post(self, request: Request, *args, **kwargs) -> Response:
        """Добавление нового устройства"""
        serializer = DeviceSerializer(data=request.data)
        if serializer.is_valid():
            service.add_device_info(serializer)
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AccessLockCreateRest(CreateAPIView):
    serializer_class = AccessLockSerializer
    renderer_classes = [JSONRenderer]

    def post(self, request: Request, *args, **kwargs) -> Response:
        """Добавление записи об активировании устройства(Access lock)"""
        serializer = AccessLockSerializer(data=request.data)
        if serializer.is_valid():
            service.add_access_lock_info(serializer)
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PersonDeleteRest(DestroyAPIView):
    serializer_class = PersonSerializer
    renderer_classes = [JSONRenderer]

    def delete(self, request: Request, person_id: int) -> Response:
        """Удаление персоны по идентификатору"""
        service.delete_person_info_by_id(person_id)
        return Response(status=status.HTTP_200_OK)


class DeviceDeleteRest(DestroyAPIView):
    serializer_class = DeviceSerializer
    renderer_classes = [JSONRenderer]

    def delete(self, request: Request, device_id: int) -> Response:
        """Удаление устройства по идентификатору"""
        service.delete_device_info_by_id(device_id)
        return Response(status=status.HTTP_200_OK)


class PersonInfoUpdateRest(UpdateAPIView):
    serializer_class = PersonSerializer
    renderer_classes = [JSONRenderer]

    def patch(self, request: Request, person_id: int,  *args, **kwargs) -> Response:
        """Обновить информацию о персоне по идентификатору"""
        serializer = PersonSerializer(data=request.data)
        if serializer.is_valid():
            service.update_person(serializer, person_id)
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class PersonPhotoUpdateRest(UpdateAPIView):
    serializer_class = PersonSerializer
    renderer_classes = [JSONRenderer]

    def patch(self, request: Request, person_id: int, *args, **kwargs) -> Response:
        """Обновить фотографию персоны по идентификатору"""
        serializer = PersonSerializer(data=request.data)
        if serializer.is_valid():
            service.update_person_photo_info(serializer, person_id)
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

#новые классы
#------------------------------------------------------------------------------------------------------------------
class GetDelPerson(GenericAPIView):
    serializer_class = PersonSerializer
    renderer_classes = [JSONRenderer]

    def get(self, request: Request, person_id: int) -> Response:
        """Выборка одной записи о персоне по идентификатору"""
        response = service.get_person(person_id)
        if response is not None:
            return Response(data=response.data)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def delete(self, request: Request, person_id: int) -> Response:
        """Удаление персоны по идентификатору"""
        service.delete_person_info_by_id(person_id)
        return Response(status=status.HTTP_200_OK)


class GetDelDevice(GenericAPIView):
    serializer_class = DeviceSerializer
    renderer_classes = [JSONRenderer]

    def get(self, request: Request, device_id: int) -> Response:
        """Выборка одной записи об устройстве по идентификатору"""
        response = service.get_device(device_id)
        if response is not None:
            return Response(data=response.data)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def delete(self, request: Request, device_id: int) -> Response:
        """Удаление устройства по идентификатору"""
        service.delete_device_info_by_id(device_id)
        return Response(status=status.HTTP_200_OK)


class GetPostAccessLock(GenericAPIView):
    serializer_class = AccessLockSerializer
    renderer_classes = [JSONRenderer]

    def get(self, request: Request) -> Response:
        """Выборка всей истории посещений"""
        response = service.get_access_lock_history()
        return Response(data=response.data)

    def post(self, request: Request) -> Response:
        """Добавление записи об проходе через устройство(Access lock)"""
        serializer = AccessLockSerializer(data=request.data)
        if serializer.is_valid():
            service.add_access_lock_info(serializer)
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetDelHistoryIntervalByInt(GenericAPIView):
    serializer_class = DateRangeByIntSerializer
    renderer_classes = [JSONRenderer]

    def get(self, request: Request) -> Response:
        """Выборка истории посещения в определенном интервале времени с int в качестве параметров"""
        serializer = DateRangeByIntSerializer(data=request.data)
        if serializer.is_valid():
            response = service.get_access_lock_history_in_interval_by_int(serializer)
            return Response(data=response.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request) -> Response:
        """Удаление истории посещения в определенном интервале времени с int в качестве параметров"""
        serializer = DateRangeByIntSerializer(data=request.data)
        if serializer.is_valid():
            service.delete_access_lock_history_in_interval_by_int(serializer)
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetDelHistoryIntervalByDate(GenericAPIView):
    serializer_class = DateRangeByDateSerializer
    renderer_classes = [JSONRenderer]

    def get(self, request: Request, st_date: str, end_date: str) -> Response:
        """Выборка истории посещения в определенном интервале времени с date в качестве параметров"""
        response = service.get_access_lock_history_in_interval_by_date(st_date, end_date)
        return Response(data=response.data)

    def delete(self, request: Request, st_date: str, end_date: str) -> Response:
        """Удаление истории посещения в определенном интервале времени с date в качестве параметров"""
        serializer = DateRangeByDateSerializer(data=request.data)
        if serializer.is_valid():
            service.delete_access_lock_history_in_interval_by_date(st_date, end_date)
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

