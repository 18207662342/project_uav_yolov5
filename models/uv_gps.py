from coordinate_transformation import images_processing as ip
import coordinate_transformation.coordinate_transformation as ct
import os
from PIL import Image
import cv2
import coordinate_transformation.gps_view as gps


if __name__ == '__main__':
    ip.distortion()#去畸变，同一台无人机相机，畸变参数不用更改
    #yolov5--txt uv坐标文件
    txt_data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'OUTPUT\labels')
    jpg_data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'INPUT\photo_text')
    cvs_data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'OUTPUT\gps_cvs')
    jpg_data_dir_distortion = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'OUTPUT\photo_set')
    html_data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'OUTPUT\gps_html')
    # print(cvs_data_dir)
    os.chdir(jpg_data_dir)
    all_gps = []
    for image_name in os.listdir(os.getcwd()):
        # print(image_name)
        camera_intrinsic, r, t = ct.photo_parameter(os.path.join(jpg_data_dir, image_name))
        img_points = ct.get_rice_objection(os.path.join(jpg_data_dir_distortion, image_name), os.path.join(txt_data_dir, image_name[:len(image_name)-4])+'.txt')
        result = ct.pixel_to_world(camera_intrinsic, r, t, img_points)
        all_gps += ct.gauss_projection(os.path.join(cvs_data_dir, image_name[:len(image_name)-4]+'.csv'), result)
    gps.draw_gps(os.path.join(html_data_dir, image_name[:len(image_name)-4]+'.HTML'), all_gps, 'red', 'orange')
    os.chdir(cvs_data_dir)
    for csv_name in os.listdir(os.getcwd()):
        print(csv_name)
