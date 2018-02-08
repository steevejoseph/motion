import cv2, pandas, time
from datetime import datetime

# print(cv2.__version__)
print("starting!")
time.sleep(3)

first_frame=None
status_list=[None, None]
times=[]
df=pandas.DataFrame(columns=["Start", "End"])

# if arg is a num:
#   VC() acesses camera[num]
# if num is a string, VC() looks for the file
video = cv2.VideoCapture(0)

while True:
    check, frame = video.read()
    status = 0
    # print(check)
    # print(frame)
    # print(video.isOpened())
    # print(video.read()) # (False, None)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray=cv2.GaussianBlur(gray, (21,21), 0)

    if first_frame is None:
        first_frame=gray
        continue


    delta_frame=cv2.absdiff(first_frame, gray)

    # more threshold methods in OpenCV docs
    thresh_frame=cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]

    # kernel array == sophistication (instead of None)
    # bigger iteration == more smoothness
    thresh_frame=cv2.dilate(thresh_frame, None, iterations=2)


    (_, cnts, _)=cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in cnts:
        # tweak the < value
        if cv2.contourArea(contour) < 5000:
            continue

        status=1
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0, 255, 0), 3)


    status_list.append(status)
    status_list = status_list[-2:]


    if status_list[-1]==1 and status_list[-2]==0:
        times.append(datetime.now())
    if status_list[-1]==0 and status_list[-2]==1:
        times.append(datetime.now())

    # if status_list[-1] != status_list[-2]:
        # times.append(datetime.now())


    cv2.imshow("Gray Frame", gray)
    cv2.imshow("Delta Frame", delta_frame)
    cv2.imshow("Threshold Frame", thresh_frame)
    cv2.imshow("Color Frame", frame)

    key = cv2.waitKey(1)

    if key == ord('q'):
        if status == 1:
            times.append(datetime.now())
        break

for i in range(0, len(times), 2):
    df=df.append({"Start":times[i], "End":times[i+1]},ignore_index=True)

# print(status_list)
df.to_csv("Times.csv")
video.release()
cv2.destroyAllWindows
