import numpy as np
import txt_cvs as tc
import Gauss_projection as gapro
# import gps_view as draw_gps
import images_processing as ip
import cv2
import matplotlib.pyplot as plt
import pandas as pd

camera_parameter = {
    # f/dx, f/dy
    "f": [3704.21, -3704.21],
    # 相机中心坐标点
    "c": [2736 - 10.14, 1824 + 0.42],
}

def pixel_to_world(camera_intrinsics, r, t, img_points):
    K_inv = camera_intrinsics.I
    R_inv = np.asmatrix(r).I
    world_points = []
    scale_world_all = []
    coords = np.zeros((3, 1), dtype=np.float64)
    for img_point in img_points:
        coords[0] = img_point[0]
        coords[1] = img_point[1]
        coords[2] = 1.0
        cam_point = np.dot(K_inv, coords)
        cam_R_inv = np.dot(R_inv, cam_point)

        # scale = camera_parameter["h"]
        scale = t[2]
        scale_world = np.multiply(scale, cam_R_inv)
        scale_world_all.append(scale_world)
        world_point = np.asmatrix(scale_world) + np.asmatrix(t)
        pt = np.zeros((3, 1), dtype=np.float64)
        pt[0] = world_point[0]
        pt[1] = world_point[1]
        pt[2] = t[2]
        world_points.append(pt.T.tolist())

    scale_world_x = []
    scale_world_y = []
    for i , j in enumerate(scale_world_all):
        scale_world_x.append(j[0])
        scale_world_y.append(j[1])

    # 画坐标散点图
    # fig = plt.figure()
    # # 将画图窗口分成1行1列，选择第一块区域作子图
    # ax1 = fig.add_subplot(1, 1, 1)
    # ax1.set_title('Result Analysis')
    # ax1.set_xlabel('scale_world_x')
    # ax1.set_ylabel('scale_world_y')
    # ax1.scatter(scale_world_x, scale_world_y, c='r', marker='.')
    # # 画直线图
    # # ax1.plot(x2, y2, c='b', ls='--')
    # plt.xlim(xmax=8, xmin=-8)
    # plt.ylim(ymax=6, ymin=-6)
    # plt.legend('rice')
    # plt.show()

    return world_points

# if __name__ == '__main__':
#     txt_data_dir = "C:/czg/602/project/Uav path planning/1.code/pycharm code/photo_to_gps1.0/OUTPUT/labels/100_0093_0007.txt"
#     jpg_data_dir = 'C:/czg/602/project/Uav path planning/1.code/pycharm code/photo_to_gps1.0/INPUT/photo_text/100_0093_0007.JPG'
#     cvs_data_dir = 'C:/czg/602/project/Uav path planning/1.code/pycharm code/photo_to_gps1.0/OUTPUT/gps.csv'

def photo_parameter(jpg_data_dir):
    #获取图片参数h，经度纬度，roll,yaw,pitch
    photo_h, photo_b, photo_l, photo_roll, photo_yaw, photo_pitch = ip.get_photo_parameter(jpg_data_dir)
    # print('photo_dir', photo_dir)
    print(float(photo_h[2:len(photo_h)-1]), float(photo_b[1:len(photo_b)-1]),
          float(photo_l[1:len(photo_l)-1]), float(photo_roll[1:len(photo_roll)-1]),
          float(photo_yaw[1:len(photo_yaw)-1]), float(photo_pitch[1:len(photo_pitch)-1]))
    photo_h = float(photo_h[2:len(photo_h)-1])
    photo_b = float(photo_b[1:len(photo_b) - 1])
    photo_l = float(photo_l[1:len(photo_l) - 1])
    photo_x, photo_y = gapro.geodetic_to_plane(photo_b, photo_l)
    photo_roll = float(photo_roll[1:len(photo_roll) - 1])/180*np.pi
    photo_yaw = float(photo_yaw[1:len(photo_yaw) - 1])/-180*np.pi
    photo_pitch = (float(photo_pitch[1:len(photo_pitch) - 1])+90)/180*np.pi

    #相机内参赋值
    f = camera_parameter["f"]
    c = camera_parameter["c"]
    camera_intrinsic = np.mat(np.zeros((3, 3), dtype=np.float64))
    camera_intrinsic[0, 0] = f[0]
    camera_intrinsic[1, 1] = f[1]
    camera_intrinsic[0, 2] = c[0]
    camera_intrinsic[1, 2] = c[1]
    camera_intrinsic[2, 2] = np.float64(1)

    #外参赋值
    x_r_matrix = [[1, 0, 0],
                  [0, np.cos(photo_roll), -np.sin(photo_roll)],
                  [0, np.sin(photo_roll), np.cos(photo_roll)]]
    y_r_matrix = [[np.cos(photo_pitch), 0, np.sin(photo_pitch)],
                  [0, 1, 0],
                  [-np.sin(photo_pitch), 0, np.cos(photo_pitch)]]
    z_r_matrix = [[np.cos(photo_yaw), np.sin(photo_yaw), 0],
                  [-np.sin(photo_yaw), np.cos(photo_yaw), 0],
                  [0, 0, 1]]
    r_matrix = np.dot(x_r_matrix, y_r_matrix)
    r_matrix = np.dot(r_matrix, z_r_matrix)
    r = r_matrix
    t = np.asmatrix([photo_y, photo_x, photo_h]).T
    return camera_intrinsic, r, t

def get_rice_objection(jpg_data_dir, txt_data_dir):
    #打开txt文件，获取秧苗位置点
    x_center_list, y_center_list = tc.getdata(txt_data_dir)
    # 质心显示在图片上
    # img = cv2.imread(jpg_data_dir)
    # for i in range(1,len(x_center_list)):
    #     cv2.circle(img, (x_center_list[i], y_center_list[i]), 10, (0, 0, 255), -1)
    # cv2.namedWindow('img', cv2.WINDOW_NORMAL)
    # cv2.imshow('img', img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # 平面坐标转换 uv-xyz
    img_points = [x_center_list, y_center_list]
    img_points = np.asmatrix(img_points).T
    img_points = np.array(img_points)
    return img_points

# result = pixel_to_world(camera_intrinsic, r, t, img_points)

def gauss_projection(cvs_data_dir, result):
    # 高斯投影xy-bl
    gps_coordinate_list = []
    for i, coo in enumerate(result):
        coo_x = coo[0][0]
        coo_y = coo[0][1]
        coo_z = coo[0][2]
        gps_coordinate = gapro.plane_to_geodetic(coo_x, coo_y)
        gps_coordinate_list.append(gps_coordinate)
    #保存gps坐标位置
    df_eval = pd.DataFrame(data=gps_coordinate_list)
    df_result = pd.DataFrame(df_eval.values, columns=["latitude", "longitude"])
    df_result.to_csv(cvs_data_dir, encoding='gbk')
    print('Gauss projection successful')
    return gps_coordinate_list
    #在Google地图上显示坐标点
    # draw_gps(gps_coordinate_list, 'red', 'orange')

