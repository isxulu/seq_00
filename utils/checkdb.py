import numpy as np
import cv2
import sqlite3
# Camera list with one line of data per camera:
#   CAMERA_ID, MODEL, WIDTH, HEIGHT, PARAMS[]
# Number of cameras: 3
'''
1 SIMPLE_PINHOLE 3072 2304 2559.81 1536 1152
2 PINHOLE 3072 2304 2560.56 2560.56 1536 1152
3 SIMPLE_RADIAL 3072 2304 2559.69 1536 1152 -0.0218531
'''

# 加载camera.npz文件
# camera_data = np.load('./imfunc4/cameras_hd.npz')


# # 加载图像
# image_path = "./imfunc4/image_hd/000001.png"
# image = cv2.imread(image_path)

# 获取图像宽度和高度
# height, width, _ = image.shape

# print("图像宽度：", width)
# print("图像高度：", height)
# # 获取图像宽度和高度
# width = camera_data['width']
# height = camera_data['height']

# print("图像宽度：", width)
# print("图像高度：", height)

# print(camera_data.files)


# 连接到.db文件
conn = sqlite3.connect('/data/xulu/datasets/seq_00/database.db')

# 创建游标对象
cursor = conn.cursor()

# 获取所有表名
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
# 打印表名
for table in tables:
    print(table[0])
'''
cameras
sqlite_sequence
images
keypoints
descriptors
matches
two_view_geometries
'''


# 执行SQL查询
cursor.execute('SELECT * FROM images')

# 获取查询结果
result = cursor.fetchall()

# 获取列名
column_names = [desc[0] for desc in cursor.description]
print(column_names)

# 遍历结果并打印数据
for row in result:
    print(row)

# 关闭数据库连接
conn.close()