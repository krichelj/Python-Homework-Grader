class Location:
    def __init__(self, x, y):
        self.x=x
        self.y=y
        z=2.1
        if type(x)!=type(z) or type(y)!=type(z):
            raise TypeError("values should be from type float!")
        if x<0 or y<0:
            raise ValueError("values should be positive!")

    def distance_to(self, other):
        one=(self.x-other.x)**2
        two=(self.y-other.y)**2
        distance=(one+two)**0.5
        return  distance

    def __str__(self):
        return str(self.x)+"_"+str(self.y)


class Customer:
    def __init__(self, name, id, credit=0):
        self.name=name
        self.id=id
        self.credit=credit


    def add_credit(self, addition):
        self.credit=self.credit+addition


class Trip:
    def __init__(self, customer, origin, destination):
        self.customer=customer
        self.origin=origin
        self.destination=destination
        if type(customer)!=Customer:
            raise TypeError("customer should be from Type Customer!")
        if type(destination)!=Location or type(origin)!=Location:
            raise TypeError("cordinates should be from type Location!")

    def __len__(self):
        return round(Location.distance_to(self.origin,self.destination))


class Taxi:
    def __init__(self, id, location, rate):
        self.id=id
        self.location=location
        self.rate=rate
        self.success=0 # will be in use in the company class

    def get_trips(self):
        return self.success




class Company:
    def __init__(self):
        self.taxi_list=[]
        self.customer_list=[]
        self.fail_trip=0  #for the get success rate
        self.success_trip=0 #for the get success rate

    def add_taxi(self, taxi):
        self.taxi_list.append(taxi)


    def add_customer(self, customer):
        self.customer_list.append(customer)

    def find_closest_taxi(self, trip):
        if len(self.taxi_list)==0:
            return None
        else:
         dest_lst=[]
         for i in range(0,len(self.taxi_list)):
            dest_lst.append(self.taxi_list[i].location.distance_to(trip.origin)) #making a list that will get the distances in the length and indexes like taxi_list
         closest=self.taxi_list[dest_lst.index(min(dest_lst))]
         return closest

    def handle_trip(self, trip):
        if len(self.taxi_list)==0:
            self.fail_trip+=1
            return False
        else:
          close_taxi=self.find_closest_taxi(trip)
          price=close_taxi.rate*trip.__len__()
          if price>trip.customer.credit:
            self.fail_trip+=1
            return False
          else:
                trip.customer.credit=trip.customer.credit-price
                for i in range(0,len(self.taxi_list)):
                    if close_taxi==self.taxi_list[i]:
                        self.taxi_list[i].location=trip.destination
                self.success_trip+=1
                close_taxi.success+=1
                return True

    def get_success_percentage(self):
        return (self.success_trip/(self.success_trip+self.fail_trip))
