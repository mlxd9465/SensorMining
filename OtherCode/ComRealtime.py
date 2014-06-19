# This python code is use to read the data from COM port. Install pyserial library 
# It is connected to the mysql database and if you want to use it on your computer, 
# change the host id, port id, user name, passwd, and db name
# The data is save in the "REALTIME" table
# by Enhao 




import serial
import pymysql



# Read data from Serial port. When you use different COM PORT, Change "port"
ser = serial.Serial(
    port='COM3',\
    baudrate=9600,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
        timeout=0)

print("connected to: " + ser.portstr)
count=1
output = str('')

while True:
    for line in ser.read():
        cha = chr(line)
        if cha != '$':
            output = output + cha
        else:
            if count == 1:
                count = count + 1
            else: 
                print(str(count)+str(':') + output)
                li = output.split(sep=",", maxsplit=2)
                
                #Remove the "$" form the string
                chanel1 = li[0].replace("$","")
                chanel2 = li[1]
                print(chanel1)
                print(chanel2)
                               
                
#Connct to the DB newttt
                conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='*****', db='newttt')
                cur=conn.cursor()   
                         
#Insert the data to the Table REALTIME            
                cur.execute("""INSERT INTO REALTIME(IndexID,Chanel1,Chanel2) VALUES
                  (%s,%s,%s)""",(count,chanel1,chanel2))
                conn.commit()
                cur.close()
                conn.close()
                output = str('$')
                count = count+1
            

ser.close()
