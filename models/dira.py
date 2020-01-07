
# id	street	city	rooms	floor	size	price
class Dira():
    def __init__(self, id, street, city, rooms, floor, size, price, condition, source, sent=0, row=None):
        self.__id = id
        self.__street = street
        self.__city = city
        self.__rooms = rooms
        self.__floor = floor
        self.__size = size
        self.__price = price
        self.__condition = condition
        self.__source = source
        self.__sent = sent
        self.__row = row

    def to_sheet(self):
        return [self.__id, self.__street, self.__city, self.__rooms, self.__floor, self.__size, self.__price, self.__condition, self.__source]

    @staticmethod
    def from_sheet(*args):
        return Dira(*args)

    @property
    def id(self):
        return self.__id

    @property
    def subject(self):
        return "{street} {city} - קומה {floor} - {price}".format(street=self.__street, city=self.__city, floor=self.__floor, price=self.__price)

    @property
    def body(self):
        return """
            היי גלית,
            מצאתי דירה 
            מבחינת נתונים:
            מיקום - {street}
            עיר - {city}
            מחיר - {price}
            קומה - {floor}
            מצב - {condition}
            חדרים - {rooms}
            גודל - {size}
            
            את יכולה להסתכל על הדירה בקישור הבא:
            {href}
            
            בתודה, עומר.
            """.format(
                street=self.__street,
                city=self.__city,
                price=self.__price,
                floor=self.__floor,
                condition=self.__condition,
                rooms=self.__rooms,
                size=self.__size,
                href=self.href
            )
    @property
    def href(self):
        if self.__source == 'yad2':
            return "https://yad2.co.il/item/{id}".format(id=self.__id)
        if self.__source == 'madlan':
            return "https://yad2.co.il/listings/{id}".format(id=self.__id)

    @property
    def row(self):
        return self.__row

    @row.setter
    def row(self, value):
        self.__row = value

    def to_dict(self):
        return {
            "id": self.__id,
            "row": self.__row,
            "street": self.__street,
            "sent": self.__sent,
            "subject": self.subject,
            "source": self.__source,
            "body": self.body,
            "href": self.href
        }

