import sqlite3

con = sqlite3.connect(
    'banking.db')  # This creates or opens the file 'example.db' as a database
c = con.cursor()
#Test table creation
sql = """
    CREATE TABLE IF NOT EXISTS banking (
        username text, 
        first_name text,
        last_name text,
        password text,
        money integer
    )
"""
c.execute(sql)

#PRACTICE WITH SQLITE IS EITHER COMMENTED OUT OR DELETED
#c.execute("""
#    INSERT INTO banking (username, first_name, last_name, password, money)
#    VALUES('WaffleWaffler230', 'Joe', 'Golberg', 'E101M921', 1000),
#    ('Raisin', 'Emily', 'McDonald', 'Mero93', 7800),
#    ('BarneyTheDino', 'Drew', 'Gooden', '02ie012', 20100)
#""")

#c.execute("""UPDATE banking SET money = money + 100 WHERE userID = (?) """, '1')

#Testing how parameters work in this
#Jack/userID 1 should have 100 more money every time we run the program

#c.execute("""SELECT DISTINCT name FROM users WHERE gender = 'M'""")

#c.execute("""SELECT DISTINCT money FROM users WHERE gender = 'M'""")

con.commit()

#I can't look directly at data in example.db but i can SELECT it in main.py so i guess it should be fine
#SELECT works :D


#Deposit, withdraw, check balance, transfer money, check account details, exit
def getDatabase():
  c.execute("""SELECT * 
  FROM banking""")
  print(c.fetchall())

def updateName(username, password, first_name="", last_name=""):
  if (first_name != "" and last_name != ""):
    c.execute("""UPDATE banking 
    SET first_name = (?), last_name = (?) 
    WHERE username = (?) AND password = (?) 
    """, (first_name, last_name, username, password))  #change
    print("name updated")
    c.execute("""
    SELECT first_name, last_name 
    FROM banking 
    WHERE username = (?) AND password = (?) 
    """, (username, password))  #Used to test out functionality
    thing = c.fetchone()
    con.commit()  #change saved
    return thing[0], thing[1]
  return "N/A", "N/A"
#Update money in account
def updateMoney(username, password, money):
  c.execute("""UPDATE banking 
  SET money = money + (?) 
  WHERE username = (?) 
  AND password = (?) """, (money, username, password))  #change
  
  c.execute("""SELECT money 
  FROM banking 
  WHERE username = (?) AND password = (?) 
  """, (username, password))  #Used to test out functionality
  thing = c.fetchone()
  if(thing[0]<0): #Check if the money is negative
    #Reset changes and cancel transfer
    c.execute("""UPDATE banking 
    SET money = money - (?) 
    WHERE username = (?) 
    AND password = (?) """, (money, username, password))
    print("Can't have negative money. No money transferred.")
    return thing[0] - money #Return previous money value
  else: #Else not necessary but looks nice
    print("Money Transferred")
    con.commit()  #change saved
    return thing[0] #Return the new money value
#Delete account
def delete_account(username, password, first_name, last_name):
  #Delete account
  c.execute("""DELETE FROM banking 
  WHERE username = (?) AND password = (?) AND first_name = (?) AND last_name = (?) 
  """, (username, password, first_name, last_name))
  print("Account Deleted")
  con.commit()
def create_account():
  #Have user enter necessary info
  creating_account = True
  while (creating_account):
    print("-----------\nCreating account\n-----------")
    first_name = str(input("First name: "))
    last_name = str(input("Last name: "))
    username = str(input("Enter a username: "))
    password = str(input("Enter a password: "))
    #Confirm info with user
    print(f"==========Inserted Information==========\n"
          f"Username: {username}\n"
          f"First name: {first_name}\n"
          f"Last name: {last_name}\n"
          f"Password: {password}")
    print("\nIs this information correct?")
    print("=======================================")
    choice = str(input("Y/N: "))
    if (choice == "Y"):
      #Add info to database
      c.execute(
        """
      INSERT INTO banking (username, first_name, last_name, password, money) 
      VALUES((?), (?), (?), (?), (?))
      """, (username, first_name, last_name, password, 0))
      print("Account Created\n")
      con.commit()
      break
    else:
      #Ask to repeat loop
      if(input("Would you like to try again? Y/N: ") == "Y"):
        print("Reseting Account Creation\n")
      else:
        print("Exiting Account Creation\n")
        creating_account = False
        break
def access_account():
  #Password and user name
  print("\n-----------Accessing Account-----------\n")
  usern = input("Enter your username: ")
  passw = input("Enter your password: ")
  #Check if username and password are in database
  c.execute("""SELECT * 
  FROM banking WHERE password = (?) """, (passw, ))
  data1 = c.fetchone()
  c.execute("""SELECT * 
  FROM banking WHERE username = (?)""", (usern, ))
  data2 = c.fetchone()
  #Check if data retrieved isnt empty
  if(data1 is not None and data2 is not None):
    #assign data to variables
    uname = data2[0]
    fname = data2[1]
    lname = data2[2]
    password = data2[3]
    money = data2[4]
    dorw = ["deposit", "withdraw"]
    #check if data is the same
    if (data1 == data2):
      #access account
      print(f"\nAccess granted. Welcome {fname} {lname}.\n")
      accessing_account = True
      while (accessing_account):
        #Options for account
        print("\n---What would you like to do?---")
        print("1. Deposit\n2. Withdraw\n3. Check balance\n4. Delete Account\n5. Log out\n")
        choice = int(input("Enter a number: "))
        #Return to main menu
        if (choice == 5):
          print("\nLogging out...\n")
          accessing_account = False
          break
        #Deposit or withdraw depending on choice num
        elif (choice == 1 or choice == 2):
          amt = int(
              input(f"\nEnter the amount you would like to {dorw[choice-1]}: "))
          if (choice == 2):
            choice = -1
          money = updateMoney(uname, password, choice * amt)
        #Print balance
        elif (choice == 3):
          print(f"Current Balance: {money}")
        #Input confirmation to delete account
        elif(choice == 4):
          if(input("Are you sure you want to delete your account? (Y/N) ") == "Y"):
            delete_account(uname, password, fname, lname)
            break
    else:
      print("Access denied")
  else:
    print("Access denied")
#Main menu
print("Welcome to banking app")
loop = True
while loop:
  print("\n------------------Menu------------------")
  print("1. Create account\n2. Access account\n3. Exit\n")
  option = input("Enter a number: ")
  #Exit
  if option == '3':
    loop = False
    break
  #Create account
  elif option == '1':
    create_account()
  #Access account
  elif option == '2':
    access_account()
  #Print database
  elif option == '72':
    getDatabase()
  
#Idk
print("Exit")
con.close()
