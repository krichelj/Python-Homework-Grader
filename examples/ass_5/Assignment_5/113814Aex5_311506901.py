class Location:
    def __init__(self, x, y):
        """generate a location by x and y - positive floats"""
        if x < 0 or y < 0:
            raise ValueError("Location's coordinate must be a positive number")
        if type(x) is not float:
            raise TypeError("Location's coordinate must be a float type")
        self.x = x
        self.y = y

    def distance_to(self, other):
        """compute the distance between two points"""
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5

    def __str__(self):
        """return the str() value of a Location object"""
        return str(self.x) + "_" + str(self.y)


class Customer:
    def __init__(self, name, id, credit=0):
        """Generate a customer object with the features: name, id number, credit number(money for travelling)"""
        self.name = name
        self.id = id
        self.credit = credit

    def add_credit(self, addition):
        """Add additional money to credit value of a customer"""
        self.credit += addition


class Trip:
    def __init__(self, customer, origin, destination):
        """Generate a trip object with the features: customer, origin(location) and destination(location)"""
        if type(customer) is not Customer or type(origin) is not Location or type(destination) is not Location:
            raise TypeError("wrong type in one or more of trip's fields")
        self.customer = customer
        self.origin = origin
        self.destination = destination

    def __len__(self):
        """compute the distance between origin and destination"""
        origin = self.origin
        destination = self.destination
        return round(origin.distance_to(destination))


class Taxi:
    def __init__(self, id, location, rate):
        """Generate a taxi object with the features id, location- of the taxi, rate- charge per distance unit
        and success_trips- number of successful trips by the taxi"""
        self.id = id
        self.location = location
        self.rate = rate
        self.success_trips = 0

    def get_trips(self):
        """return number of successful trips by a taxi """
        return self.success_trips


class Company:
    def __init__(self):
        """Generate a company object with the features: taxi_list, customer_list and fail_trips"""
        self.taxi_list = []
        self.customer_list = []
        self.fail_trips = 0

    def add_taxi(self, taxi):
        """Add a taxi to the taxi list"""
        self.taxi_list.append(taxi)

    def add_customer(self, customer):
        """add a customer to the customer list"""
        self.customer_list.append(customer)

    def find_closest_taxi(self, trip):
        """find the closest taxi to a trip origin"""
        if not self.taxi_list:
            return None
        closest = self.taxi_list[0]
        for i in self.taxi_list:
            if trip.origin.distance_to(i.location) < trip.origin.distance_to(closest.location):
                closest = i
        return closest

    def handle_trip(self, trip):
        """Check if a trip was successful or fail, add 1 to sum of fails or taxi success according to the result"""
        closest_taxi = self.find_closest_taxi(trip)
        if closest_taxi is None:  # condition for no taxi in the list
            self.fail_trips += 1  # add 1 to fails if the trip was failed
            return False
        price = closest_taxi.rate * len(trip)
        if trip.customer.credit < price:    # condition if credit is too low for the trip price
            self.fail_trips += 1            # add 1 to fail trips if trip was failed
            return False
        else:
            trip.customer.credit -= price  # case of successful trip - charge the price from credit
            closest_taxi.location = trip.destination  # update taxi location to destination
            closest_taxi.success_trips += 1        # add 1 to the taxi success counter


    def get_success_percentage(self):
        """compute the success percentage of the company"""
        sum_success = 0
        for i in self.taxi_list:
            sum_success += i.success_trips
        return sum_success / (self.fail_trips + sum_success)


