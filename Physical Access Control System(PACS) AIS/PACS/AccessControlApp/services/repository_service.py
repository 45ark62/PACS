import datetime
from datetime import date
from typing import Optional, Iterable, List
from django.db.models import QuerySet
# Импортируем модели DAO
from ..models import Person, AccessLock, Device
from django.core.exceptions import ObjectDoesNotExist


def get_person_by_id(id: int) -> Optional[Person]:
    """Выборка одной записи о персоне по идентификатору"""
    try:
        return Person.objects.get(id=id)
    except ObjectDoesNotExist:
        return None


def get_device_by_id(id: int) -> Optional[Device]:
    """Выборка одной записи об устройстве по идентификатору"""
    try:
        device = Device.objects.get(id=id)
        device.Status = device.get_Status_display()
        return device
    except ObjectDoesNotExist:
        return None


def get_all_persons() -> QuerySet:
    """Выборка всех записей о всех персонах"""
    return Person.objects.all()


def get_all_devices() -> QuerySet:
    """Выборка всех записей о всех устройствах"""
    return Device.objects.all()


def get_all_access_lock_history() -> QuerySet:
    """Выборка всей истории посещений"""
    AccessLockList = AccessLock.objects.all()
    for item in AccessLockList:
        item.AccessLockType = item.get_AccessLockType_display()
        item.DateTime = item.DateTime.strftime("%Y-%m-%d %H:%M:%S")
    return AccessLockList


def get_access_lock_history_by_device(device_id: int) -> QuerySet:
    """Выборка истории посещений по устройству"""
    AccessLockList = AccessLock.objects.filter(ForeignDevice_id=device_id).all()
    for item in AccessLockList:
        item.AccessLockType = item.get_AccessLockType_display()
        item.DateTime = item.DateTime.strftime("%Y-%m-%d %H:%M:%S")
    return AccessLockList


def add_device(device_type: str, description: str, status: str) -> Optional[Device]:
    """Добавление нового устройства"""
    device = Device.objects.create(DeviceType=device_type, Description=description, Status=status)
    device.save()
    return device


def add_person(surname: str, name: str, patronymic: str, job: str, workplace: str,
               phone_number: str, photo: str) -> Optional[Person]:
    """Добавление новой персоны"""
    person = Person.objects.create(Surname=surname, Name=name, Patronymic=patronymic, Job=job, Workplace=workplace,
                                   PhoneNumber=phone_number, Photo=photo)
    person.save()
    return person


def add_access_lock(device_id: int, person_id: int, access_lock_type: str) -> None:
    """Добавление записи об активировании устройства(Access lock)"""
    enter_exit = AccessLock.objects.create(ForeignPerson_id=person_id,
                                           ForeignDevice_id=device_id,
                                           AccessLockType=access_lock_type)
    enter_exit.save()


def update_person_info(person_id: int, job: str, workplace: str, phone_number: str) -> None:
    """Изменение должности, рабочего места, телефона персоны"""
    person = get_person_by_id(person_id)
    person.Job = job
    person.Workplace = workplace
    person.PhoneNumber = phone_number
    person.save()


def update_person_photo(person_id: int, photo: str) -> None:
    """Изменение фото персоны"""
    person = get_person_by_id(person_id)
    person.Photo = photo
    person.save()


def delete_person_by_id(id: int) -> None:
    """Удаление персоны по идентификатору"""
    try:
        get_person_by_id(id).delete()
    except ObjectDoesNotExist:
        return


def delete_device_by_id(id: int) -> None:
    """Удаление устройства по идентификатору"""
    try:
        get_device_by_id(id).delete()
    except ObjectDoesNotExist:
        return


def delete_all_access_lock_history() -> None:
    """Удаление истории посещений"""
    get_all_access_lock_history().delete()


#Новые функции
#----------------------------------------------------------------------------------------------------------------------
def get_access_lock_history_by_interval_by_int(st_year: int, st_month: int, st_day: int, #todo преобразовать в джанговский формат
                                           end_year: int, end_month: int, end_day: int) -> QuerySet:
    """Выборка истории посещения в определенном интервале времени с int в качестве параметров"""
    AccessLockList = AccessLock.objects.filter(DateTime__gte=datetime.datetime(st_year, st_month, st_day,
                                                                    0, 0, 0),
                                     DateTime__lte=datetime.datetime(end_year, end_month, end_day,
                                                                     23, 59, 59)).all()
    for item in AccessLockList:
        item.AccessLockType = item.get_AccessLockType_display()
        item.DateTime = item.DateTime.strftime("%Y-%m-%d %H:%M:%S")
    return AccessLockList


def get_access_lock_history_by_interval_by_date(st_date: date, end_date: date) -> QuerySet:
    """Выборка истории посещения в определенном интервале времени с date в качестве параметров"""
    AccessLockList = AccessLock.objects.filter(DateTime__gte=datetime.datetime(st_date.year, st_date.month, st_date.day,
                                                                     0, 0, 0),
                                               DateTime__lte=datetime.datetime(end_date.year, end_date.month, end_date.day,
                                                                    23, 59, 59)).all()
    for item in AccessLockList:
        item.AccessLockType = item.get_AccessLockType_display()
        #item.DateTime = item.DateTime.strftime("%Y-%m-%d %H:%M:%S")
    return AccessLockList


def delete_access_lock_history_by_interval_by_int(st_year: int, st_month: int, st_day: int,
                                           end_year: int, end_month: int, end_day: int) -> None:
    """Удаление истории посещения в определенном интервале времени с int в качестве параметров"""
    get_access_lock_history_by_interval_by_int(st_year, st_month, st_day, end_year, end_month, end_day).delete()



def delete_access_lock_history_by_interval_by_date(st_date: date, end_date: date) -> None:
    """Удаление истории посещения в определенном интервале времени с date в качестве параметров"""
    get_access_lock_history_by_interval_by_int(st_date.year,
                                               st_date.month,
                                               st_date.day,
                                               end_date.year,
                                               end_date.month,
                                               end_date.day).delete()
