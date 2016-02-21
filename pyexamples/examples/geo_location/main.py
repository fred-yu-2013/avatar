# -*- coding: utf-8 -*-

from geopy.geocoders import Nominatim
from geopy.distance import vincenty

# # 获取地址
#
# geolocator = Nominatim()
# location = geolocator.geocode("175 5th Avenue NYC")
#
# print(location.address)
#
# # geolocator2 = Nominatim()
# # location2 = geolocator.geocode("121.598695, 31.266828")
# #
# # print location2.address

# # 获取坐标间的距离
#
# newport_ri = (41.49008, -71.312796)
# cleveland_oh = (41.499498, -81.695391)
# print(vincenty(newport_ri, cleveland_oh).miles)

# 200米

# 50 m: x + 0.0005 or y + 0.001, 单个变化
location = (121.598695, 31.266828)
location2 = (121.5987, 31.26684)
print(vincenty(location, location2).m)