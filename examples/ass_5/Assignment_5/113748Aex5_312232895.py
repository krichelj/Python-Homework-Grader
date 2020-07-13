class Location:
    def __init__(self, x, y):
        if isinstance(x, float) and isinstance(y, float):
            if x < 0 or y < 0:
                raise ValueError("Coordinate must be positve")
            self.x = x
            self.y = y
        else:
            raise TypeError("Coordinate must be float")

    def distance_to(self, other):
        return ((self.x-other.x)**2 + (self.y-other.y)**2)**0.5

    def __str__(self):
        return str(self.x) + '_' + str(self.y)


class Customer:
    def __init__(self, name, id, credit=0):
        self.name = name
        self.id = id
        self.credit = credit

    def add_credit(self, addition):
        self.credit += addition


class Trip:
    def __init__(self, customer, origin, destination):
        if not isinstance(customer, Customer):
            raise TypeError("customer should be Customer type")
        self.customer = customer
        if isinstance(origin, Location) and isinstance(destination, Location):
            self.origin = origin
            self.destination = destination
        else:
            raise TypeError("should be Location type")

    def __len__(self):
        return round(self.origin.distance_to(self.destination))


class Taxi:
    def __init__(self, id, location, rate):
        self.id = id
        self.location = location
        self.rate = rate
        self.success = 0

    def get_trips(self):
        return self.success


class Company:
    def __init__(self):
        self.taxi_list = []
        self.customer_list = []
        self.good = 0
        self.bad = 0

    def add_taxi(self, taxi):
        self.taxi_list.append(taxi)

    def add_customer(self, customer):
        self.customer_list.append(customer)

    def find_closest_taxi(self, trip):
        if self.taxi_list is []:
            return None
        else:
            all_taxi_dest = []
            for taxi in self.taxi_list:
                all_taxi_dest.append(taxi.location.distance_to(trip.origin))
            for taxi in self.taxi_list:
                if taxi.location.distance_to(trip.origin) == min(all_taxi_dest):
                    return taxi

    def handle_trip(self, trip):
        if self.find_closest_taxi(trip) is None:
            self.bad += 1
            return False
        else:
            price = self.find_closest_taxi(trip).rate * len(trip)
            if price > trip.customer.credit:
                self.bad += 1
                return False
            else:
                trip.customer.credit -= price
                self.find_closest_taxi(trip).success += 1
                self.find_closest_taxi(trip).location = trip.destination
                self.good += 1
                return True

    def get_success_percentage(self):
        return self.good/(self.good + self.bad)
