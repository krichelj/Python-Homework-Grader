class Location:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        if not self.float_validation():
            raise TypeError('X and Y Must be float')
        if not self.negative_validation():
            raise ValueError('X and Y cant be negative')


    def float_validation(self):
        """ validation for the init """
        if (type(self.x) != float) or (type(self.y) != float):
            return False
        else:
            return True

    def negative_validation(self):
        """ validation for the init """
        if (self.x < 0) or (self.y < 0):
            return False
        else:
            return True


    def distance_to(self, other):
        """returns the distance between two locations"""
        return ((self.x - other.x)**2 + (self.y - other.y)**2)**0.5

    def __str__(self):
        return str(self.x)+"_"+str(self.y)



class Customer:
    def __init__(self, name, id, credit=0):
        self.name = name
        self.id = id
        self.credit = credit


    def add_credit(self, addition):
        """adding the addition to the customers credit"""
        self.credit = self.credit + addition


class Trip:
    def __init__(self, customer, origin, destination):
        self.customer = customer
        self.origin = origin
        self.destination = destination
        """validations for the init"""
        if not isinstance(self.customer, Customer):
            raise TypeError("The types are not correct")
        if not isinstance(self.origin, Location):
            raise TypeError("The types are not correct")
        if not isinstance(self.destination, Location):
            raise TypeError("The types are not correct")


    def __len__(self):
        """returns the rounded distance between the origin and the destination"""
        return round(((self.destination.x - self.origin.x) ** 2 + (self.destination.y - self.origin.y) ** 2) ** 0.5)


class Taxi:
    def __init__(self, id, location, rate):
        self.id = id
        self.location = location
        self.rate = rate
        """the trips will be used later for counting the successful rides, adding 1 for every successful one"""
        self.trips = 0


    def get_trips(self):
        """returns the successful rides"""
        return self.trips



class Company:
    def __init__(self, taxi_lst=[], customer_lst=[]):
        self.taxi_lst = taxi_lst[:]
        self.customer_lst = customer_lst[:]
        self.successful_rides = 0
        self.not_successful_rides = 0


    def add_taxi(self, taxi):
        """adding a taxi to the taxi list"""
        self.taxi_lst.append(taxi)


    def add_customer(self, customer):
        """adding a customer to the customer list"""
        self.customer_lst.append(customer)

    def find_closest_taxi(self, trip):
        """if there are no taxis, return None"""
        if len(self.taxi_lst)==0:
            return None
        else:
            """if there are taxis, it's creating lists of locations and distances, and searching for the min distance"""
            taxis_locations_lst =[]
            taxis_distance_from_trip_origin_lst = []
            for taxi in self.taxi_lst:
                taxis_locations_lst.append(taxi.location)
            for location in taxis_locations_lst:
                taxis_distance_from_trip_origin_lst.append(location.distance_to(trip.origin))
            min_distance = min(taxis_distance_from_trip_origin_lst)
            """after finding the min distance, it finds for which taxi that belong, by using its index in the list"""
            index_of_min = taxis_distance_from_trip_origin_lst.index(min_distance)
            """finally, we've got the taxi with the min distance. Now we'll return it"""
            return self.taxi_lst[index_of_min]

    def handle_trip(self, trip):
        closest_taxi = self.find_closest_taxi(trip)
        """if the there are no taxis, so we'll count it and return false"""
        if closest_taxi == None:
            self.not_successful_rides = self.not_successful_rides + 1
            return False
        else:
            """if there is a taxi, we'll calculate its price: rate * trip's len"""
            price = (closest_taxi.rate) * (len(trip))
            """if the customer doesn't have enough money, the ride won'y happen - we'll count it and return false"""
            if trip.customer.credit < price:
                self.not_successful_rides = self.not_successful_rides + 1
                return False
            else:
                """if the customer is able to pay, the ride happens and the customers credit reduces by the price"""
                trip.customer.credit = trip.customer.credit - price
                """the taxis location is changing to the destination of the trip"""
                closest_taxi.location = trip.destination
                """we'll count this successful rides both for the company and for the taxi"""
                self.successful_rides = self.successful_rides + 1
                closest_taxi.trips = closest_taxi.trips + 1
                return True

    def get_success_percentage(self):
        """calculating the percentage of successful rides out of all the rides attempts"""
        return (self.successful_rides)/((self.successful_rides + self.not_successful_rides))



