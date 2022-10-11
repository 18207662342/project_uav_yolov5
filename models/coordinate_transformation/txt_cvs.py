import pandas as pd
def getdata(data_loc):
    width,height = 5472,3648    #5472*3648
    class_list = []
    x_min_list = []
    y_min_list = []
    x_max_list = []
    y_max_list = []
    x_center_list = []
    y_center_list = []
    with open(data_loc, "r") as f:
        for i in f.readlines():
            data_i = i.split(" ")
            class_i = str(data_i[0][0:])
            u_center_i = float(data_i[1][0:])
            v_center_i = float(data_i[2][0:])
            v_width_i = float(data_i[3][0:])
            u_height_i = float(data_i[4][0:])
            class_list.append(class_i)
            x_min_list.append(int((float(u_center_i) - 0.5 * float(v_width_i)) * width))
            y_min_list.append(int((float(v_center_i) - 0.5 * float(u_height_i)) * height))
            x_max_list.append(int((float(u_center_i) + 0.5 * float(v_width_i)) * width))
            y_max_list.append(int((float(v_center_i) + 0.5 * float(u_height_i)) * height))
            x_center_list.append(int((float(u_center_i))*width))
            y_center_list.append(int((float(v_center_i))*height))
        # print(len(class_list))
    return  x_center_list, y_center_list

# data_loc = r"C:\czg\602\project\Uav path planning\1.code\pycharm code\photo_to_gps1.0\OUTPUT\labels\DJI_0014.txt"
# x_center_list, y_center_list = getdata(data_loc)
# list = [x_center_list, y_center_list]
# df_eval = pd.DataFrame(data=list)
# df_result = pd.DataFrame(df_eval.values.T, columns=["x_center_list", "y_center_list"])
# df_result.to_csv('C:/czg/602/project/Uav path planning/1.code/pycharm code/photo_to_gps1.0/OUTPUT/DATA.csv', encoding='gbk')
#
