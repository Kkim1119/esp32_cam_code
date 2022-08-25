from PIL import Image, ImageDraw
import PIL

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
            specific_data_pool.append(data_pool[i])
            #counter += 1
    average_value = combined_value / DATA_POOL_SIZE
    #print("count: " + str(counter) + " ")

    return specific_data_pool

#----------------------------------------------------
def give_robot_coordinate(img):
    robot_img = PIL.Image.open(img)  # Identifies and opens the image given during function call
    px = robot_img.load()  # Creates variable that holds pixel value and loads the image
    data_pool = list(robot_img.getdata())  # Parses through every pixel in image and stores RGB values in a list that it creates
    pixel_series_number = 0

    DATA_POOL_SIZE = len(data_pool)

    for i in range(DATA_POOL_SIZE):
        if (data_pool[i][0] > 175 and data_pool[i][1] < 150 and data_pool[i][2] < 200):
            pixel_series_number = i
            break;

    x_coordinate = pixel_series_number % 1600
    y_coordinate = pixel_series_number / 1600

    #-----Validation process code--------------------
    #px[x_coordinate, y_coordinate] = (0,0,255)

    #robot_img.convert("RGB")
    #robot_img.save("robot_location_1.jpg")

    return int(x_coordinate), int(y_coordinate)

#----------------------------------------------------

print("start code")

data_list = make_data_pool("/Users/kibumkim/Documents/esp32_cam_code/1600x1200_1.jpeg", 0)

print(give_robot_coordinate("/Users/kibumkim/Documents/esp32_cam_code/1600x1200_4.jpeg"))

with open("rgb_values.txt", "w") as f:
    print(data_list, file=f)
    f.close()
