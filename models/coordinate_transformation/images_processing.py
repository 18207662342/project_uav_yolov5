import numpy as np
import cv2
import os

def get_photo_data(jpg_input_path):
    b = b"\x3c\x2f\x72\x64\x66\x3a\x44\x65\x73\x63\x72\x69\x70\x74\x69\x6f\x6e\x3e"
    a = b"\x3c\x72\x64\x66\x3a\x44\x65\x73\x63\x72\x69\x70\x74\x69\x6f\x6e\x20"
    dj_data_dict = {}
    img = open(jpg_input_path, 'rb')
    data = bytearray()
    flag = False
    for i in img.readlines():
        if a in i:
            flag = True
        if flag:
            data += i
        if b in i:
            break
    if len(data) > 0:
        data = str(data.decode('ascii'))
        lines = list(filter(lambda x: 'drone-dji:' in x, data.split("\n")))
        for d in lines:
            d = d.strip()[10:]
            k, v = d.split("=")
            # print(f"{k} : {v}")
            dj_data_dict[str(k)] = str(v)
        # print(dj_data_dict)
    return dj_data_dict
    # fa = open("C:/czg/602/project/Uav path planning/1.code/pycharm code/photo_to_gps1.0/INPUT/photo/DJI_0015.txt", "w", encoding='utf-8')
    # fa.write(data)

    # AbsoluteAltitude = dj_data_dict["AbsoluteAltitude"]
    # RelativeAltitude = dj_data_dict["RelativeAltitude"]
    # GpsLatitude = dj_data_dict["GpsLatitude"]
    # GpsLongtitude = dj_data_dict["GpsLongtitude"]
    # GimbalRollDegree = dj_data_dict["GimbalRollDegree"]
    # GimbalYawDegree = dj_data_dict["GimbalYawDegree"]
    # GimbalPitchDegree = dj_data_dict["GimbalPitchDegree"]
    # FlightRollDegree = dj_data_dict["FlightRollDegree"]
    # FlightYawDegree = dj_data_dict["FlightYawDegree"]
    # FlightPitchDegree = dj_data_dict["FlightPitchDegree"]
    # CalibratedOpticalCenterX = dj_data_dict["CalibratedOpticalCenterX"]
    # CalibratedOpticalCenterY = dj_data_dict["CalibratedOpticalCenterY"]
    # RtkFlag = dj_data_dict["RtkFlag"]
    # DewarpData = dj_data_dict["DewarpData"]
    # distortion_values = DewarpData.split(",")
    # CalibratedOpticalCenterX = CalibratedOpticalCenterX + distortion_values[2]
    # CalibratedOpticalCenterY = CalibratedOpticalCenterY + distortion_values[3]

    # distortion_value_k1 = distortion_values[4]
    # distortion_value_k2 = distortion_values[5]
    # distortion_value_k3 = distortion_values[6]
    # distortion_value_k4 = distortion_values[7]
    # distortion_value_k5 = distortion_values[8]
    # print(DewarpData)
    # print(distortion_values)
    # print(distortion_values[3])
    # return RelativeAltitude, GpsLatitude, GpsLongtitude, GimbalRollDegree, GimbalYawDegree, GimbalPitchDegree, \
    #        CalibratedOpticalCenterX, CalibratedOpticalCenterY, distortion_values
    # return dj_data_dict

def distortion():
    K = [[3704.21, 0, 2725.86],#(3707.68+3700.74)/2
         [0, 3704.21, 1824.42],#3685.352203
         [0, 0, 1]]
    K = np.asmatrix(K)
    distCoeffs = np.float32([-0.280892000000, 0.132348000000, 0.000916079000, -0.000695559000, -0.047167700000])
    path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'INPUT\photo_text')
    path1 = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'OUTPUT\photo_set')
    os.chdir(path)
    for image_name in os.listdir(os.getcwd()):
        print(image_name)
        img = cv2.imread(os.path.join(path, image_name))
        distortion_return = cv2.undistort(img, K, distCoeffs)
        cv2.imwrite(os.path.join(path1, image_name), distortion_return)

def get_photo_parameter(photo_dir):
    dj_data_dict = {}
    dj_data_dict = get_photo_data(photo_dir)
    return dj_data_dict["RelativeAltitude"], dj_data_dict["GpsLatitude"], dj_data_dict["GpsLongtitude"], \
           dj_data_dict["GimbalRollDegree"], dj_data_dict["GimbalYawDegree"], dj_data_dict["GimbalPitchDegree"]

# def get_photo_h(photo_dir):
#     h, b ,l, roll, yaw, pitch = get_photo_parameter(photo_dir)
#     return h

def get_photo_h():
    return dj_data_dict["RelativeAltitude"]

def get_photo_b():
    return dj_data_dict["GpsLatitude"]

def get_photo_l():
    return dj_data_dict["GpsLongtitude"]

def get_photo_roll():
    return dj_data_dict["GimbalRollDegree"]

def get_photo_yaw():
    return dj_data_dict["GimbalYawDegree"]

def get_photo_pitch():
    return dj_data_dict["GimbalPitchDegree"]