class Location:
    def __init__(self, x, y):
        self.x=x
        self.y=y
        if (type(x)!=float or type(y)!=float): #The TypeError
            raise TypeError ("The coordinate is not from float type, SYSTEM CRASHED")
        if (x<0 and y<0): #The ValueErrorr
            raise ValueError ("Can't be negative coordinate, SYSTEM CRASHED")

    def distance_to(self, other):
        self.other=other
        return (((self.x-other.x)**2)+(self.y-other.y)**2)**0.5 #The distance between the coordinates

    def __str__(self):
        return (str(self.x) +"_"+str(self.y))


class Customer:
    def __init__(self, name, id, credit=0):
        self.name=name
        self.id=id
        self.credit=credit

    def add_credit(self, addition):
        self.credit+=addition

class Trip:
    def __init__(self, customer, origin, destination):
        self.customer=customer
        self.origin=origin
        self.desination=destination
        if(isinstance(self.customer,Customer)==False or isinstance(self.origin,Location)==False or isinstance(self.desination,Location)==False):
            raise TypeError ("The objects are not from the right type, SYSTEM CRASHED") #Checking if one of values is invalid

    def __len__(self):
        return round(Location.distance_to(self.origin,self.desination))

class Taxi:
    def __init__(self, id, location, rate,gooddrive=0):#Added gooddrive to check how many succses drives the taxi did
        self.id=id
        self.location=location
        self.rate=rate
        self.gooddrive=gooddrive

    def get_trips(self):
        return self.gooddrive


class Company:
    def __init__(self,taxi_list=[],customer_list=[],gooddrive=0,totaldrive=0): #create the list + counters for the amount of taxi drives
        self.taxi_list=taxi_list
        self.customer_list=customer_list
        self.gooddrive=gooddrive
        self.totaldrive=totaldrive

    def add_taxi(self, taxi): #Add new taxi to the list
        self.taxi_list.append(taxi)

    def add_customer(self, customer): #Add new customer
        self.customer_list.append(customer)

    def find_closest_taxi(self, trip):
        if(self.taxi_list==[]): #If we didnt add any new taxi than return none
            return None
        else:
            count=1
            i=1
            x=self.taxi_list[0]
            while count!=len(self.taxi_list): #Checking for the taxi that is closet the most to the trip origin
                if Location.distance_to(self.taxi_list[i-1].location,trip.origin)>Location.distance_to(self.taxi_list[i].location,trip.origin):
                    x=self.taxi_list[i]
                i+=1
                count+=1
            return x

    def handle_trip(self, trip):
        self.totaldrive+=1
        if self.find_closest_taxi(trip)==None: #If no taxi was added, return false
            return False
        else:
            if(trip.customer.credit<=(self.find_closest_taxi(trip).rate*trip.__len__())): #The Customer cant pay
                return False
            else:
                trip.customer.credit-=self.find_closest_taxi(trip).rate*trip.__len__() #Lower customer credits
                self.find_closest_taxi(trip).gooddrive+=1
                self.find_closest_taxi(trip).location=trip.desination#Set new taxi destination
                self.gooddrive+=1
                return True

    def get_success_percentage(self):
        return self.gooddrive/self.totaldrive #Return amount of drives that been good





