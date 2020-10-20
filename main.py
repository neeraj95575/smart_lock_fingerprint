import time
import hashlib
from pyfingerprint.pyfingerprint import PyFingerprint
import sqlite3
import RPi.GPIO as GPIO  
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(2,GPIO.OUT) #servo motor
GPIO.setup(3,GPIO.IN)   #ir sensor

p = GPIO.PWM(2, 50) # GPIO 2 for PWM with 50Hz
p.start(8.5) 



def my_callback1(channel1):
                                                count=0
                                                global time_stamp
                                                time_now = time.time()
                                                 #sleep(2)
                                                 #if (time_now - time_stamp) >=1:
                                                 #def fg():  2535 
                                                try:

                                                    #print("\nscan the finger print of student for getting info. from database \n")
                                                    f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

                                                    if ( f.verifyPassword() == False ):
                                                        raise ValueError('The given fingerprint sensor password is wrong!')

                                                except Exception as e:
                                                    print('The fingerprint sensor could not be initialized!')
                                                    print('Exception message: ' + str(e))
                                                    exit(1)

                                                ## Gets some sensor information
                                                print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))

                                                ## Tries to search the finger and calculate hash
                                                try:
                                                    #print('Waiting for finger...')

                                                    ## Wait that finger is read
                                                    while ( f.readImage() == False ):
                                                        pass

                                                    ## Converts read image to characteristics and stores it in charbuffer 1
                                                    f.convertImage(0x01)

                                                    ## Searchs template
                                                    result = f.searchTemplate()

                                                    positionNumber = result[0]
                                                    accuracyScore = result[1]

                                                    if ( positionNumber == -1 ):
                                                        print('No match found!')
                                                        print("door close")
                                                        p.start(8.5)
                                                        #exit(1)
                                                    else:
                                                        print('Found template at position #' + str(positionNumber))
                                                        ##print('The accuracy score is: ' + str(accuracyScore))

                                                    ## Loads the found template to charbuffer 1
                                                    f.loadTemplate(positionNumber, 0x01)
                                                    ## Downloads the characteristics of template loaded in charbuffer 1
                                                    characterics = str(f.downloadCharacteristics(0x01)).encode('utf-8')
                                                    ## Hashes characteristics of template
                                                    
                                                     ##print('SHA-2 hash of template: ' )
                                                    
                                                    global fp
                                                    fp=hashlib.sha256(characterics).hexdigest()
                                                    conn=sqlite3.connect('finger_database.db')
                                                    c=conn.cursor()
                                                    c.execute('''SELECT id,name,hashval,position FROM locker_table WHERE hashval=?  ''',(fp, ))
                                                    records1 = c.fetchall()
                                                    print_records= ' '
                                                    row=["Empty","Empty","Empty","Empty"]
                                                    for row in records1:
                                                                print_records =str(row) +"\n"
                                                                                                                        
                                                                ff=row[0]  ###### id
                                                                jj=row[1]  ##### name
                                                                                                    
                                                                dd=row[2]####### finger print
                                                                lk=row[3]#######  position
                                                                                                           
                                                    conn.commit()
                                                    conn.close()

                                                    if fp == dd:
                                                        p.ChangeDutyCycle(6.6)  ############## motor open the door
                                                        time.sleep(0.5)
                                                        print("name = " + jj)
                                                        print("door open")
                                                    else:
                                                        print("door close")
                                                        p.start(8.5)        ############## motor close the door

                                                    

                                                except Exception as e:
                                                    
                                                    print('Operation failed!')
                                                    print('Exception message: ' + str(e))      



GPIO.add_event_detect(3, GPIO.RISING, callback=my_callback1, bouncetime=6000)



