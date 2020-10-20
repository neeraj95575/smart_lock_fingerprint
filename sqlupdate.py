import time
from pyfingerprint.pyfingerprint import PyFingerprint
import sqlite3
import pyfingerprint
import hashlib
import sys

global str

def delete(): #delete the data from locker table
            try:
                  print("enter the id for delete info.")
                  r=input("enter id which you want to delete =")
                  conn = sqlite3.connect('finger_database.db')
                  curs= conn.cursor()
                  print("Connected to SQLite")
                  curs.execute('''DELETE FROM locker_table WHERE id = ?''',(r, ))
                  conn.commit()
                  print("Record Updated successfully ")
                  curs.close()
                  
            except Exception as e:
                     print('Operation failed!')
                     print('Exception message: ' + str(e))



def select():
                
               def allinfo():
                         try:
                                print(" all  info. from database ")
                                conn = sqlite3.connect('finger_database.db')
                                curs= conn.cursor()
                                print("Connected to SQLite")
                                curs.execute('''SELECT * FROM locker_table''')
                                records = curs.fetchall()
                                print("total rows are: ", len(records))
                                for row in records:
                                    print("\n*******************************************************************\n")
                                    print("id: ",row[0])
                                    print("name    : ",row[1])
                                    print("finger print: ",row[2])
                                    print("position of finger in device: ",row[3])
                                    print("\n*******************************************************************\n")
                      
                                    print("just end")
                                    conn.commit()
                                    print("Record Updated successfully ")
                                    curs.close()

                         except Exception as e:
                                    print('Operation failed!')
                                    print('Exception message: ' + str(e))

               def one():
                     try:
                            print("enter the id info. from database ")
                            r=input("enter  id =")
                            conn = sqlite3.connect('finger_database.db')
                            curs= conn.cursor()
                            print("Connected to SQLite")
                            
                            curs.execute('''SELECT name,hashval,position FROM locker_table WHERE id =?  ''',(r, ))
                            records = curs.fetchall()
                            for row in records:
                                    print("id ",row[0])
                                    print("name: ",row[1])
                                    print("position of finger in device: ",row[2])
                                    print("********************************************************************* ")
                                        
                                        
                            conn.commit()
                            print("Record Updated successfully ")
                            curs.close()

                     except Exception as e:
                         print('Operation failed!')
                         print('Exception message: ' + str(e))

        
               print("enter the choice =")
               print("1.getting all information  ")
               print("2.getting one information")

               z=int(input("enter your choice ="))
               if z == 1:
                  allinfo()
            
               elif z == 2:
                  one()
                        
                      
            
