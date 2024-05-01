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

def updateMoney(username, password, money):
  c.execute("""UPDATE banking 
  SET money = money + (?) 
  WHERE username = (?) 
  AND password = (?) """, (money, username, password))  #change
  print("Money Transferred")
  c.execute("""SELECT money 
  FROM banking 
  WHERE username = (?) AND password = (?) 
  """, (username, password))  #Used to test out functionality
  thing = c.fetchone()
  if(thing[0]<0):
    c.execute("""UPDATE banking 
    SET money = money - (?) 
    WHERE username = (?) 
    AND password = (?) """, (money, username, password))
    print("Can't have negative money. No money transferred.")
    return thing[0] - money;
  else: 
    con.commit()  #change saved
    return thing[0]

def delete_account(username, password, first_name, last_name):
  c.execute("""DELETE FROM banking 
  WHERE username = (?) AND password = (?) AND first_name = (?) AND last_name = (?) 
  """, (username, password, first_name, last_name))
  print("Account Deleted")
  con.commit()
def create_account():
  #Have user enter necessary info
  creating_account = True
  while (creating_account):
    print("Enter your name")
    creating_account = False
    #Confirm info with user
    #Add info to database
    print("-----------\nCreating account\n-----------")
    first_name = str(input("First name: "))
    last_name = str(input("Last name: "))
    username = str(input("Enter a username: "))
    password = str(input("Enter a password: "))
    
    print(f"==========Inserted Information==========\n"
          f"Username: {username}\n"
          f"First name: {first_name}\n"
          f"Last name: {last_name}\n"
          f"Password: {password}")
    print("\nIs this information correct?")
    print("=======================================")
    choice = str(input("Y/N: "))
    if (choice == "Y"):
      c.execute(
        """
      INSERT INTO banking (username, first_name, last_name, password, money) 
      VALUES((?), (?), (?), (?), (?))
      """, (username, first_name, last_name, password, 0))
      print("Account Created\n")
      con.commit()
    else:
      print("Cancelling Account Creation\n")
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

  if(data1 is not None and data2 is not None):
    uname = data2[0]
    fname = data2[1]
    lname = data2[2]
    password = data2[3]
    money = data2[4]
    dorw = ["deposit", "withdraw"]
    
    if (data1 == data2):
      print(f"\nAccess granted. Welcome {fname} {lname}.\n")
      accessing_account = True
      while (accessing_account):
        print("\n---What would you like to do?---")
        print("1. Deposit\n2. Withdraw\n3. Check balance\n4. Delete Account\n5. Log out\n")
        choice = int(input("Enter a number: "))
        if (choice == 5):
          print("\nLogging out...\n")
          accessing_account = False
          break
        elif (choice == 1 or choice == 2):
          amt = int(
              input(f"\nEnter the amount you would like to {dorw[choice-1]}: "))
          if (choice == 2):
            choice = -1
          money = updateMoney(uname, password, choice * amt)
        elif (choice == 3):
          print(f"Current Balance: {money}")
        elif(choice == 4):
          if(input("Are you sure you want to delete your account? (Y/N) ") == "Y"):
            delete_account(uname, password, fname, lname)
            break
    else:
      print("Access denied")
  else:
    print("Access denied")
print("Welcome to banking app")
#Num of users?
num = 0

loop = True
while loop:
  print("\n------------------Menu------------------")
  print("1. Create account\n2. Access account\n3. Exit\n")
  option = input("Enter a number: ")
  if option == '3':
    loop = False
    break
  elif option == '1':

    create_account()
  elif option == '2':

    access_account()
  elif option == '72':
    getDatabase()
  
#Idk
print("Exit")
con.close()
