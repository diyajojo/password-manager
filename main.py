import cryptography
from cryptography.fernet import Fernet # allows to encrypt texts
import os #operating system functionality
import secrets
import string 

def check_password_strength(password):
 
 strength=0
 upper=lower=digit=spl_char=False
 length=len(password)

 for char in password:
  if char.isupper():
   upper = True
  elif char.islower():
   lower = True
  elif char.isdigit():
   digit = True
  elif char in string.punctuation:
   spl_char=True

  if length>=8:
   strength+=1
  if lower:
   strength+=1
  if upper:
   strength+=1
  if digit:
   strength+=1
  if spl_char:
    strength+=1
  
  if strength >= 4:
   return "Strong"
  elif strength >= 2:
   return "Medium"
  else:
   return "Weak"
 

def random_password(length=12,include_uppercase=True, include_lowercase=True, include_digit=True,include_splchar=True):
 characters=''
 #character will contain all upercase,lowercase,digits and punctutation in python
 if include_lowercase:
  characters+= string.ascii_lowercase
 if include_uppercase:
  characters+= string.ascii_uppercase
 if include_digit:
  characters+= string.digits
 if include_splchar:
  characters+= string.punctuation

 if characters== '':
  raise ValueError("Cannot be an empty string")
 
 password=''.join(secrets.choice(characters) for _ in range(length)) #loop runs 12 times and adds random character from characters into password 
 return password


def create_key():
 key=Fernet.generate_key()
 with open('key.key','wb') as key_file:
  key_file.write(key) 

def load_key():
 if not os.path.exists('key.key'):
  create_key()
 with open('key.key','rb') as f:
  key= f.read()
 return key

key=load_key()
fer=Fernet(key)

def add_pass():
 name=input("Enter account name: ")
 while True:
  ch=input("Do you want to generate a random password(yes or no)? ")
  if(ch.lower()=='yes'):
   password = random_password()
   break
  elif(ch.lower()=='no'):
   password=input("Enter password: ")
   strength=check_password_strength(password)
   attempts=0
   while True:
    strength = check_password_strength(password)
    if strength == "Strong":
     break  
    print(f"Password strength: {strength}. Please try again.")
    password = input("Enter password: ")
    attempts += 1
    if attempts >= 3:
     print("Maximum attempts reached. Password must be strong.")
     return
     break
  else:
   print("Invalid Entry ")
   continue
   

 with open('password.txt','a+') as f :
  f.write(name + "|" + Fernet(load_key()).encrypt(password.encode()).decode() + "\n")

def view_pass():
 if not os.path.exists('password.txt'):
  print("No passwords are yet saved.")
 else:
  with open('password.txt','r') as f:
   for line in f:
    line.strip()
    if '|' in line:
     try:
      user,password=line.split('|',1)
      decrypted_password = Fernet(load_key()).decrypt(password.encode()).decode()
      print(f"User: {user} and Password: {decrypted_password}")
     except cryptography.fernet.InvalidToken:
      print(f"Error: Invalid data found for {user}.")

def del_pass():
 to_delete=input("Enter the username whose password is to be deleted ")
 with open('password.txt','r') as f , open('temp.txt','w') as temp_f:
  for line in f:
   if '|' in line:
    line=line.strip()
    user, pwd =line.split('|',1)
    if user!= to_delete:
     temp_f.write(line +"\n")
   else:
    print(f"Skipping invalid line in password file.")
 f.close()

 os.remove('password.txt')
 os.rename('temp.txt','password.txt')

 print(f"Password for {to_delete} deleted successfully.")

def search_pass():
 if not os.path.exists('password.txt'):
  print("No passwords are yet saved.")
 else:
  found=False
  user=input("Enter the username whose password is to be searched ")
  with open('password.txt','r') as f:
   for line in f:
    line=line.strip()
    if '|' in line:
     name, password=line.split('|',1)
     if user.lower()==name.lower():
       decrypted_password = Fernet(load_key()).decrypt(password.encode()).decode()
       print(f"Password for {user}: {decrypted_password}")
       found=True
       break
  if not found:
   print("User name not found")
  
 
  
  
def main():   
 print ("Password Manager that gives options to add, view or delete and search a password")   
 while True:
  mode=input("ADD/VIEW/DELETE/SEARCH. Enter your choice ")
  if mode.lower()=="view" :
   view_pass()
  elif mode.lower()=="add":
   add_pass()
  elif mode.lower()=="delete":
   del_pass()
  elif mode.lower()=="search":
   search_pass()
  else:
   print("Invalid entry")
  
main()
  