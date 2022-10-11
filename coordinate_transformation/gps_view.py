import folium
import os

def draw_gps(html_data_dir, locations, color1,color2):
    """
    绘制gps轨迹图
    :param locations: list, 需要绘制轨迹的经纬度信息，格式为[[lat1, lon1], [lat2, lon2], ...]
    :param output_path: str, 轨迹图保存路径
    :param file_name: str, 轨迹图保存文件名
    :return: None
    """
    # m1 = folium.Map(locations[0], zoom_start=35, attr='default')  # 中心区域的确定
    m1 = folium.Map(
        # location=[38.96, 117.78],
        locations[0],
        zoom_start=12,
        # tiles='http://webrd02.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=7&x={x}&y={y}&z={z}', # 高德街道图
        # tiles='http://webst02.is.autonavi.com/appmaptile?style=6&x={x}&y={y}&z={z}', # 高德卫星图
        tiles='https://mt.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',  # google 卫星图
        # tiles='https://mt.google.com/vt/lyrs=h&x={x}&y={y}&z={z}', # google 地图
        attr='default'
    )
    folium.PolyLine(  # polyline方法为将坐标用线段形式连接起来
        locations,  # 将坐标点连接起来
        weight=1,  # 线的大小为3
        color=color1,  # 线的颜色为橙色
        opacity=0.8  # 线的透明度0.8
    ).add_to(m1)  # 将这条线添加到刚才的区域m内
    # 起始点，结束点
    # folium.Marker(locations[0], popup='<b>Starting Point</b>').add_to(m1)
    m1.save(html_data_dir)  # 将结果以HTML形式保存到指定路径


# locations = [[23.16238986, 113.34031269],[23.162622, 113.339846],[23.162130, 113.339805],[23.162132, 113.339671],[23.162279, 113.339673]]
#

# draw_gps(locations, 'red','orange')

