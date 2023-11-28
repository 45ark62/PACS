from rest_framework import serializers
from .models import *


class Hist:
    def __init__(self, pk, ForeignPerson, FIO, ForeignDevice, AccessLockType, DateTime):
        self.id = pk
        self.ForeignPerson = ForeignPerson
        self.FIO = FIO
        self.ForeignDevice = ForeignDevice
        self.AccessLockType = AccessLockType
        self.DateTime = DateTime


class Dev:
    def __init__(self, id, DeviceType, Description, Status, Capacity):
        self.id = id
        self.DeviceType = DeviceType
        self.Description = Description
        self.Status = Status
        self.Capacity = Capacity


class Pers:
    def __init__ (self, id, Surname, Name, Patronymic, Job, Workplace, PhoneNumber, WorkTime, ArrivalTime):
        self.id = id
        self.Surname = Surname
        self.Name = Name
        self.Patronymic = Patronymic
        self.Job = Job
        self.Workplace = Workplace
        self.PhoneNumber = PhoneNumber
        self.WorkTime = WorkTime
        self.ArrivalTime = ArrivalTime

class PersonSerializer(serializers.ModelSerializer):
    WorkTime = serializers.TimeField(required=False)
    ArrivalTime = serializers.CharField(max_length=8, required=False)

    class Meta:
        model = Person
        fields = ('id', 'Surname', 'Name', 'Patronymic', 'Job', 'Workplace', 'PhoneNumber', 'WorkTime', 'ArrivalTime')


class DeviceSerializer(serializers.ModelSerializer):
    Capacity = serializers.FloatField(required=False)

    class Meta:
        model = Device
        fields = ('id', 'DeviceType', 'Description', 'Status', 'Capacity')


class AccessLockSerializer(serializers.ModelSerializer):
    ForeignPerson = serializers.IntegerField()
    FIO = serializers.CharField(max_length=255, required=False)
    ForeignDevice = serializers.IntegerField()
    #AccessLockType = serializers.CharField(max_length=10)
    DateTime = serializers.DateTimeField(required=False)

    class Meta:
        model = AccessLock
        fields = ('id', 'ForeignPerson', 'FIO', 'ForeignDevice', 'AccessLockType', 'DateTime')


class DateRangeByIntSerializer(serializers.Serializer):
    st_year = serializers.IntegerField(min_value=1000, max_value=3000)
    st_month = serializers.IntegerField(min_value=0, max_value=12)
    st_day = serializers.IntegerField(min_value=1, max_value=31)
    end_year = serializers.IntegerField(min_value=1000, max_value=3000)
    end_month = serializers.IntegerField(min_value=1, max_value=12)
    end_day = serializers.IntegerField(min_value=1, max_value=31)


class DateRangeByDateSerializer(serializers.Serializer):
    st_date = serializers.DateField
    end_date = serializers.DateField



