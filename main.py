print("Welcome to banking app")

loop = True

while(loop):
  print("Options\n1. Create Account\n2. Deposit\n3. Withdraw\n4. Check Balance\n5. Exit")
  option = int(input("Enter your option: "))
  if(option==5):
    loop = False
    break
  elif(option==1):
    print("option 1")
  elif(option==2):
    print("option 2")
  elif(option==3):
    print("option 3")
  elif(option==4):
    print("option 4")