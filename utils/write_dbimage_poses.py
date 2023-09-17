import argparse
import numpy as np
import sys
sys.path.append('.')
import database

def main():
    parser = argparse.ArgumentParser(description='modify colmap database images table')
    parser.add_argument('--db_path', type=str, required=True)
    parser.add_argument('--imagestxt_path', type=str, required=True)   # records of camera models
    args = parser.parse_args()

    # open the database that we are going to modify
    db = database.COLMAPDatabase.connect(args.db_path)

    # modify the database
    ids, image_names, cam_ids, prior_qs, prior_ts = [], [], [], [], []
    with open(args.imagestxt_path, 'r') as file:
        lines = file.readlines()
        # print(lines)
        # 1 0.9924259418213532 -0.014906502718832594 0.1218085853118103 -0.005598082704089651 -191.02 3.28832 22.5401 1 000000.png
        for i in range(0, len(lines), 2):
            l = lines[i].split(' ')
            image_name = l[-1][:-1]
            cam_id = int(image_name.split('.')[0]) + 1
            id = int(l[0])          # database id
            prior_q, prior_t = np.array([np.float64(x) for x in l[1:5]]).astype(np.float64), np.array([np.float64(x) for x in l[5:8]]).astype(np.float64)
            # param = np.array([np.float64(x) for x in camera_line[-4:]]).astype(np.float64)
            ids.append(id), image_names.append(image_name), cam_ids.append(cam_id), prior_qs.append(prior_q), prior_ts.append(prior_t)
            db.update_image(image_name, cam_id, prior_q, prior_t, id)
    
    # commit the changes
    db.commit()
  
    # close the database
    db.close()

if __name__ == '__main__':

    main()
