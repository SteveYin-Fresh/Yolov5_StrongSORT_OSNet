import pandas as pd
import cv2
import time


#https://stackoverflow.com/questions/8044539/listing-available-devices-in-python-opencv
def returnCameraIndexes():
    # checks the first 10 indexes.
    index = 0
    arr = []
    i = 10
    while i > 0:
        cap = cv2.VideoCapture(index)
        if cap.read()[0]:
            arr.append(index)
            cap.release()
        index += 1
        i -= 1
    return arr

#https://stackoverflow.com/questions/30577042/resolution-list-opencv-python-camera
def change_resolution(camid, w, h):

   num_frame = 0
   cap = cv2.VideoCapture(camid)
   size = cap.get(cv2.CAP_PROP_FRAME_WIDTH), cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
   size_new = cap.set(cv2.CAP_PROP_FRAME_WIDTH, w),cap.set(cv2.CAP_PROP_FRAME_HEIGHT, h)
   #print(size)

   start = time.time()
   while(True):
       ret, frame = cap.read()
       if num_frame < 60:
           num_frame = num_frame + 1
           time.sleep(0.001)
       else:
           break

   total_time = (time.time() - start)
   fps = (num_frame / total_time)
   print(str(num_frame) + ' Frames for ' +  str(round(total_time,6)) + 's, frame rate = ' + str(round(fps,2)) + ' fps' + ' for (' + str(w) + ', ' + str(h) + ')')

   cap.release()
   cv2.destroyAllWindows()


if __name__ == "__main__":
    cams = returnCameraIndexes() 
    print('Find ' + str(len(cams)) + ' cameras: ' + str(cams))

    #resolution = [(320,480),(640,480),(704,680),(960,680),(1280,720),(1440,720),(1920,1080)]
    resolution = [(640,480),(1280,720),(1920,1080)]
    for camid in cams:
        print('---For camera ' + str(camid) + '---')
        for reso in resolution:
            change_resolution(camid, reso[0], reso[1])

    cam_id = int(input("Please choose cam id in " + str(cams) + ":\n"))
    reso_id = int(input("Please choose resolution id in " + str(resolution) + ":\n"))
    (width, height) = resolution[reso_id]

    cap = cv2.VideoCapture(cam_id)
    size = cap.get(cv2.CAP_PROP_FRAME_WIDTH), cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    size_new = cap.set(cv2.CAP_PROP_FRAME_WIDTH, width),cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    #cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
    print('---Starting camera ' + str(cam_id) + ' at (' + str(width) + ', ' + str(height) + ')---')
    start = time.time()
    num_frame = 0
    while(cap.isOpened()):
        # cap the video frame by frame
        ret, frame = cap.read()
        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break

        # Display the resulting frame
        cv2.imshow('frame', frame)
        num_frame += 1

        # the 'q' button is set as the quitting button
        if cv2.waitKey(1) == ord('q'):
            break

    total_time = (time.time() - start)
    fps = (num_frame / total_time)
    print(str(num_frame) + ' Frames for ' +  str(round(total_time,6)) + 's, frame rate = ' + str(round(fps,2)) + ' fps' + ' for (' + str(width) + ', ' + str(height) + ')')

    # After the loop release the cap object, destroy window
    cap.release()
    cv2.destroyAllWindows()


'''
    url = "https://en.wikipedia.org/wiki/List_of_common_resolutions"
    table = pd.read_html(url)[0]            #pip install lxml to enable this pd read_html line
    table.columns = table.columns.droplevel()
    cap = cv2.Videocap(0)
    resolutions = {}
    for index, row in table[["W", "H"]].iterrows():
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, row["W"])
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, row["H"])
        width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        resolutions[str(width)+"x"+str(height)] = "OK"
    print(resolutions)
'''
