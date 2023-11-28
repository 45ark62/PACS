from django.test import TestCase
import random
from .services.repository_service import *
from .services.AccessControl_service import *


class TestWeatherRepositoryService(TestCase):


    def setUp(self):
        """Добавление устройства, персоны и события AccessLock"""
        device = add_device('Turniket', 'bla', '1')
        person = add_person('Ivanov', 'Ivan', 'Ivanovich', 'Student', 'blablabla',
                            '89274556433', '/path/')
        add_access_lock(device.pk, person.pk, '1')


    def test_get_person(self):
        """Выборка только что созданной записи персоны и проверка на корректность данных"""
        person = get_person_by_id(1)
        self.assertEqual(person.Surname, 'Ivanov')
        self.assertEqual(person.Name, 'Ivan')
        self.assertEqual(person.Patronymic, 'Ivanovich')
        self.assertEqual(person.Job, 'Student')
        self.assertEqual(person.Workplace, 'blablabla')
        self.assertEqual(person.PhoneNumber, '89274556433')


    def test_get_device(self):
        """Выборка только что созданной записи устройства и проверка на корректность данных"""
        device = get_device_by_id(1)
        self.assertEqual(device.DeviceType, 'Turniket')
        self.assertEqual(device.Status, 'Работает')


    def test_get_access_lock(self):
        """Выборка только что созданног особытия AccessLock и проверка на корректность данных"""
        person = get_person_by_id(1)
        device = get_device_by_id(1)
        res = get_all_access_lock_history()
        self.assertEqual(res.first().ForeignPerson, person)
        self.assertEqual(res.first().ForeignDevice, device)


    def test_update_person_info(self):
        """Внесение изменений в персону, выборка и проверка на корректность данных"""
        update_person_info(1, 'Professor', 'INEK', '89274556433')
        person = get_person_by_id(1)
        self.assertEqual(person.Job, 'Professor')
        self.assertEqual(person.Workplace, 'INEK')
        self.assertEqual(person.PhoneNumber, '89274556433')


    def test_get_all_devices(self):
        """Создание нового устройства, возвращение в result списка из двух устройтсв, проверка создались ли устройства и корректны ли данные"""
        device = get_device_by_id(1)
        device2 = add_device('Zamok', 'bla2', '1')
        result = get_all_devices()
        self.assertEqual(result.first().Description, 'bla')
        self.assertEqual(result.last().Description, 'bla2')


    def test_delete_person_by_id(self):
        """Удаление персоны и проверка, в result должно возвратиться None"""
        delete_person_by_id(1)
        result = get_person_by_id(1)
        self.assertIsNone(result)


    def test_delete_device_by_id(self):
        """Удаление устройства и проверка, в result должно возвратиться None"""
        delete_device_by_id(1)
        result = get_device_by_id(1)
        self.assertIsNone(result)


    def test_get_access_lock_history_by_interval(self):
        """Выборка истории посещения за определенное время"""   #todo спросить как убрать предупреждения
        device = get_device_by_id(1)
        person = get_person_by_id(1)
        add_access_lock(device.pk, person.pk, '1')
        add_access_lock(device.pk, person.pk, '1')
        add_access_lock(device.pk, person.pk, '1')
        self.assertEqual(get_access_lock_history_by_interval_by_int(2005, 2, 23,
                                                             2020, 2, 23).count(), 0)
        self.assertEqual(get_access_lock_history_by_interval_by_int(2005, 2, 23,
                                                             2024, 11, 12).count(), 4)
        self.assertEqual(get_all_access_lock_history().count(), 4)


    def test_delete_access_lock_history_by_interval(self):
        """Удаление истории посещения за определенное время"""  #todo спросить как убрать предупреждения
        delete_access_lock_history_by_interval_by_int(2005, 2, 23,
                                               2020, 2, 23)
        self.assertEqual(get_all_access_lock_history().count(), 1)
        delete_access_lock_history_by_interval_by_int(2005, 2, 23,
                                               2024, 11, 12)
        self.assertEqual(get_all_access_lock_history().count(), 0)


    def get_access_lock_history_by_device_service(self): #Нерабочий
        """Тестирование Service layer"""
        device = get_device_by_id(1)
        obj = AccessControlService
        result = AccessControlService.get_access_lock_history_in_device(device.pk)
        self.assertEqual(result, get_access_lock_history_by_device(1))


    def tearDown(self):
        pass
