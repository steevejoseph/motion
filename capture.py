import cv2, time

DEBUG = False

# if arg is a num:
#   VC() acesses camera[num]
# if num is a string:
#   VC() looks for the file
video = cv2.VideoCapture(0)

frames = 1
while True:

    a += 1
    check, frame = video.read()

    if DEBUG:
        print(cv2.__version__)
        print(check)
        print(frame)
        print(video.isOpened())
        print(video.read()) # (False, None)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # time.sleep(3)

    cv2.imshow("Capturing", frame)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break

print(frames)
cv2.destroyAllWindows()
video.release()
