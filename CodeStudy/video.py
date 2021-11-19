import cv2

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

while True:
    success, img = cap.read()
    cv2.imshow("img", img)
    if cv2.waitKey(1) == ord("q"):
        break
    if not cv2.getWindowProperty("img", cv2.WND_PROP_VISIBLE):
        break

cap.release()
cv2.destroyAllWindows()
