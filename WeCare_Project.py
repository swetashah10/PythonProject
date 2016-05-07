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
listOfUserObjects = []

# Defining classes for different entities:

### USER class ###
class User(object):
    def __init__(self,name,uniqueID,zipcode,ssn,userType,pin,status):
        self._uniqueID = uniqueID
        self._name = name
        self._zipcode = zipcode
        self._status = status
        self._ssn = ssn
        self._pin = pin
        self._userType = userType
        if len(self._ssn) == 9:
            self._backgroundCheckStatus = 'Cleared'
        else:
            self._backgroundCheckStatus = 'Rejected'
        if userType == "Elderly":
             elderlyUsers[self._uniqueID] = [self._name,self._zipcode,  self._status, self._ssn, self._backgroundCheckStatus,self._uniqueID]
        elif userType == "Caregiver":
             caregiverUsers[self._uniqueID] = [self._name,self._zipcode,  self._status, self._ssn, self._backgroundCheckStatus,self._uniqueID]
 

    def __str__(self):
        return 'User Details: Unique ID: {} --- Name: {} --- Zipcode: {} --- Status: {} --- Background Check Status: {}'.format(str(self._uniqueID),self._name,self._zipcode,self._status,self._backgroundCheckStatus)

    def __save__(self, isCaregiver):
        if isCaregiver == True:
            caregiverUsers[self._uniqueID] = [self.__name]
            pickle.dump(caregiverUsers, open("caregiverUsers.p", "wb"))
        else:
            elderlyUsers[self._uniqueID] = str(self)
            pickle.dump(elderlyUsers, open("elderlyUsers.p","wb"))

### ELDERLY class ###
class Elderly(User):
    def __init__(self,name,uniqueID,zipcode,ssn,userType,pin,status="Not Served"):
        User.__init__(self,name,uniqueID,zipcode,ssn,userType,pin,status)
        self.elderlyUsingCareservices = {}
 
    def __str__(self):
        return User.__str__(self)

    def hasMatchingCaregivers(self):
        matchingCaregivers = []
        for caretaker in caregiverUsers:
            if caregiverUsers[caretaker][1] == self._zipcode:
                matchingCaregivers.append(caregiverUsers[caretaker])

        if len(matchingCaregivers) > 0:
            return True
        else:
            return False
        
    #@classmethod          
    def search_caregiver__(self):
        matchingCaregivers = []
        for caretaker in caregiverUsers:
            if caregiverUsers[caretaker][1] == self._zipcode and caregiverUsers[caretaker][1] != "Booked":
                matchingCaregivers.append(caregiverUsers[caretaker])

        if len(matchingCaregivers) > 0:
            print("")
            print("~~~~~~  Caregivers - Based on Zipcode EXACT Match: {}  ~~~~~~~".format(self._zipcode))
            print("____________________________________________________")
            print("Name \t\t Status \t Background Check\tUnique ID")
            print("-------------------------------------------------------------------------------------------")
            for caregiver in matchingCaregivers:
                print(caregiver[0],"\t\t",caregiver[2],"\t",caregiver[4],"\t\t",caregiver[5])
                print("")
        else:
            print("No match found...!")

    def checkBookedServices(self):
        return self.elderlyUsingCareservices
    
    def book_caregiver__(self,caregiverID):
        careID = int(caregiverID)
        isValidCaretaker = False
        for caretaker in caregiverUsers:
            if caregiverUsers[caretaker][5] == careID and caregiverUsers[caretaker][2] != "Booked":
                caregiverUsers[caretaker][2] = "Booked"
                for userObj in listOfUserObjects:
                    if userObj._userType == "Caregiver" and userObj._uniqueID == careID and isinstance(userObj, Caregiver):
                        userObj._status = "Booked"
                        self._status = "Being Served"
                        print("Congratulations! {}'s care services are now booked by you. Please release the booking, once the service period is complete.".format(userObj._name))
                        listOfCaregiversForElderly = []
                        listOfCaregiversForElderly.append(userObj)
                        if self in self.elderlyUsingCareservices:
                            listOfCaregiversForElderly = self.elderlyUsingCareservices[self]
                            listOfCaregiversForElderly.append(userObj)
                            self.elderlyUsingCareservices[self] = listOfCaregiversForElderly
                            isValidCaretaker = True
                        else:
                            listOfCaregiversForElderly = []
                            listOfCaregiversForElderly.append(userObj)
                            self.elderlyUsingCareservices[self] = listOfCaregiversForElderly
                            isValidCaretaker = True
        if isValidCaretaker == False:
            print("No ACTIVE caregivers found to book. Please try booking an ACTIVE caregiver.")
        
    def __isLoginUser__(self, username, userpin):
        if self._name == username and self._pin == userpin:
            return True
        else:
            return False

        
    def deactivateService(self):
         if self._status == "Being Served":



    def printMenu(self):
        exitElderlyPortal = False
        
        while exitElderlyPortal != True:

                   userInput = input("""

Welcome! Please select the menu option:

1. Search Caregivers
2. Book Care Service
3. Logout of Portal
4. Check My Booked Services
5. Deactivate a Service

""")
                   if userInput == '1':
                       self.search_caregiver__()
                   elif userInput == '2':
                       if self.hasMatchingCaregivers():
                           print(" ~~~~~ BOOKING a Caregiver Service ~~~~~~")
                           careGiverUniqueID = input("Please enter the unique ID of caregiver to book: ")
                           self.book_caregiver__(careGiverUniqueID)
                       else:
                           print("Sorry, there are no matching caregivers to book against. Please use option 1 to search for matching caregivers.")
                   elif userInput == '3':
                       print("Logging out of the Elderly Portal...Bye")
                       exitElderlyPortal = True
                   elif userInput == '4':
                       dictOfBookedServices = self.checkBookedServices()
                       if len(dictOfBookedServices) > 0:
                           for someObj in dictOfBookedServices:
                               print("Elderly Details:\n",str(someObj))
                               for listOfCaretakers in dictOfBookedServices[someObj]:
                                   print("Caregiver details: ",str(listOfCaretakers))
                       else:
                           print("Sorry, you do not have any booked services yet. Please use option 1 and 2 to book care services.")
                    elif userInput == '5':
                        if len(self.elderlyUsingCareservices[self]) <= 0 and self._status != "Being Served":
                            print("You cannot deactivate services as there are no services scheduled for you currently. Please check your booking details.")
                        else:
                            self.deactivateService()
                            
### CAREGIVER class ###
class Caregiver(User):
    def __init__(self,name,uniqueID,zipcode,ssn,userType,pin,status="Active"):
        User.__init__(self,name,uniqueID,zipcode,ssn,userType,pin,status)

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
6. Login to Elderly Portal
7. Login to Caregiver Portal

"""
import random
userChoice = input(todaysMenu)
exitIndicator = False
while exitIndicator != True:
    if userChoice == '1':
        print("You chose to register an Elderly user. Please enter the details below:")
        name = input("Name: ")
        zipcode = input("Zipcode: ")
        #status = input("Status ('Served','Not Served', 'Being Served'): ")
        ssn = input("SSN number: ")
        pin = input("PIN Number: ")
        elderly = Elderly(name,random.randint(100,1000),zipcode,ssn,"Elderly", pin)
        print(elderly)
        listOfUserObjects.append(elderly)
        userChoice = '100'
    elif userChoice == '2':
        print("You chose to register a Caregiver user. Please enter the details below: ")
        name = input("Name: ")
        zipcode = input("Zipcode: ")
        #status = input("Status ('Booked','Active', 'Inactive'): ")
        ssn = input("SSN number: ")
        pin = input("PIN Number: ")
        caregiver = Caregiver(name,random.randint(100,1000),zipcode,ssn,"Caregiver", pin)
        print(caregiver)
        listOfUserObjects.append(caregiver)
        userChoice = '100'
    elif userChoice == '3':
        print("Thank you for using WeCare.com. See you soon! Take Care!")
        exitIndicator = True
    elif userChoice == '4':
        found = False
        #caregivers = pickle.load(open("caregiverUsers.p","rb"))
        #print(caregivers)
        for userObj in listOfUserObjects:
            if userObj._userType == "Caregiver":
                found = True
                print(str(userObj))
        if found==False:
            print("No Caregivers registered in system yet. ")
        userChoice = '100'
    elif userChoice == '5':
        found = False
        #elderly = pickle.load(open("elderlyUsers.p","rb"))
        #print(elderly)
        for userObj in listOfUserObjects:
            if userObj._userType == "Elderly":
                found = True
                print(str(userObj))

        if found == False:
            print("No Elderly users registered in the system yet.")
        userChoice = '100'
    elif userChoice == '6':
        elderlyPortalMenu = """

        *** Welcome to Elderly Portal ***

        Please enter valid name and pin to login:
 
        """
        print(elderlyPortalMenu)
        name = input("Name: ")
        pin = input("Pin: ")
        for userObj in listOfUserObjects:
            if userObj._userType == "Elderly":
                if userObj._name == name and userObj._pin == pin:
                    #c = userObj
                    loginStatus = False
                    if isinstance(userObj, Elderly):
                        print("Login Successful!")
                        print("~~~~~~ Welcome {}! to the Elderly Portal.~~~~~~~~".format(userObj._name))
                        print("{}'s Profile Details".format(userObj._name))
                        print("Your zipcode is: {} ".format(userObj._zipcode))
                        print("Your status is: {}".format(userObj._status))
                        print("Your background check result: {}".format(userObj._backgroundCheckStatus))
                        loginStatus = True
                        userObj.printMenu()
                        loginStatus = True
                    elif loginStatus == False:
                        print("Login Failed! Please check your name and pin and try again...")
        userChoice = '100'
    else:
        userChoice = input(todaysMenu)
