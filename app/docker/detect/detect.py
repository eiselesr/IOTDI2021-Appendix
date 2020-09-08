from yolo_sort import *
import time

min_num_frames_for_id = 5
save_loc = "/input"

yolo = yolo_py_consumer()
yolo.start()

outs = []
for frame_num, file in enumerate(os.listdir(save_loc)):

    start = time.time()

    res = yolo.file_consume(str(save_loc) + "/"+str(frame_num) + '.jpg', frame_num)

    for item in res:
        outs.append(item)

    print('total yolo time: {}'.format(time.time() - start))