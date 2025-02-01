import sys
import traceback
import tellopy
import av
import cv2
import numpy
import time


def handler(event, sender, data, **args):
    drone = sender
    if event is drone.EVENT_FLIGHT_DATA:
        print(data)


def main():
    drone = tellopy.Tello()

    try:
        drone.connect()
        drone.wait_for_connection(60.0)
        drone.subscribe(drone.EVENT_FLIGHT_DATA, handler)

        retry = 3
        container = None
        while container is None and 0 < retry:
            retry -= 1
            try:
                container = av.open(drone.get_video_stream())
            except av.AVError as ave:
                print(ave)
                print("retry...")

        # skip first 300 frames
        frame_skip = 300
        while True:
            for frame in container.decode(video=0):
                if 0 < frame_skip:
                    frame_skip = frame_skip - 1
                    continue
                start_time = time.time()
                image = cv2.cvtColor(numpy.array(frame.to_image()), cv2.COLOR_RGB2BGR)
                cv2.imshow("Original", image)
                cv2.imshow("Canny", cv2.Canny(image, 100, 200))

                # 키보드 입력 처리
                key = cv2.waitKey(1) & 0xFF
                if key == ord("t"):  # 't' 키로 이륙
                    drone.takeoff()
                elif key == ord("l"):  # 'l' 키로 착륙
                    drone.land()
                elif key == 27:  # ESC 키로 종료
                    break

                if frame.time_base < 1.0 / 60:
                    time_base = 1.0 / 60
                else:
                    time_base = frame.time_base
                frame_skip = int((time.time() - start_time) / time_base)

    except Exception as ex:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exception(exc_type, exc_value, exc_traceback)
        print(ex)
    finally:
        drone.quit()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
