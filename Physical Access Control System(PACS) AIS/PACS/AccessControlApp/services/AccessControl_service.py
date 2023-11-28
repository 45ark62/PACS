from ..serializers import *
from .repository_service import *
from datetime import date, datetime, time, timedelta


class AccessControlService:

    def get_person(self, person_id: int) -> Optional[PersonSerializer]:
        person = get_person_by_id(person_id)
        if person is not None:
            day_history = get_access_lock_history_by_interval_by_date(date.today(), date.today()).order_by('DateTime')
            at_work_now = False
            time_delta = timedelta(hours=0, minutes=0, seconds=0)
            st_time = time(hour=0, minute=0, second=0)
            end_time = time(hour=0, minute=0, second=0)
            arrival_time = time(hour=0, minute=0, second=0)
            did_come = False
            for i in day_history:
                if i.ForeignPerson.pk == person.pk:
                    if i.AccessLockType == '1':
                        if did_come:
                            at_work_now = True
                            st_time = i.DateTime.time()
                        else:
                            at_work_now = True
                            did_come = True
                            st_time = i.DateTime.time()
                            arrival_time = st_time
                    else:
                        at_work_now = False
                        end_time = i.DateTime.time()
                        time_delta += timedelta(hours=end_time.hour-st_time.hour,
                                                minutes=end_time.minute-st_time.minute,
                                                seconds=end_time.second-st_time.second)
                        print(time_delta)

            if at_work_now:
                end_time = datetime.now().time()
                time_delta += timedelta(hours=end_time.hour-st_time.hour,
                                        minutes=end_time.minute-st_time.minute,
                                        seconds=end_time.second-st_time.second)
            if time_delta != timedelta(hours=0, minutes=0, seconds=0):
                result = Pers(person_id,
                              person.Surname,
                              person.Name,
                              person.Patronymic,
                              person.Job,
                              person.Workplace,
                              person.PhoneNumber,
                              str(time_delta),
                              arrival_time.strftime('%H:%M:%S')
                              )
                return PersonSerializer(result)
            else:
                result = Pers(person_id,
                              person.Surname,
                              person.Name,
                              person.Patronymic,
                              person.Job,
                              person.Workplace,
                              person.PhoneNumber,
                              str(time_delta),
                              '-')
                return PersonSerializer(result)
        return None

    def get_device(self, device_id: int) -> Optional[DeviceSerializer]:
        device = get_device_by_id(device_id)
        if device is not None:
            day_history = get_access_lock_history_by_interval_by_date(date.today(), date.today())
            device_day_history = 0
            for i in day_history:
                if i.ForeignDevice.pk == device_id:
                    device_day_history = device_day_history + 1
            Capacity = device_day_history / 24

            result = Dev(device.pk,
                         device.DeviceType,
                         device.Description,
                         device.Status,
                         Capacity)
            return DeviceSerializer(result)
        return device

    def get_devices(self) -> DeviceSerializer:
        devices = get_all_devices()
        result = []
        day_history = get_access_lock_history_by_interval_by_date(date.today(), date.today())
        for device in devices:
            device_day_history = 0
            for j in day_history:
                if j.ForeignDevice.pk == device.pk:
                    device_day_history = device_day_history + 1
            Capacity = device_day_history / 24
            result.append(Dev(device.pk,
                              device.DeviceType,
                              device.Description,
                              device.Status,
                              Capacity))
        devices_data = DeviceSerializer(result, many=True)
        return devices_data

    def get_persons(self) -> PersonSerializer:
        persons = get_all_persons()
        person_list = []
        for person in persons:
            person_list.append(self.get_person(person.pk).data)
        return PersonSerializer(person_list, many=True)

    def get_access_lock_history(self) -> AccessLockSerializer:
        history = get_all_access_lock_history()
        if history.count() != 0:
            access_lock_data = []
            for i in range(0, history.count()):
                person = get_person_by_id(history[i].ForeignPerson.pk)
                access_lock_data.append(Hist(history[i].pk,
                                        history[i].ForeignPerson.pk,
                                        person.Surname + ' ' + person.Name + ' ' + person.Patronymic,
                                        history[i].ForeignDevice.pk,
                                        history[i].AccessLockType,
                                        history[i].DateTime))
            result = AccessLockSerializer(access_lock_data, many=True)
            return result
        result = AccessLockSerializer(history, many=True)
        return result

    def get_access_lock_history_in_device(self, device_id: int) -> AccessLockSerializer:
        history = get_access_lock_history_by_device(device_id)
        if history.count() != 0:
            access_lock_data = []
            for i in range(0, history.count()):
                person = get_person_by_id(history[i].ForeignPerson.pk)
                access_lock_data.append(Hist(history[i].pk,
                                             history[i].ForeignPerson.pk,
                                             person.Surname + ' ' + person.Name + ' ' + person.Patronymic,
                                             history[i].ForeignDevice.pk,
                                             history[i].AccessLockType,
                                             history[i].DateTime))
            result = AccessLockSerializer(access_lock_data, many=True)
            return result
        result = AccessLockSerializer(history, many=True)
        return result

    def get_access_lock_history_in_interval_by_int(self, date: DateRangeByIntSerializer) -> AccessLockSerializer:
        date_data = date.data
        history = get_access_lock_history_by_interval_by_int(st_year=date_data.get('st_year'),
                                                     st_month=date_data.get('st_month'),
                                                     st_day=date_data.get('st_day'),
                                                     end_year=date_data.get('end_year'),
                                                     end_month=date_data.get('end_month'),
                                                     end_day=date_data.get('end_day'))
        if history.count() != 0:
            access_lock_data = []
            for i in range(0, history.count()):
                person = get_person_by_id(history[i].ForeignPerson.pk)
                access_lock_data.append(Hist(history[i].pk,
                                             history[i].ForeignPerson.pk,
                                             person.Surname + ' ' + person.Name + ' ' + person.Patronymic,
                                             history[i].ForeignDevice.pk,
                                             history[i].AccessLockType,
                                             history[i].DateTime))
            result = AccessLockSerializer(access_lock_data, many=True)
            return result
        result = AccessLockSerializer(history, many=True)
        return result

    def get_access_lock_history_in_interval_by_date(self, st_date: str, end_date: str) -> AccessLockSerializer:
        st_date = datetime.strptime(st_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        history = get_access_lock_history_by_interval_by_date(st_date=st_date,
                                                              end_date=end_date)
        if history.count() != 0:
            access_lock_data = []
            for i in range(0, history.count()):
                person = get_person_by_id(history[i].ForeignPerson.pk)
                access_lock_data.append(Hist(history[i].pk,
                                             history[i].ForeignPerson.pk,
                                             person.Surname + ' ' + person.Name + ' ' + person.Patronymic,
                                             history[i].ForeignDevice.pk,
                                             history[i].AccessLockType,
                                             history[i].DateTime.strftime("%Y-%m-%d %H:%M:%S")))
            result = AccessLockSerializer(access_lock_data, many=True)
            return result
        result = AccessLockSerializer(history, many=True)
        return result

    def add_person_info(self, person: PersonSerializer):
        person_data = person.data
        add_person(surname=person_data.get('Surname'),
                   name=person_data.get('Name'),
                   patronymic=person_data.get('Patronymic'),
                   job=person_data.get('Job'),
                   workplace=person_data.get('Workplace'),
                   phone_number=person_data.get('PhoneNumber'),
                   photo='path'
                   )

    def add_device_info(self, device: DeviceSerializer):
        device_data = device.data
        add_device(device_type=device_data.get('DeviceType'),
                   description=device_data.get('Description'),
                   status=device_data.get('Status')
                   )

    def add_access_lock_info(self, access_lock: AccessLockSerializer):
        access_lock_data = access_lock.data
        add_access_lock(device_id=access_lock_data.get('ForeignDevice'),
                        person_id=access_lock_data.get('ForeignPerson'),
                        access_lock_type=access_lock_data.get('AccessLockType')
                        )

    def update_person(self, person: PersonSerializer, person_id: int):
        person_data = person.data
        update_person_info(person_id=person_id,
                           job=person_data.get('Job'),
                           workplace=person_data.get('Workplace'),
                           phone_number=person_data.get('PhoneNumber')
                           )

    def update_person_photo_info(self, person: PersonSerializer, person_id: int):
        person_data = person.data
        update_person_photo(person_id=person_id,
                            photo=person_data.get('Photo')
                            )

    def delete_person_info_by_id(self, person_id: int):
        delete_person_by_id(person_id)

    def delete_device_info_by_id(self, device_id: int):
        delete_device_by_id(device_id)

    def delete_access_lock_history_in_interval_by_int(self, date: DateRangeByIntSerializer):
        date_data = date.data
        delete_access_lock_history_by_interval_by_int(date_data.get('st_year'),
                                                      date_data.get('st_month'),
                                                      date_data.get('st_day'),
                                                      date_data.get('end_year'),
                                                      date_data.get('end_month'),
                                                      date_data.get('end_day'))

    def delete_access_lock_history_in_interval_by_date(self, st_date: str, end_date: str):
        st_date = datetime.strptime(st_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        result = get_access_lock_history_by_interval_by_date(st_date=st_date,
                                                             end_date=end_date)
