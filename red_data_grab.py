from PIL import Image, ImageDraw
import PIL
import urllib.request
import http
import serial
import time
import math

def make_data_pool(img,rgb):
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
def give_robot_coordinate(url):
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
    #-----Validation process code--------------------
    #px[x_coordinate, y_coordinate] = (0,0,255)

    #robot_img.convert("RGB")
    #robot_img.save("robot_location_1.jpg")

    return x_and_y
#----------------------------------------------------
def show_robot_direction(img):
    initial_x_y = give_image_robot_coords("/Users/kibumkim/Documents/esp32_cam_code/1600x1200_direction_test_2.jpeg")
    new_x_y = give_image_robot_coords("/Users/kibumkim/Documents/esp32_cam_code/1600x1200_direction_test_1.jpeg")

    init_x = initial_x_y[0]
    init_y = initial_x_y[1]
    new_x = new_x_y[0]
    new_y = new_x_y[1]

    delta_x = new_x - init_x
    delta_y = new_y - init_y
    robot_img = PIL.Image.open(img)  # Identifies and opens the image given during function call
    px = robot_img.load()

    draw = ImageDraw.Draw(robot_img)


    draw.line((init_x,init_y, new_x,new_y), fill="blue", width=5)
    draw.line((init_x,init_y, init_x, 0), fill="red", width=5)
    robot_img.show()

    degree = math.degrees(math.atan(abs(delta_x) / abs(delta_y)))

    if(init_x<new_x):
        if(init_y>new_y):
            degree += 270
        else:
            degree += 180
    else:
        if(init_y<new_y):
            degree += 90

    print(degree)

#----------------------------------------------------
def get_robot_coord():
    final_x_y = [0,0]
    while (True):
        first_x_y = give_robot_coordinate("http://192.168.0.36/1600x1200.jpg")
        second_x_y = give_robot_coordinate("http://192.168.0.36/1600x1200.jpg")

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
print("start code")

#print(give_robot_coordinate("http://192.168.0.36/1600x1200.jpg"))

#get_robot_coord()
show_robot_direction("/Users/kibumkim/Documents/esp32_cam_code/1600x1200_direction_test_2.jpeg")

#data_list = make_data_pool("/Users/kibumkim/Documents/esp32_cam_code/1600x1200.jpg", 0)
#with open("rgb_values.txt", "w") as f:
    #print(data_list, file=f)
    #f.close()


#============== Open COM port ==================
#serialPort = serial.Serial(
    #port="/dev/cu.usbserial-DN012CUI", baudrate=9600, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE
#)
#serialString = ""  # Used to hold data coming over UART
#print("Open serial port")
#while 1:
    # Wait until there is data waiting in the serial buffer
    #if serialPort.in_waiting > 0:

        # Read data out of the buffer until a carraige return / new line is found
        #serialString = serialPort.readline()

        # Print the contents of the serial data
        #try:
            #cmd = serialString.decode("Ascii")
            #print(cmd)
        #except:
            #pass