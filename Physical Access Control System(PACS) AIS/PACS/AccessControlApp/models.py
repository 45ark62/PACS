import datetime
from django.db import models


class Person(models.Model):
    Surname = models.CharField(max_length=80, verbose_name="Фамилия")
    Name = models.CharField(max_length=80, verbose_name="Имя")
    Patronymic = models.CharField(max_length=80, verbose_name="Отчество")
    Job = models.CharField(max_length=80, verbose_name="Должность")
    Workplace = models.CharField(max_length=150, verbose_name="Рабочее место")
    PhoneNumber = models.CharField(max_length=11, verbose_name="Номер телефона")
    Photo = models.CharField(max_length=200, verbose_name="Фото")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['Name', 'Surname', 'Patronymic'], name='unique person fio')
        ]
        db_table = "Person"
        ordering = ["Surname", "Name", "Patronymic"]




class Device(models.Model):
    DeviceType = models.CharField(max_length=80, default='Турникет', verbose_name="Тип устройства")
    Description = models.TextField(null=False, blank=True)
    STATES = (
        ('1', 'Работает'),
        ('0', 'Не работает'),
    )
    Status = models.CharField(max_length=1, choices=STATES, default='1', verbose_name="Состояние")

    class Meta:
        db_table = "Device"


class AccessLock(models.Model):
    ForeignPerson = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='visits')
    ForeignDevice = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='passes')
    TYPES = (
        ('1', 'Вход'),
        ('0', 'Выход'),
    )
    AccessLockType = models.CharField(max_length=1, choices=TYPES)
    DateTime = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="Дата и время")

    class Meta:
        ordering = ['-DateTime']
        db_table = "AccessLock"

    def __str__(self):
        return str(self.DateTime)
