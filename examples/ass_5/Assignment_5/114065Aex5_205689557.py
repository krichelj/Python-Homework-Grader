class Location:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        if not self.type_validate():
            raise TypeError("x and y must be of float type")
        if not self.value_validate():
            raise ValueError("x and y can not be negative")

    def type_validate(self):
        if type(self.x) != float or type(self.y) != float:
            return False
        else: return True

    def value_validate(self):
        if self.x < 0 or self.y < 0:
            return False
        else: return True

    def distance_to(self, other):
        return (((self.x - other.x)**2) + (self.y - other.y)**2)**0.5

    def __str__(self):
        return str(self.x) + "_" + str(self.y)


class Customer:
    def __init__(self, name, id, credit=0):
        self.name = name
        self.id = id
        self.credit = credit

    def add_credit(self, addition):
        self.credit += addition


class Trip:
    def __init__(self, customer, origin, destination):
        self.customer = customer
        self.origin = origin
        self.destination = destination
        if not self.type_validation():
            raise TypeError("The given customer, origin or destination type is wrong")

    def type_validation(self):
        if type(self.customer) != Customer or type(self.origin) != Location or type(self.destination) != Location:
            return False
        else: return True

    def __len__(self):
        return round(self.origin.distance_to(self.destination))


class Taxi:
    def __init__(self, id, location, rate):
        self.id = id
        self.location = location
        self.rate = rate

    def get_trips(self):
        return Company.success.get(self, 0)


class Company:
    success = {}
    failure = 0
    def __init__(self):
        self.taxi_list = []
        self.customer_list = []

    def add_taxi(self, taxi):
        if taxi not in self.taxi_list:
            self.taxi_list.append(taxi)

    def add_customer(self, customer):
        if customer not in self.customer_list:
            self.customer_list.append(customer)

    def find_closest_taxi(self, trip):
        if self.taxi_list == []:
            return None
        distances = []
        for taxi in self.taxi_list:
            distances.append(trip.origin.distance_to(taxi.location))
        index = distances.index(min(distances))
        return self.taxi_list[index]

    def handle_trip(self, trip):
        if self.find_closest_taxi(trip) == None:
            self.failure += 1
            return False
        taxi = self.find_closest_taxi(trip)
        price = taxi.rate*len(trip)
        if trip.customer.credit < price:
            self.failure += 1
            return False
        trip.customer.credit = trip.customer.credit - price
        taxi.location = trip.destination
        self.success[taxi] = self.success.get(taxi, 0) + 1
        return True

    def get_success_percentage(self):
        sum_success = 0
        for num_of_success in self.success:
            sum_success += self.success.get(num_of_success)
        return (sum_success/(sum_success + self.failure))