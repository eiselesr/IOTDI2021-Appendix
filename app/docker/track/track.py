import time
from sort import *


##############################
# tracking


outs = np.array(outs)

print('starting tracking')

mot_tracker = Sort(max_age=50, min_hits=15)

res = {}
i = 0


for frame_num in range(int(outs[:, 0].max()) + 1):


    start_time = time.time()
    dets = outs[outs[:, 0] == frame_num, 1:6]

    trackers = mot_tracker.update(dets)

    for d in trackers:
        _id = d[4]
        if _id in res:
            res[_id] = res[_id] + 1
        else:
            res[_id] = 1


total_count = 0
for key, value in res.items():
    print(value)
    if value >= min_num_frames_for_id:
        total_count = total_count + 1

print()
print('total number of vehicles seen:')
print(total_count)
print('------------------')

