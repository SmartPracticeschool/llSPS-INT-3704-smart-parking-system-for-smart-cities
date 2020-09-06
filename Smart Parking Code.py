import time,random,sys
import ibmiotf.device

#Provide your IBM Watson Device Credentials

organisation="00ugak"
devicetype="NodeMCU"
deviceid="car"
authm="token"
authtoken="12345678"

def myCommandCallback(cmd):
    print("Command received:%s"% cmd.data["command"])       #commands
    print("Booking a slot.")                                    
try:
    dataop={"org":organisation,"type":devicetype,"id":deviceid,"auth-method":authm,"auth-token":authtoken}
    devicecli=ibmiotf.device.Client(dataop)

#.....................................................
except Exception as e:
    print("Caught exception connecting device:%s"% str(e))
    sys.exit()
    
devicecli.connect()

totalslot=5
emptyslot=5                         #total 5 slots empty by default
slot=[1,1,1,1,1]                    #all 5 slots empty initially
total_entered=0
total_exits=0
while True:
    previous=emptyslot
    #entry gate
    IRentry=random.randint(0,1)     #IRsensor gives 1 if there is a vehicle at the gate
    if IRentry==1:
        print("Opening the entry gate")
        total_entered=total_entered+1
    if emptyslot==0:
        print("Sorry,parking slots are NOT AVAILABLE!!")        #print a message if no slots available

    emptyslot=0
    
    #Check for empty slots
    ultrasonic1=random.randint(2,400)
    if ultrasonic1<=40:
        print("Slot 1 OCCUPIED")
        slot[0]=0                   #setting flag 0 for occupied slot
    else:
        print("Slot 1 AVAILABLE")
        slot[0]=1                   #setting flag 1 for available slot
        
    ultrasonic2=random.randint(2,400)
    if ultrasonic2<=40:
        print("Slot 2 OCCUPIED")
        slot[1]=0
    else:
        print("Slot 2 AVAILABLE")
        slot[1]=1

    
    ultrasonic3=random.randint(2,400)
    if ultrasonic1<=40:
        print("Slot 3 OCCUPIED")
        slot[2]=0
    else:
        print("Slot 3 AVAILABLE")
        slot[2]=1

    ultrasonic4=random.randint(2,400)
    if ultrasonic3<=40:
        print("Slot 4 OCCUPIED")
        slot[3]=0
    else:
        print("Slot 4 AVAILABLE")
        slot[3]=1

    ultrasonic5=random.randint(2,400)
    if ultrasonic5<=40:
        print("Slot 5 OCCUPIED")
        slot[4]=0
    else:
        print("Slot 5 AVAILABLE")
        slot[4]=1


        
    for i in slot:
        if i==1:
            emptyslot=emptyslot+1
            
    data={"available_slots":emptyslot,"filled_slots":5-emptyslot,"total":totalslot}
    def myonpublishcallback():
        print("Number of vacant slots are %s"% emptyslot)
        
    success=devicecli.publishEvent("slots info","json",data,qos=1,on_publish=myonpublishcallback())       #publishing data to cloud
    
    if not success:
        print("Not connected to IOTf.")
    

         #exit gate
    IRexit=random.randint(0,1)
    if IRexit==1:
        print("Opening the exit gate.THANK YOU for visiting!!")
        total_exits==total_exits+1
    
    time.sleep(5)                      #checks status every 5 seconds
    devicecli.commandCallback=myCommandCallback

print(total_entered)
print(total_exits)
    
# Disconnect the device and application from the cloud
devicecli.disconnect()
