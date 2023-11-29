from collections import UserDict
from datetime import datetime, date


class Field:
    
    def init(self, value):
        self.__value = None
        self.value = value
 
    @property
    def value(self):
        return self.__value
 
    @value.setter
    def value(self, value):
        self.__value = value

    def __str__(self):
        return str(self.__value)


class Name(Field):
    
    def __init__(self, value):
        self.value = value


class Phone(Field):

    def __init__(self, value):
        self.__value = value
        self.value = value

    @Field.value.setter
    def value(self, value):
        if value.isnumeric() and len(value) == 10:
            self.__value = value
        else:
            raise ValueError

    @value.getter
    def value(self):
        return self.__value


class Birthday(Field):

    def __init__(self, value):
        self.__value = value
        self.value = value

    @Field.value.setter
    def value(self, value):
        try:
            self.__value = datetime.strptime(value, '%Y.%m.%d').date()
        except:
            raise ValueError

    @value.getter
    def value(self):
        return self.__value


class Record:

    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, value):
        phone = Phone(value)
        self.phones.append(phone)

    def add_birthday(self, value):
        self.birthday = Birthday(value)

    def remove_phone(self, value):
        for phone in self.phones:
            if value == phone.value:
                self.phones.remove(phone)
                return

    def edit_phone(self, value_now, value_new):
        for phone in self.phones:
            if value_now == phone.value:
                phone.value = value_new
                return
        raise ValueError

    def find_phone(self, value):
        for phone in self.phones:
            if value == phone.value:
                return phone
            
    def days_to_birthday(self):
        if self.birthday:
            current_date = date.today()
            year_now = current_date.year
            birthday = self.birthday.replace(year = year_now)
            # Calculate
            if birthday > current_date:
                return (birthday - current_date).days
            elif birthday == current_date:
                return "0"
            elif birthday < current_date:
                birthday = birthday.replace(year = year_now+1)
                return (birthday - current_date).days

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):

    def add_record(self, user_record):
        self.data.update({user_record.name.value: user_record})

    def find(self, value):
        if value in self.data:
            return self.data[value]

    def delete(self, value):
        if value in self.data:
            self.data.pop(value)

    def iterator(self, item_number):
        counter = 0
        result = ''
        for item, record in self.data.items():
            result += f'{item}: {record}\n'
            counter += 1
            if counter >= item_number:
                yield result[:-1]
                counter = 0
                result = ''
                break


def main():

    # Створення нової адресної книги
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")
    john_record.add_birthday('2000.10.01')
    john_record.edit_phone("5555555555", "1111111111")
    book.add_record(john_record)

    jane_record = Record("Jane")
    jane_record.add_phone("0000000000")
    jane_record.add_phone("9999999999")
    # jane_record.add_birthday('1980.10.01')
    book.add_record(jane_record)

    yan_record = Record("Yan")
    yan_record.add_phone("2222222222")
    yan_record.add_phone("8888888888")
    yan_record.add_birthday('1990.10.01')
    book.add_record(yan_record)

    for value in book.iterator(2):
        print(value)

    # Додавання запису John до адресної книги
    # book.add_record(john_record)

    # # Створення та додавання нового запису для Jane
    # jane_record = Record("Jane")
    # jane_record.add_phone("9876543210")
    # book.add_record(jane_record)

    # Виведення всіх записів у книзі
    # for name, record in book.data.items():
    #     print(record)

    # # Знаходження та редагування телефону для John
    # john = book.find("John")
    # john.edit_phone("1234567890", "1112223333")

    # print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

    # # Пошук конкретного телефону у записі John
    # found_phone = john.find_phone("5555555555")
    # print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

    # # Видалення запису Jane
    # book.delete("Jane")


if __name__ == "__main__":
    main()
