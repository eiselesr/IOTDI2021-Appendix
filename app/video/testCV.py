import cv2
vidcap = cv2.VideoCapture('video.mp4')
success,image = vidcap.read()
# print(image)
print(type(image))
count = 0
# while success:
#       cv2.imwrite("output/%d.jpg" % count, image)     # save frame as JPEG file
#       success,image = vidcap.read()
#       print('Read a new frame: ', success)
#       count += 1
