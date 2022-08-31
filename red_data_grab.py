from PIL import Image, ImageDraw
import PIL
import urllib.request
import http
import serial
import time
import math

def make_data_pool(img,rgb):                #Creates the RGB data pool in order to find the range of pixel values that match with robot hood only
    robot_img = PIL.Image.open(img)         #Identifies and opens the image given during function call
    robot_img.load()                        #Creates variable that holds pixel value and loads the image
    data_pool = list(robot_img.getdata())   #Parses through every pixel in image and stores RGB values in a list that it creates
    specific_data_pool = []
    combined_value = 0
    #counter = 0

    DATA_POOL_SIZE = len(data_pool)

    for i in range(DATA_POOL_SIZE):
        combined_value += data_pool[i][rgb]
        if(data_pool[i][0]>175 and data_pool[i][1]<150 and data_pool[i][2] <200):
            specific_data_pool.append(data_pool[i][rgb])
            #counter += 1
    average_value = combined_value / DATA_POOL_SIZE
    #print("count: " + str(counter) + " ")

    return specific_data_pool

#----------------------------------------------------
def give_robot_coordinate(url):                             #Takes a photo image of the robot and environment and gives robot pixel coordinate(x-max:1600, y-max: 1200)
    #img.write(urllib.request.urlopen(url).read())
    request_obj = urllib.request.urlopen(url)
    while True:
        try:
            img = open('1600x1200.jpg', 'wb')
            img.write(request_obj.read())
        except http.client.IncompleteRead:
            print("avoided exception")
            continue
        else:
            break

    img.close()

    robot_img = PIL.Image.open("1600x1200.jpg")               # Identifies and opens the image given during function call
    px = robot_img.load()                                     # Creates variable that holds pixel value and loads the image
    data_pool = list(robot_img.getdata())                     # Parses through every pixel in image and stores RGB values in a list that it creates
    pixel_series_number = 0
    x_and_y = []

    DATA_POOL_SIZE = len(data_pool)


    for i in range(DATA_POOL_SIZE):
        if (data_pool[i][0] > 201 and data_pool[i][1] < 128 and data_pool[i][2] < 170):
            pixel_series_number = i
            break

    x_coordinate = pixel_series_number % 1600
    y_coordinate = pixel_series_number / 1600

    x_and_y.append(int(x_coordinate))
    x_and_y.append(int(y_coordinate))
    #-----Validation process code--------------------
    px[x_coordinate, y_coordinate] = (0,0,255)

    robot_img.convert("RGB")
    robot_img.save("robot_location_1.jpg")

    return x_and_y
#-----------------------------------------------------
def give_image_robot_coords(img):                 #For testing the direction line creating function.
    robot_img = PIL.Image.open(img)               # Identifies and opens the image given during function call
    px = robot_img.load()                                     # Creates variable that holds pixel value and loads the image
    data_pool = list(robot_img.getdata())                     # Parses through every pixel in image and stores RGB values in a list that it creates
    pixel_series_number = 0
    x_and_y = []

    DATA_POOL_SIZE = len(data_pool)


    for i in range(DATA_POOL_SIZE):
        if (data_pool[i][0] > 201 and data_pool[i][1] < 128 and data_pool[i][2] < 170):
            pixel_series_number = i
            break

    x_coordinate = pixel_series_number % 1600
    y_coordinate = pixel_series_number / 1600

    x_and_y.append(int(x_coordinate))
    x_and_y.append(int(y_coordinate))


    return x_and_y

#-----Validation process code--------------------
    #px[x_coordinate, y_coordinate] = (0,0,255)

    #robot_img.convert("RGB")
    #robot_img.save("robot_location_1.jpg")
#----------------------------------------------------
def show_robot_direction(initial_x_y, new_x_y):              #compares the coordinates of the robot before and after moving, returns degrees of rotation of robot(starting at initial position)
    init_x = initial_x_y[0]
    init_y = initial_x_y[1]
    new_x = new_x_y[0]
    new_y = new_x_y[1]

    delta_x = new_x - init_x
    delta_y = new_y - init_y
    #robot_img = PIL.Image.open(img)  # Identifies and opens the image given during function call
    #px = robot_img.load()

    #draw = ImageDraw.Draw(robot_img)


    #draw.line((init_x,init_y, new_x,new_y), fill="blue", width=5)
    #draw.line((init_x,init_y, init_x, 0), fill="red", width=5)
    #robot_img.show()

    degree = math.degrees(math.atan(abs(delta_x) / abs(delta_y)))

    if(degree > 90):
        degree -= 90

    if(init_x<new_x):
        if(init_y>new_y):
            degree += 270
        elif(init_y<new_y):
            degree += 180
    elif(init_x>new_x):
        if(init_y<new_y):
            degree += 90

    return int(degree)

#----------------------------------------------------
def get_robot_coord():                    #gets the robot's coordinates and returns it
    final_x_y = [0,0]
    while (True):
        first_x_y = give_robot_coordinate("http://192.168.0.37/1600x1200.jpg")
        second_x_y = give_robot_coordinate("http://192.168.0.37/1600x1200.jpg")

        delta_x = first_x_y[0] - second_x_y[0]
        delta_y = first_x_y[1] - second_x_y[1]

        final_x = second_x_y[0]
        final_y = second_x_y[1]

        # print("delta x: " + str(delta_x))
        # print("delta y: " + str(delta_y))

        if (abs(delta_x) < 10 and abs(delta_y) < 10):
            break

    final_x_y[0] = final_x
    final_x_y[1] = final_y
    print(str(final_x) + ", " + str(final_y))

    return final_x_y
# ----------------------------------------------------
def run_and_make_packet(packet,initial_x_y, new_x_y):
    revision_id = "0" + hex(1)[2:]
    data_type = "0" + hex(5)[2:]
    packet_length = hex(20)[2:]
    degree = show_robot_direction(initial_x_y, new_x_y)
    x_and_y = get_robot_coord()
    coord_x = x_and_y[0]
    coord_y = x_and_y[1]

    checksum_value = 0x100 - ((int(revision_id,16)+int(data_type,16)+int(packet_length,16)+int(hex(degree)[2:],16)+int(hex(coord_x)[2:],16)+int(hex(coord_y)[2:],16)) & 0x00ff)
    #print("total hex: " + str(checksum_value))
    checksum= hex(checksum_value)[2:]
    #print("checksum: "+checksum)

    packet += revision_id + data_type + packet_length
    if(degree > 255):
        packet += "0"
    else:
        packet += "00"
    packet += hex(degree)[2:]

    if(coord_x > 255):
        packet += "0"
    else:
        packet += "00"
    packet += hex(coord_x)[2:]

    if(coord_y > 255):
        packet += "0"
    else:
        packet += "00"
    packet += hex(coord_y)[2:]

    packet += checksum
    #print("packet: " + packet)
    return packet
# ----------------------------------------------------
def sendData(data):         #sends data through the serial port to the robot. Encodes data in ASCII format
    #data += " "
    serialPort.write(data.encode())

# ----------------------------------------------------

#MAIN ------------------------------------------------------------- MAIN
#============== Open COM port ==================
global serialPort
with open("map_data.txt",'w') as f:
    f.close()
packet_sending_data = ""

#packet_sending_data += run_and_make_packet(packet_sending_data)


serialPort = serial.Serial(
    port="/dev/cu.usbserial-DN012CUI", baudrate=9600, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE
)
serialString = ""  # Used to hold data coming over UART

print("Open serial port")

#print(give_robot_coordinate("http://192.168.0.36/1600x1200.jpg"))


#data_list = make_data_pool("/Users/kibumkim/Documents/esp32_cam_code/1600x1200.jpg", 0)
#with open("rgb_values.txt", "w") as f:
    #print(data_list, file=f)
    #f.close()
while 1:
    #Wait until there is data waiting in the serial buffer
    if serialPort.in_waiting > 0:

        #Read data out of the buffer until a carraige return / new line is found
        serialString = serialPort.readline()

        #Print the contents of the serial data
        try:
            cmd = serialString.decode("Ascii")
            #if(cmd=="communication\r\n"):
                #sendData(packet_data)
            if(cmd[:2] == "01"):
                revision_byte = cmd[:2]
                dataType_byte = cmd[2:4]
                packetLength_byte = cmd[4:6]
                if(dataType_byte == "06"):
                    request_byte = cmd[6:8]
                    checksum_byte = cmd[8:10]
                    checksum_compare = hex(0x100 - ((int(revision_byte, 16) + int(dataType_byte, 16) + int(packetLength_byte, 16) + int((request_byte), 16)) & 0x00ff))[2:]
                    if(checksum_byte.capitalize() == checksum_compare.capitalize()):
                        print("correct data received")
                        if(request_byte == "01"):
                            initial_x_y = get_robot_coord()
                            new_x_y = [0,0]
                        elif(request_byte == "00"):
                            new_x_y = get_robot_coord()
                            show_robot_direction(initial_x_y,new_x_y)

                        packet_sending_data += run_and_make_packet(packet_sending_data,initial_x_y, new_x_y)
                        sendData(packet_sending_data)
                    else:
                        print("incorrect data received!!")
            elif(cmd.find("scan_data") != -1):
                with open("map_data.txt", "a") as f:
                    print(cmd, file=f)
                    f.close()

            print(cmd)
        except:
            pass