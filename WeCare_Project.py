"""

Project Proposal: WeCare.com provides a platform for Caregivers and Elderly to collaborate and help the
Elderly during times of need.

Basic Process Automation:
1. Elderly registers in the system as "Elderly"
2. Caregivers register in the system under category "Caregiver"
3. Elderly search for Caregiver providing care of particular pre-defined type.
4. Elderly choose a caregiver who fit in thier schedule, or System assigns a caregiver to the elderly by looking
at the schedules.
5. During the period of service, the "Caregiver" status is changed to "Not Available/Booked"
6. During the period of service, the "Elderly" status is changed to "Being Served"
7. After the period of service, the Caregiver status is changed to "Available"
8. After the period of service, the Elderly status is changed to "Looking" or "Served"
9. Rating system is in place for both Caregiver and Elderly. 

Student Name and ID: Sweta Shah, 87336
Faculty: Professor. Dr. Srinivasan Mandayam

"""
import pickle
caregiverUsers = {}
elderlyUsers = {}

# Defining classes for different entities:

### USER class ###
class User(object):
    def __init__(self,name,uniqueID,zipcode,status,ssn,userType):
        self._uniqueID = uniqueID
        self._name = name
        self._zipcode = zipcode
        self._status = status
        self._ssn = ssn
        if len(self._ssn) == 9:
            self._backgroundCheckStatus = 'Cleared'
        else:
            self._backgroundCheckStatus = 'Rejected'
        if userType == "Elderly":
             elderlyUsers[self._uniqueID] = [self.__name,self.__zipcode,  self._status, self.__ssn, self.__backgroundCheckStatus]
        elif userType == "Caregiver":
             caregiverUsers[self._uniqueID] = [self.__name,self.__zipcode,  self._status, self.__ssn, self.__backgroundCheckStatus]


    def __str__(self):
        return 'User Details: \nUnique ID: {} \nName: {} \nZipcode: {} \nStatus: {}\nBackground Check Status: {}'.format(str(self._uniqueID),self._name,self._zipcode,self._status,self._backgroundCheckStatus)

    def __save__(self, isCaregiver):
        if isCaregiver == True:
            caregiverUsers[self._uniqueID] = [self.__name]
            pickle.dump(caregiverUsers, open("caregiverUsers.p", "wb"))
        else:
            elderlyUsers[self._uniqueID] = str(self)
            pickle.dump(elderlyUsers, open("elderlyUsers.p","wb"))

### ELDERLY class ###
class Elderly(User):
    def __init__(self,name,uniqueID,zipcode,status,ssn,userType):
        User.__init__(self,name,uniqueID,zipcode,status,ssn,userType)

    def __str__(self):
        return User.__str__(self)

### CAREGIVER class ###
class Caregiver(User):
    def __init__(self,name,uniqueID,zipcode,status,ssn,userType):
        User.__init__(self,name,uniqueID,zipcode,status,ssn,userType)

    def __str__(self):
        return User.__str__(self)

#### MAIN METHOD ####  
# Display the initial menu: Register a user as Caregiver or Elderly.

todaysMenu = """

Welcome to WeCare.com portal. Please select one of the following actions:

1. Register a user under "Elderly" category
2. Register a user under "Caregiver" category
3. Quit
4. View Caregivers
5. View Elderly

"""
import random
userChoice = input(todaysMenu)
exitIndicator = False
while exitIndicator != True:
    if userChoice == '1':
        print("You chose to register an Elderly user. Please enter the details below:")
        name = input("Name: ")
        zipcode = input("Zipcode: ")
        status = input("Status ('Served','Not Served', 'Being Served'): ")
        ssn = input("SSN number: ")
        elderly = Elderly(name,random.randint(100,1000),zipcode,status,ssn,"Elderly")
        print(elderly)
        userChoice = '100'
    elif userChoice == '2':
        print("You chose to register a Caregiver user. Please enter the details below: ")
        name = input("Name: ")
        zipcode = input("Zipcode: ")
        status = input("Status ('Booked','Active', 'Inactive'): ")
        ssn = input("SSN number: ")
        caregiver = Caregiver(name,random.randint(100,1000),zipcode,status,ssn,"Caregiver")
        print(caregiver)
        userChoice = '100'
    elif userChoice == '3':
        print("Thank you for using WeCare.com. See you soon! Take Care!")
        exitIndicator = True
    elif userChoice == '4':
        caregivers = pickle.load(open("caregiverUsers.p","rb"))
        print(caregivers)
        userChoice = '100'
    elif userChoice == '5':
        elderly = pickle.load(open("elderlyUsers.p","rb"))
        print(elderly)
        userChoice = '100'
    else:
        userChoice = input(todaysMenu)
