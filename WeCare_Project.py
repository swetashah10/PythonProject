"""

Project Proposal: WeCare.com provides a platform for Caregivers and Elderly to collaborate and help the
Elderly during times of need.

Actors in the System:
1. Elderly User
2. Caregiver User
3. Sysadmin User

Basic Process Flow:
-- ELDERLY
1. Elderly create thier profile and register themselves by providing information like zipcode, SSN, secret pin and Name.
2. Elderly can search the database of caregivers and the exact match to their location is displayed by the program.
3. Elderly can book the services of an "Active" caregiver, the caregiver should not have "Booked" status.
4. Elderly can terminate / deactivate the caregiver reasons (for any reason, either completion of the service or unexpected change of event).
5. Once Elderly deactivates the service, the caregiver is "Active" again, and is available for anyone to book/reserve services.

--CAREGIVER
1. Caregiver create thier profile and register themselves by providing information like zipcode, SSN, secret pin and Name.
2. SSN is validated for correctness. Due to limited scope of this project, the number of digits in SSN is validated to be 9-digit number. If SSN is valid, the Background check
    status is "Cleared"
    If SSN is invalid (not 9-digit number), the Background check status is "Rejected".
3. Once Elderly books a service of a caregiver, the caregiver status changes to "Booked"
4. "Booked" caregivers are not visible in the search results.
5. Once Elderly deactivates the service, the caregiver status changes to "Active". Currently this is unidirectional. 


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


Assumptions:
1. SSN is deemed to be valid if it is a 9-digit number.
2. Pin code exact match is currently considered to be feasible to match caregivers with Elderly.
3. No database is used, and hence no data will be persisted.
4. Rating system to be implemented yet.

Student Name and ID: Sweta Shah, 87336
Faculty: Professor. Dr. Srinivasan Mandayam

"""
import pickle
print(__doc__)

# Global variables shared by all instances of classes defined below. 
caregiverUsers = {}
elderlyUsers = {}
listOfUserObjects = []
countForOption4 = 1
countForOption5 = 1
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
        return "User Details: Unique ID: {} --- Name: {} --- Zipcode: {} --- Status: {} ".format(str(self._uniqueID),self._name,self._zipcode,self._status)

    def hasMatchingCaregivers(self):
        matchingCaregivers = []
        for caretaker in caregiverUsers:
            if caregiverUsers[caretaker][1] == self._zipcode:
                matchingCaregivers.append(caregiverUsers[caretaker])

        if len(matchingCaregivers) > 0:
            return True
        else:
            return False
        
    def search_caregiver__(self):
        matchingCaregivers = []
        for caretaker in caregiverUsers:
            if caregiverUsers[caretaker][1] == self._zipcode and caregiverUsers[caretaker][2] != "Booked":
                matchingCaregivers.append(caregiverUsers[caretaker])

        if len(matchingCaregivers) > 0:
            print("")
            print("~~~~~~  Caregivers - Based on Zipcode EXACT Match: {}  ~~~~~~~".format(self._zipcode))
            print("____________________________________________________")
            print("Name \t\t Status \t Background Check\tUnique ID")
            print("-------------------------------------------------------------------------------------------")
            for caregiver in matchingCaregivers:
                print(caregiver[0],"\t",caregiver[2],"\t",caregiver[4],"\t\t",caregiver[5])
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
            caregiverID = input("Enter the Caregiver unique ID whose service you wish to terminate: ")
            #self._status = "Served"
            listOfCaregiversForElderly = self.elderlyUsingCareservices[self]
            listOfCaregiverToDeactivate = []
            beforeRemovalLen = len(listOfCaregiversForElderly)
            for item in listOfCaregiversForElderly:
                if item._uniqueID == int(caregiverID):
                    item._status = "Active"
                    listOfCaregiverToDeactivate.append(item._uniqueID)
                    listOfCaregiversForElderly.remove(item)
                    print("Caregiver {}'s services have been deactivated.".format(item._name))
                    
            
            afterRemovalLen = len(listOfCaregiversForElderly)
            if len(listOfCaregiversForElderly) == 0:
                del self.elderlyUsingCareservices[self]
                self._status = "Served"
            elif afterRemovalLen < beforeRemovalLen:
                self.elderlyUsingCareservices[self] = listOfCaregiversForElderly

            for userObj in listOfUserObjects:
                print("Inside for loop priting userObj: ",str(userObj))
                for iden in listOfCaregiverToDeactivate:
                    print("Inside for loop, printing iden value: ",iden)
                    if userObj._uniqueID == iden:
                        print("Inside IF, changing status from Booked to Active, initial status = ",userObj._status)
                        userObj._status = "Active"
                        print("Would you like to provide a rating for this Caregiver's services?")
                        rate = int(input("Rate between 1 - 5: "))
                        userObj._ratingList.append(rate)
                        review = input("Please enter a line of review: ")
                        if self._name in userObj._reviewText:
                            review += userObj._reviewText[self._name]
                        userObj._reviewText[self._name] = review
                        

            for caretaker in caregiverUsers:
                for iden in listOfCaregiverToDeactivate:
                    if caregiverUsers[caretaker][5] == iden and caregiverUsers[caretaker][2] == "Booked":
                        caregiverUsers[caretaker][2] = "Active"

                        
    def printMenu(self):
        exitElderlyPortal = False
        
        while exitElderlyPortal != True:

                   userInput = input("""

Please select the menu option:

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
                       isSelfInDict = self in self.elderlyUsingCareservices.keys()
                       if not isSelfInDict and self._status != "Being Served":
                           print("You cannot deactivate services as there are no services scheduled for you currently. Please check your booking details.")
                       else:
                           self.deactivateService()
                        
                            
### CAREGIVER class ###
class Caregiver(User):
    def __init__(self,name,uniqueID,zipcode,ssn,userType,pin,status="Active"):
        User.__init__(self,name,uniqueID,zipcode,ssn,userType,pin,status)
        self._ratingList = []
        self._reviewText = {}

    def __str__(self):
        return User.__str__(self)

    def checkRatingAndReviews(self):
        avg = 0
        sumOfRate = 0
        for rate in self._ratingList:
            sumOfRate += rate
        if len(self._ratingList) != 0:
            avg = sumOfRate // len(self._ratingList)
            
        print("Rating = "+str(avg))
        print("~~~~ REVIEWS ~~~~~")
        print(self._reviewText)
        
    def printMenu(self):
        exitCaregiverPortal = False
        while exitCaregiverPortal != True:
            userInput = input("""

Please select the menu option:

1. Check My Booked Services
2. View My Reviews anf Ratings
3. Logout of Portal


""")
            if userInput == '1':
                print("Implementation in progress....")
            elif userInput == '2':
                self.checkRatingAndReviews()
            elif userInput == '3':
                exitCaregiverPortal = True

#### MAIN METHOD ####  
# Display the initial menu: Register a user as Caregiver or Elderly.

todaysMenu = """

Welcome to WeCare.com portal.

Note:
a) As this is first run of the program, there are no Caregivers currently registered in the system.
b) Please register a couple of caregivers to book caregiver services, when you register as Elderly.


Please select one of the following actions:

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
    isFirstRunForOption4 = countForOption4
    isFirstRunForOption5 = countForOption5
    if userChoice == '1':
        print("You chose to register an Elderly user. Please enter the details below:")
        name = input("Name (Username): ")
        while len(name) == 0:
            print("Name aka username was not entered. Please enter a Name: ")
            name = input("Name (Username): ")
        zipcode = input("Zipcode: ")
        while not isinstance( zipcode, int ) and len(zipcode) != 5:
            print("Either zipcode entered in invalid number or length is not equal to 5. Please enter a valid 5-digit zipcode.")
            zipcode = input("Zipcode: ")
        ssn = input("SSN number (Optional): ")

        # Wanted to mask the pin here. However on using getpass module, the pin is not being echoed in terminal
        # or command line. It is being echoed with a warning message in IDLE window. Hence skipping using
        # getpass module, and masking of the pin altogether, as IDLE is what we have used in class so far.
        # Assuming IDLE will be used while testing this application. 
        pin = input("PIN Number (Please note your pin, will be required for login): ")
        while pin == "" or len(pin) == 0:
            print("Pin was not entered. Please enter a pin value.")
            pin = input("PIN Number (Please note your pin, will be required for login): ")
            
        elderly = Elderly(name,random.randint(100,1000),zipcode,ssn,"Elderly", pin)
        print(elderly)
        listOfUserObjects.append(elderly)
        userChoice = '100'
        
    elif userChoice == '2':
        print("You chose to register a Caregiver user. Please enter the details below: ")
        name = input("Name: ")
        while len(name) == 0:
            print("Name aka username was not entered. Please enter a Name: ")
            name = input("Name (Username): ")
        zipcode = input("Zipcode: ")
        while not isinstance( zipcode, int ) and len(zipcode) != 5:
            print("Either zipcode entered in invalid number or length is not equal to 5. Please enter a valid 5-digit zipcode.")
            zipcode = input("Zipcode: ")
        ssn = input("SSN number (Required for verification, please enter valid 9-digit SSN): ")
        while ssn == "" or len(ssn) != 9:
            print("Either you did not enter ssn or a 9-digit number was not specified.")
            ssn = input("SSN number (Required for verification, please enter valid 9-digit SSN): ")

        # Wanted to mask the pin here. However on using getpass module, the pin is not being echoed in terminal
        # or command line. It is being echoed with a warning message in IDLE window. Hence skipping using
        # getpass module, and masking of the pin altogether, as IDLE is what we have used in class so far.
        # Assuming IDLE will be used while testing this application. 
        pin = input("PIN Number (Please note your pin, will be required for login): ")
        while pin == "" or len(pin) == 0:
            print("Pin was not entered. Please enter a pin value.")
            pin = input("PIN Number (Please note your pin, will be required for login): ")
        caregiver = Caregiver(name,random.randint(100,1000),zipcode,ssn,"Caregiver", pin)
        print(caregiver)
        listOfUserObjects.append(caregiver)
        userChoice = '100'
        
    elif userChoice == '3':
        print("Saving the program object state....")
        try:
            elderlyFileObject = open("ElderlyObjects.p",'wb')
            caregiverFileObject = open("CaregiverObjects.p",'wb')
            for obj in listOfUserObjects:
                if obj._userType == "Elderly":
                    pickle.dump(obj, elderlyFileObject)
                elif obj._userType == "Caregiver":
                    pickle.dump(obj, caregiverFileObject)

            elderlyFileObject.close()
            caregiverFileObject.close()
            print("Please refer files: ElderlyObjects.p, CaregiverObjects.p for saved information.")
        except:
            print("Some exception occurred while saving the data.")
        print("Thank you for using WeCare.com. See you soon! Take Care!")
        exitIndicator = True
        
    elif userChoice == '4':
        found = False
        
        # Load the objects in the program, only during first run of the program.
        print("isFirstRunForOption4: ",isFirstRunForOption4)
        if isFirstRunForOption4 == 1:
            i = 1
            try:
                fileObj = open("CaregiverObjects.p","rb")
                while i:
                    try:
                        listOfUserObjects.append(pickle.load(fileObj))
                    except EOFError:
                        fileObj.close()
                        i=0
                        break;
            except IOError as e:
                print("I/O error({0}): {1}".format(e.errno, e.strerror))
            except:
                print("Unexpected error:", sys.exc_info()[1]) 

        for userObj in listOfUserObjects:
            if userObj._userType == "Caregiver":
                found = True
                print(str(userObj))
                caregiverUsers[userObj._uniqueID] = [userObj._name,userObj._zipcode, userObj._status, userObj._ssn, userObj._backgroundCheckStatus,userObj._uniqueID]

        if found==False:
            print("No Caregivers registered in system yet. ")
        countForOption4 += 1
        userChoice = '100'
        
    elif userChoice == '5':
        found = False

        # Load the objects in the program, only during first run of the program.
        print("isFirstRunForOption5: ",isFirstRunForOption5)
        if isFirstRunForOption5 == 1:
            i =1
            try:
                fileObj2 = open("ElderlyObjects.p","rb")
                while i:
                    try:
                        listOfUserObjects.append(pickle.load(fileObj2))
                    except EOFError:
                        fileObj2.close()
                        i=0
                        break;
            except IOError as e:
                print("I/O error({0}): {1}".format(e.errno, e.strerror))
            except:
                print("Unexpected error:", sys.exc_info()[1])
        
        #print(elderly)
        for userObj in listOfUserObjects:
            if userObj._userType == "Elderly":
                found = True
                print(str(userObj))
                elderlyUsers[userObj._uniqueID] = [userObj._name,userObj._zipcode,  userObj._status, userObj._ssn, userObj._backgroundCheckStatus,userObj._uniqueID]


        if found == False:
            print("No Elderly users registered in the system yet.")
        countForOption5 += 1
        userChoice = '100'
        
    elif userChoice == '6':
        elderlyPortalMenu = """

        *** Welcome to Elderly Portal ***

        Please enter valid name and pin to login:
 
        """
        print(elderlyPortalMenu)
        name = input("Name: ")
        pin = input("Pin: ")
        loginDueToPinFail = True
        for userObj in listOfUserObjects:
            if userObj._userType == "Elderly":
                if userObj._name == name and userObj._pin == pin:
                    loginDueToPinFail = False
                    loginStatus = False
                    if isinstance(userObj, Elderly):
                        print("Login Successful!")
                        print("~~~~~~ Welcome {}! to the Elderly Portal.~~~~~~~~".format(userObj._name))
                        print("{}'s Profile Details".format(userObj._name))
                        print("Your zipcode is: {} ".format(userObj._zipcode))
                        print("Your status is: {}".format(userObj._status))
                        loginStatus = True
                        userObj.printMenu()
                        loginStatus = True
                    elif loginStatus == False:
                        print("Login Failed! Please check your name and pin and try again...")
                elif loginDueToPinFail:
                    print("Login Failed! Please check your name and pin and try again...")
                    
        userChoice = '100'
    elif userChoice == '7':
        caregiverPortalMenu = """

        *** Welcome to Caregiver Portal ***

        Please enter valid name and pin to login:
 
        """
        print(caregiverPortalMenu)
        name = input("Name: ")
        pin = input("Pin: ")
        loginDueToPinFail = True
        for userObj in listOfUserObjects:
            if userObj._userType == "Caregiver":
                if userObj._name == name and userObj._pin == pin:
                    loginDueToPinFail = False
                    loginStatus = False
                    if isinstance(userObj, Caregiver):
                        print("Login Successful!")
                        print("~~~~~~ Welcome {}! to the Caregiver Portal.~~~~~~~~".format(userObj._name))
                        print("{}'s Profile Details".format(userObj._name))
                        print("Your zipcode is: {} ".format(userObj._zipcode))
                        print("Your status is: {}".format(userObj._status))
                        print("Your background check result: {}".format(userObj._backgroundCheckStatus))
                        loginStatus = True
                        userObj.printMenu()
                        loginStatus = True
                    elif loginStatus == False:
                        print("Login Failed! Please check your name and pin and try again...")
                elif loginDueToPinFail:
                    print("Login Failed! Please check your name and pin and try again...")
                    
        userChoice = '100'
    else:
        userChoice = input(todaysMenu)
