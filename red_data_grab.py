from PIL import Image, ImageDraw
import PIL

def make_data_pool(img):
    robot_img = PIL.Image.open(img)
    test_px = robot_img.load()
    return robot_img

#----------------------------------------------------

print("start code")

R_data_list = make_data_pool("/Users/kibumkim/Documents/esp32_cam_code/1600x1200_1_robot_only.jpeg")
#G_data_list = make_data_pool()
#B_data_list = make_data_pool()

R_data_list.show()

