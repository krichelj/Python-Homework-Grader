class Location:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        if (type(self.x) != float) or (type(self.y) != float):  # wrong type
            raise TypeError("invalid input type")
        if (self.x < 0) or (self.y < 0):  # negative input
            raise ValueError("input cannot be negative")

    def distance_to(self, other):
        x1 = self.x
        y1 = self.y
        x2 = other.x
        y2 = other.y
        return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5  # calculates the distance by definition

    def __str__(self):
        return str(self.x) + '_' + str(self.y)  # turns the point into a string


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
        if (type(customer) != Customer) or (type(origin) != Location) or (type(destination) != Location):  # wrong type
            raise TypeError("invalid input type")

    def __len__(self):
        return round(self.origin.distance_to(self.destination))  # returns the distance by using distance_to


class Taxi:
    def __init__(self, id, location, rate):
        self.id = id
        self.location = location
        self.rate = rate

    def get_trips(self):
        successful_rides = Company.ride_succeed
        return successful_rides.get(self, 0)  # returns the number of the successful rides by definition


class Company:
    ride_fail = 0  # number of fail rides
    ride_succeed = {}  # dictionary when Taxi is Key, num of successful trips is Value

    def __init__(self):
        self.taxi_list = []
        self.customer_list = []

    def add_taxi(self, taxi):
        self.taxi_list.append(taxi)

    def add_customer(self, customer):
        self.customer_list.append(customer)

    def find_closest_taxi(self, trip):  # finds the closest taxi to origin
        if len(self.taxi_list) == 0:  # no taxis
            return None
        else:
            closest_taxi = self.taxi_list[0]
            for taxi in self.taxi_list:  # compares between the taxis and finds the closest one
                if trip.origin.distance_to(taxi.location) < trip.origin.distance_to(closest_taxi.location):
                    closest_taxi = taxi
            return closest_taxi

    def handle_trip(self, trip):
        if len(self.taxi_list) == 0:  # no taxis
            self.ride_fail += 1  # updates the ride_fail
            return False
        else:
            closest_taxi = self.find_closest_taxi(trip)
            price = closest_taxi.rate * trip.__len__()
            money = trip.customer.credit
            if price > money:
                self.ride_fail += 1  # updates the ride_fail
                return False
            else:
                trip.customer.add_credit(-(price))  # updates the credit at customer
                closest_taxi.location = trip.destination  # updates the location of the taxi after the trip
                self.ride_succeed[closest_taxi] = self.ride_succeed.get(closest_taxi, 0) + 1  # updates ride_succeed
                return True

    def get_success_percentage(self):
        total_good_rides = sum(self.ride_succeed.values())
        return total_good_rides / (total_good_rides + self.ride_fail)  # returns the percentage of successful rides
