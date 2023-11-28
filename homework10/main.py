from collections import UserDict


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    
    def __init__(self, value):
        self.value = value


class Phone(Field):

    def __init__(self, value):
        if value.isnumeric() and len(value) == 10:
            self.value = value
        else:
            raise ValueError


class Record:

    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, value):
        phone = Phone(value)
        self.phones.append(phone)

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
