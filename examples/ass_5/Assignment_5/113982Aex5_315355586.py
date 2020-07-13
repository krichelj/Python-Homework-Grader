class Location:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        if (type(self.x) != float) or (type(self.y) != float):   # the location type is not true
            raise TypeError("The type should be float!")
        if (self.x < 0) or (self.y < 0):   # if it is negative number
            raise ValueError("The number should be positive!")

    def distance_to(self, other):
        x_self = self.x
        y_self = self.y
        x_other = other.x
        y_other = other.y
        return ((x_self-x_other)**2 + (y_self-y_other)**2)**0.5   # the definition of the distance

    def __str__(self):
        return str(self.x) + "_" + str(self.y)   # return the string of the location

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
        if not isinstance(customer, Customer) or not isinstance(destination, Location) or not isinstance(origin, Location):
            raise TypeError("The type is not good, try again!")   # if one or more of the types is wrong

    def __len__(self):
        return round(self.origin.distance_to(self.destination))   # the distance on the trip

class Taxi:
    def __init__(self, id, location, rate):
        self.id = id
        self.location = location
        self.rate = rate

    def get_trips(self):
        good_trips = Company.good
        return good_trips.get(self, 0)   # sum of good trips is in the dictionary

class Company:
    good = {}   # dictionary when taxi is key and sum of good trips is value
    bad = 0   # add 1 every time the trip was not Succeeded
    def __init__(self):
        self.taxi_list = []   # empty list
        self.customer_list = []   # empty list

    def add_taxi(self, taxi):
        if taxi not in self.taxi_list:
            self.taxi_list.append(taxi)   # add taxis to the list taxi_list

    def add_customer(self, customer):
        if customer not in self.customer_list:
            self.customer_list.append(customer)   # add customers to the list customer_list

    def find_closest_taxi(self, trip):
        if len(self.taxi_list) == 0:   # if there are no taxis
            return None
        min_distance = self.taxi_list[0]   # define the closest taxi
        for taxi in self.taxi_list:
            if trip.origin.distance_to(taxi.location) < trip.origin.distance_to(min_distance.location):
                min_distance = taxi
        return min_distance   # return the closest taxi

    def handle_trip(self, trip):
        if len(self.taxi_list) == 0:   # if there are no taxis
            self.bad += 1   # add 1 to the failed trips (name bad)
            return False
        min_distance = self.find_closest_taxi(trip)
        price = min_distance.rate * trip.__len__()   # define the price the customer needs to pay
        money = trip.customer.credit   # define the money the customer has
        if money < price:   # not enough money
            self.bad += 1   # add 1 to the failed trips (name bad)
            return False
        trip.customer.add_credit(-price)   # minus price to the customer's money
        min_distance.location = trip.destination   # the taxi stay in the destination
        self.good[min_distance] = self.good.get(min_distance, 0) + 1   # plus 1 to the good trips dictionary
        return True


    def get_success_percentage(self):
        sum_good = sum(self.good.values())   # sums values from good trips dictionary
        return sum_good / (sum_good + self.bad)   # the percentage
