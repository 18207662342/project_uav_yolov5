import images_processing as ip
import detect as yo
import coordinate_transformation as ct
import os
from PIL import Image
import cv2
import gps_view as gps

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

if __name__ == '__main__':
    jpg_data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'INPUT/photo1')  # 提取照片信息,      #输入
    jpg_data_dir_distortion = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data/images_false_rice')#去畸变后图片保存位置
    txt_data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'runs/detect/exp25/labels')#提取秧苗位置信息   #位置更改
    cvs_data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'OUTPUT/gps_cvs')#保存秧苗gps坐标信息
    html_data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'OUTPUT/gps_html')

    # ip.distortion(jpg_data_dir, jpg_data_dir_distortion)  # 去畸变，同一台无人机相机，畸变参数不用更改

    # yo.yolov5_detect()

    # yolov5--txt uv坐标文件
    os.chdir(jpg_data_dir)
    all_gps = []
    for image_name in os.listdir(os.getcwd()):
        # print(image_name)
        camera_intrinsic, r, t = ct.photo_parameter(os.path.join(jpg_data_dir, image_name))
        img_points = ct.get_rice_objection(os.path.join(jpg_data_dir_distortion, image_name), os.path.join(txt_data_dir, image_name[:len(image_name)-4])+'.txt')
        result = ct.pixel_to_world(camera_intrinsic, r, t, img_points)
        all_gps += ct.gauss_projection(os.path.join(cvs_data_dir, image_name[:len(image_name)-4]+'.csv'), result)
    gps.draw_gps(os.path.join(html_data_dir, image_name[:len(image_name)-4]+'.HTML'), all_gps, 'red', 'orange')

    scale_world_x = []
    scale_world_y = []
    for i in all_gps:
        scale_world_x.append(i[0])
        scale_world_y.append(i[1])

    # 画坐标散点图
    fig = plt.figure()
    # 将画图窗口分成1行1列，选择第一块区域作子图
    ax1 = fig.add_subplot(1, 1, 1)
    ax1.set_title('Result Analysis')
    ax1.set_xlabel('scale_world_x')
    ax1.set_ylabel('scale_world_y')
    ax1.scatter(scale_world_x, scale_world_y, c='r', marker='.')
    # 画直线图
    # ax1.plot(x2, y2, c='b', ls='--')
    # plt.xlim(xmax=8, xmin=-8)
    # plt.ylim(ymax=6, ymin=-6)
    plt.legend('rice')
    plt.savefig(os.path.join(os.path.dirname(txt_data_dir), 'result'), bbox_inches='tight', pad_inches=0, dpi=600)

    plt.show()

    # os.chdir(cvs_data_dir)
    # for csv_name in os.listdir(os.getcwd()):
    #     print(csv_name)
