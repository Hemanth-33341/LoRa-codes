from datetime import datetime
from LoRaRF import SX127x
import time

busId = 0; csId = 0
resetPin = 22; irqPin = -1; txenPin = -1; rxenPin = -1
LoRa = SX127x()
print("Begin LoRa radio")
if not LoRa.begin(busId, csId, resetPin, irqPin, txenPin, rxenPin) :
    raise Exception("Something wrong, can't begin LoRa radio")

print("Set frequency to 433 Mhz")
LoRa.setFrequency(434000000)


print("Set modulation parameters:\n\tSpreading factor = 7\n\tBandwidth = 125 kHz\n\tCoding rate = 4/5")
LoRa.setSpreadingFactor(7)
LoRa.setBandwidth(125000)
LoRa.setCodeRate(4/5)

print("Set packet parameters:\n\tExplicit header type\n\tPreamble length = 12\n\tPayload Length = 15\n\tCRC on")
LoRa.setHeaderType(LoRa.HEADER_EXPLICIT)
LoRa.setPreambleLength(12)
LoRa.setPayloadLength(15)
LoRa.setCrcEnable(True)

print("Set syncronize word to 0x34")
LoRa.setSyncWord(0x34)
print("\n-- LoRa Node3 --\n")

# Receive message continuously
#while True :

    # Request for receiving new LoRa packet
#    LoRa.request()
    # Wait for incoming LoRa packet
#    LoRa.wait()

    # Put received packet to message and counter variable
    # read() and available() method must be called after request() or listen() method
message = "Node 2"
message_list=[]
    # available() method return remaining received payload length and will decrement each read() or get() method called
for i in message:
   message_list.append(ord(i))
print(len(message_list))

counter=0
while True:
   message = "Node 2"
   message_list=[]
    # available() method return remaining received payload length and will decrement each read() or get() method called
   for i in message:
       message_list.append(ord(i))

   time_slot=[[10,20],[40,50]]
   cur_time=datetime.now().second
   time_slot1=time_slot[0]
   time_slot2=time_slot[1]
   message_list.append(counter)
   message_list.append(datetime.now().hour)
   message_list.append(datetime.now().minute)
   message_list.append(datetime.now().second)

   if time_slot1[0] <= cur_time <= time_slot1[1] or time_slot2[0] <= cur_time <= time_slot2[1]:
      LoRa.beginPacket()
      LoRa.write(message_list,len(message_list))
      #LoRa.write(counter)
      #LoRa.write(datetime.now().hour)
      #LoRa.write(datetime.now().minute)
      #LoRa.write(datetime.now().second)
      LoRa.endPacket()
      LoRa.wait()
      print(len(message_list))
      print("Message sent from node-2 at ", datetime.now().hour ," hours " , datetime.now().minute , " minutes", datetime.now().second," seconds ")
      counter+=1
      time.sleep(10)
 
