import os, sys
import csv
currentdir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(os.path.dirname(currentdir)))
from LoRaRF import SX127x
import time
from datetime import datetime

# Begin LoRa radio and set NSS, reset, busy, IRQ, txen, and rxen pin with connected Raspberry Pi gpio pins
# IRQ pin not used in this example (set to -1). Set txen and rxen pin to -1 if RF module doesn't have one
busId = 0; csId = 0
resetPin = 22; irqPin = -1; txenPin = -1; rxenPin = -1
LoRa = SX127x()
print("Begin LoRa radio")
if not LoRa.begin(busId, csId, resetPin, irqPin, txenPin, rxenPin) :
    raise Exception("Something wrong, can't begin LoRa radio")

# Set frequency to 915 Mhz
print("Set frequency to 915 Mhz")
LoRa.setFrequency(434000000)

# Set RX gain. RX gain option are power saving gain or boosted gain
print("Set RX gain to power saving gain")
LoRa.setRxGain(LoRa.RX_GAIN_POWER_SAVING, LoRa.RX_GAIN_AUTO)    # AGC on, Power saving gain

# Configure modulation parameter including spreading factor (SF), bandwidth (BW), and coding rate (CR)
# Receiver must have same SF and BW setting with transmitter to be able to receive LoRa packet
print("Set modulation parameters:\n\tSpreading factor = 7\n\tBandwidth = 125 kHz\n\tCoding rate = 4/5")
LoRa.setSpreadingFactor(7)                                      # LoRa spreading factor: 7
LoRa.setBandwidth(125000)                                       # Bandwidth: 125 kHz
LoRa.setCodeRate(4/5)                                             # Coding rate: 4/5

# Configure packet parameter including header type, preamble length, payload length, and CRC type
# The explicit packet includes header contain CR, number of byte, and CRC type
# Receiver can receive packet with different CR and packet parameters in explicit header mode
print("Set packet parameters:\n\tExplicit header type\n\tPreamble length = 12\n\tPayload Length = 15\n\tCRC on")
LoRa.setHeaderType(LoRa.HEADER_EXPLICIT)                        # Explicit header mode
LoRa.setPreambleLength(12)                                      # Set preamble length to 12
LoRa.setPayloadLength(15)                                       # Initialize payloadLength to 15
LoRa.setCrcEnable(True) 

#def save_to_excel(output_string):
#    split_data = output_string.split()
#    processed_data = [eval(item) if item.startswith('[') else item for item in split_data]
#    df = pd.DataFrame([processed_data], columns=['Data', 'Value1', 'Value2', 'Packet Status', 'RSSI', 'SNR'])
#    df.to_excel('C:\\Users\\admin\\Desktop\\test1.xlsx', index=False, header=not any(df.index))

# Set CRC enable

# Set syncronize word for public network (0x34)
print("Set syncronize word to 0x34")
LoRa.setSyncWord(0x34)

print("\n-- LoRa Receiver --\n")

# Receive message continuously
while True :

    # Request for receiving new LoRa packet
    LoRa.request()
    # Wait for incoming LoRa packet
    LoRa.wait()

    # Put received packet to message and counter variable
    # read() and available() method must be called after request() or listen() method
    message = []
    device=[]
    data=[]
    
    # available() method return remaining received payload length and will decrement each read() or get() method called
    while LoRa.available() :
          message.append(LoRa.read())
    print(f"Message:{message}")
    #length=len(message)
    for i in range(6):
       device.append( chr(message[i]))
    for i in range(6,len(message)):
       data.append( message[i]) 

    d_name = ''.join(device)
    
    cur_time = datetime.now().second
    if device[5] == '1' and 0 < cur_time < 10: 
    
    
    #counter = LoRa.read()
    #hour = LoRa.read()
    #minute = LoRa.read()
    #second = LoRa.read()

    # Print received message and counter in serial
        print(f"device:{d_name} data:{data}")
    #print(f"{message}  {counter} {hour} {minute} {second}")

    # Print packet/signal status including RSSI, SNR, and signalRSSI

    '''if device[5] == '1':
       f=open("node1.csv",'a')
       f.write(f"{d_name}",)
       f.write(f"count{data[0]},hrs:{data[1]},min:{data[2]},sec:{data[3]},RSSI:{LoRa.packetRssi()},SNR:{LoRa.snr()} \n")

    if device[5] == '2':
       f=open("node2.csv",'a')
       f.write(f"{d_name}",)
       f.write(f"count{data[0]},hrs:{data[1]},min:{data[2]},sec:{data[3]},RSSI{LoRa.packetRssi()},SNR{LoRa.snr()} \n")

    if device[5] == '3':
       f=open("node3.csv",'a')
       f.write(f"{d_name}",)
       f.write(f"count{data[0]},hrs:{data[1]},min:{data[2]},sec:{data[3]},RSSI{LoRa.packetRssi()},SNR{LoRa.snr()} \n")


    #f.write(str(counter)+" ", )
    #f.write(str(hour)+" ",)
    #f.write(str(minute)+" ",)
    #f.write(str(second)+ "\n")
    #f.close() 
    
    status = LoRa.status()
    if status == LoRa.STATUS_CRC_ERR : print("CRC error")
    elif status == LoRa.STATUS_HEADER_ERR : print("Packet header error")'''