class Location:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        if not isinstance(x, float):
            raise ValueError("ValueError: x must be float type")
        if not isinstance(y, float):
            raise ValueError("ValueError: y must be float type")
        if not self.valid():
            raise TypeError("TypeError: x and y must be possitive number")

    def valid(self):
        if self.x < 0 or self.y <0:
            return False
        else:
            return True

    def distance_to(self, other):
        distance = 0
        distance = ((((self.x-other.x)**2)-((self.y-other.y)**2))*0.5)
        return distance

    def __str__(self):
        return str(self.x)+"/"+str(self.y)


class Customer:
    def __init__(self, name, id, credit=0):
        self.name = name
        self.id = id
        self.credit = credit

    def add_credit(self, addition):
        self.addition = addition
        self.credit += addition
class Trip:
    def __init__(self, customer, origin, destination):
        self.customer = customer
        self.origin = origin
        self.destination = destination
        if not isinstance(customer,Customer):
            raise TypeError("TypeError: not belong to Customer,diffrent class")
        if not isinstance(origin,Location):
            raise TypeError("TypeError: not belong to Location,diffrent class")
        if not isinstance(destination,Location):
            raise TypeError("TypeError: not belong to Location,diffrent class")

    def __len__(self):
        return round(self.origin.distance_to(self.destination))

class Taxi:
    def __init__(self, id, location, rate):
        self.id = id
        self.location= location
        self.rate = rate

        def get_trips(self):
            Succses = 0
            if self.id.handle_trip == True:
                Succses = Succses+1
            return Succses

class Company:
    def __init__(self):
        self.Taxis = {}
        self.Customers = {}

    def add_taxi(self, taxi):
        self.taxi = taxi
        taxi.append(Taxis)

    def add_customer(self, customer):
        self.customer = customer
        customer.append(Customers)


    def find_closest_taxi(self, trip):
        self.trip = trip
        if len(self.taxi_list) == 0:
            return
       ### i faild, didn't handle the qeustion



    def handle_trip(self, trip):
        if len(self.taxi_list) == 0:
            self.Failed_trips = Failed_trips + 1
            return False
        Min_distance = self.find_closest_taxi(trip)
        price = Min_distance.rate * trip._len_()
        money = trip.customer.credit
        if money < price:
            self.Failed_trips = Failed_trips + 1
            return False
        trip.customer.add_credit(-price)
        min_distance.location = trip.destination
        self.Handle[Min_distance] = self.Handle.get(Min_distance, 0) + 1
        return True

    def get_success_percentage(self):
        return (self.Handle/(self.Handle+self.Failed_trips))

### i didn't handle the homework . i supoose it's batter to subbmited something than don't subbmit at all.
















