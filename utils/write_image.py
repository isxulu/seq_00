# Image list with two lines of data per image:
#   IMAGE_ID, QW, QX, QY, QZ, TX, TY, TZ, CAMERA_ID, NAME
#   POINTS2D[] as (X, Y, POINT3D_ID)
# Number of images: 2, mean observations per image: 2
'''
1 0.851773 0.0165051 0.503764 -0.142941 -0.737434 1.02973 3.74354 1 P1180141.JPG
2362.39 248.498 58396 1784.7 268.254 59027 1784.7 268.254 -1
2 0.851773 0.0165051 0.503764 -0.142941 -0.737434 1.02973 3.74354 1 P1180142.JPG
1190.83 663.957 23056 1258.77 640.354 59070
'''
###########################################################################################################
# 因为特征提取生成的 database 中图片的次序并不规则，则需先生成 databse，再根据其次序生成 images.txt                 #
# colmap request: Each image in images.txt must have the same image_id (first column) as in the database  #
###########################################################################################################
import numpy as np
import os
import sqlite3
import json

def get_extrs():
# 连接到.db文件
    conn = sqlite3.connect('/data/xulu/datasets/seq_00/database.db')

    # 创建游标对象
    cursor = conn.cursor()

    # # 获取所有表名
    # cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    # tables = cursor.fetchall()
    '''
    cameras
    sqlite_sequence
    images
    keypoints
    descriptors
    matches
    two_view_geometries
    '''
    # # 打印表名
    # for table in tables:
    #     print(table[0])

    # 执行SQL查询
    cursor.execute('SELECT * FROM images')
    # 获取查询结果
    result = cursor.fetchall()
    # # 遍历结果并打印数据
    # for row in result:
    #     print(row)
    # 关闭数据库连接
    conn.close()

    extrinsic_matrixs = []
    output_lines = []
    for row in result:
        image_name = row[1]
        image_id = row[0]   # idx from 1 same with database.db not 0 
        json_path = '/data/xulu/datasets/seq_00/images/meta_data.json'
        with open(json_path, 'r') as file:
            json_data = json.load(file)

        c2w = []
        for frame in json_data["frames"]:
            if frame["rgb_path"] == image_name:
                c2w = frame["camtoworld"]
                break
        c2w = np.array(c2w)
        # c2w[:, 1:3] = -c2w[:, 1:3]  # opengl -> opencv
        extrinsic_matrix = np.linalg.inv(c2w)
        # print(extrinsic_matrix)
        extrinsic_matrixs.append(extrinsic_matrix)
        # 提取旋转部分（3x3矩阵）
        rotation_matrix = extrinsic_matrix[:3, :3]

        # 计算旋转矩阵的四元数表示
        qw = np.sqrt(1 + np.trace(rotation_matrix)) / 2
        qx = (rotation_matrix[2, 1] - rotation_matrix[1, 2]) / (4 * qw)
        qy = (rotation_matrix[0, 2] - rotation_matrix[2, 0]) / (4 * qw)
        qz = (rotation_matrix[1, 0] - rotation_matrix[0, 1]) / (4 * qw)
        
        # 提取平移部分
        translation_vector = extrinsic_matrix[:3, 3]
        tx = translation_vector[0]
        ty = translation_vector[1]
        tz = translation_vector[2]

        # > output.file
        camera_id = image_id

        output_line = f"{image_id} {qw} {qx} {qy} {qz} {tx} {ty} {tz} {camera_id} {image_name}"
        output_lines.append(output_line)

    # 将结果隔行写入image.txt文件
    with open('./sparse_model/images.txt', 'w') as f:
        for line in output_lines:
            f.write(line + '\n\n')
    return extrinsic_matrixs