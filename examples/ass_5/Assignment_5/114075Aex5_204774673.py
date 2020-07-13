
class Location:
    def __init__(self, x, y):
        self.x=x
        self.y=y
        z=1.1
        if type(x)!=type(z) or type(y)!=type(z):
            raise TypeError('Wrong type of input')
        if x<0 or y<0:
            raise  ValueError("Input must be larger than zero")

    def distance_to(self, other):
        return ((self.x-other.x)**2+(self.y-other.y)**2)**0.5

    def __str__(self):
        return (str(self.x)+"_"+str(self.y))



class Customer:
    def __init__(self, name, id, credit=0):
        self.name=name
        self.id = id
        self.credit=credit

    def add_credit(self, addition):
        self.credit+=addition
    def __str__(self):
        return (str(self.name))



class Trip:
    def __init__(self, customer, origin, destination):
        if type(customer)!=Customer or type(destination)!=Location or type(origin)!=Location:
            raise TypeError('Wrong input of customer or destination or origin')
        self.origin=origin
        self.destination=destination
        self.customer=customer
    def __len__(self):
        return round(self.origin.distance_to(self.destination))



class Taxi:

    def __init__(self,id,location,rate):
        self.success=0
        self.id=id
        self.location=location
        self.rate=rate

    def change_location(self,NewLocation):
        self.location=NewLocation

    def get_trips(self):
        return int(self.success)
        self.succes+=1

class Company:

    def __init__(self):

        self.total_number_of_rides=0
        self.taxi_list=[]
        self.total_number_of_sucess=0
        self.customer_list=[]
    def add_taxi(self,taxi):
        self.taxi_list.append(taxi)


    def add_customer(self,customer):
        self.customer_list.append(customer)

    def find_closest_taxi(self, trip):
        distance_of_taxis = []
        name_of_taxis=[]
        if len(company.taxi_list)==0:
            return False
        else:
            for i in range(0,(len(self.taxi_list))):

                name_of_taxis.append(self.taxi_list[i])
                distance_of_taxis.append(self.taxi_list[i].location.distance_to(trip.origin))
            return name_of_taxis[distance_of_taxis.index(min(distance_of_taxis))]
    def handle_trip(self, trip):

        if len(self.taxi_list)==0:
            self.total_number_of_rides+=1
            return False
        else:
            if trip.customer.credit<(self.find_closest_taxi(trip).rate*len(trip)):
                self.total_number_of_rides+=1
                return False
            else:
                trip.customer.add_credit((self.find_closest_taxi(trip).rate*len(trip)*-1))
                self.find_closest_taxi(trip).success+=1
                self.find_closest_taxi(trip).change_location(trip.destination)
                self.total_number_of_rides+=1
                self.total_number_of_sucess+=1

                return True

    def get_success_percentage(self):
        if self.total_number_of_rides==0:
            return 0
        else:
             return self.total_number_of_sucess/self.total_number_of_rides


