import time
from pyfingerprint.pyfingerprint import PyFingerprint
import sqlite3
import pyfingerprint
import hashlib
import sys
import sqlupdate


print("create tabel\n")
print("Y. create the tabel ")
print("other wise if table is already created enter any key except -->  y or Y")
p=str(input("enter the choice ="))
conn = sqlite3.connect('finger_database.db')

if p == 'y' or 'Y':
    curs = conn.cursor()
    curs.execute("CREATE TABLE locker_table (id text not null,name text not null, hashval text not null, position text not null,primary key(hashval),unique(id))")
                 
      



## Enrolls new finger
##
while 1:

        print("\nEnter your choice \n")
        print("1. Enroll the record")
        print("2. Delete the record finger print from device")
        print("3. Delete the locker table values")
        print("4. Show the locker table values")
        print("\n\n*******************************************************************\n\n")       
            

####################################################################
        def delete(): #delete the fingerprint from device
             try:
                 f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

                 if ( f.verifyPassword() == False ):
                     raise ValueError('The given fingerprint sensor password is wrong!')

             except Exception as e:
                  print('The fingerprint sensor could not be initialized!')
                  print('Exception message: ' + str(e))
                  exit(1)

## Gets some sensor information
             print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))

## Tries to delete the template of the finger
             try:
                 positionNumber = input('Please enter the template position you want to delete: ')
                 positionNumber = int(positionNumber)

                 if ( f.deleteTemplate(positionNumber) == True ):
                      print('Template deleted!')

             except Exception as e:
                print('Operation failed!')
                print('Exception message: ' + str(e))
                exit(1)

 #########################################enroll####################################################       
## Tries to initialize the sensor nnnnnn
        def enroll():
            try:
                        f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

                        if ( f.verifyPassword() == False ):
                                            raise ValueError('The given fingerprint sensor password is wrong!')

            except Exception as e:
                  print('The fingerprint sensor could not be initialized!')
                  print('Exception message: ' + str(e))
                  exit(1)

                  ## Gets some sensor information
                  print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))

            ## Tries to enroll new finger
            try:
                             print('Waiting for finger...')

                             ## Wait that finger is read
                             while ( f.readImage() == False ):
                                           pass

                             ## Converts read image to characteristics and stores it in charbuffer 1
                             f.convertImage(0x01)

                             ## Checks if finger is already enrolled
                             result = f.searchTemplate()
                             positionNumber = result[0]

                             if ( positionNumber >= 0 ):
                                   print('Template already exists at position #' + str(positionNumber))
                               #    exit(0)

                             print('Remove finger...')
                             time.sleep(2)

                             print('Waiting for same finger again...')

                             ## Wait that finger is read again
                             while ( f.readImage() == False ):
                                             pass


                             ## Converts read image to characteristics and stores it in charbuffer 2
                             f.convertImage(0x02)

                             ## Compares the charbuffers
                             if ( f.compareCharacteristics() == 0 ):
                                             raise Exception('Fingers do not match')

                             ## Creates a template
                             f.createTemplate()

                             ## Saves template at new position number
                             positionNumber = f.storeTemplate()
                             r =input("Enter the name = ")
                             n = input("id = ")

                           
	            ## Loads the found template to charbuffer 1
                             f.loadTemplate(positionNumber, 0x01)

	            ## Downloads the characteristics of template loaded in charbuffer 1
                             characterics = str(f.downloadCharacteristics(0x01)).encode('utf-8')

                             ## Hashes characteristics of template
                             cre_hash = hashlib.sha256(characterics).hexdigest()
                             curs = conn.cursor()
                             curs.execute('INSERT INTO locker_table(id,name,hashval,position) values(? ,?, ? ,?)',( n,r,cre_hash, positionNumber))
                             conn.commit()
                             ## conn.close()
                             print('Finger enrolled successfully!')
                             print('New template position #' + str(positionNumber))




            except Exception as e:
                        print('Operation failed!')
                        print('Exception message: ' + str(e))
                         #exit(1)

        x=int(input("enter your choice ="))
        
        if x == 1:
             enroll()
          
        elif x == 2:
             delete()

        elif x == 3:
            sqlupdate.delete()

        elif x == 4:
           sqlupdate.select()
        

        
