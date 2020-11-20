import cv2


def _show_pyramid(pyr):
    # Code that shows the pyramid
    for i in range(4):
        cv2.imshow(f"level {i} of the pyramid", pyr[i])
    cv2.waitKey(0)
    cv2.destroyAllWindows()