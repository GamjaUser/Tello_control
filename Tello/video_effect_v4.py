import sys
import traceback
import tellopy
import keyboard  # keyboard 모듈을 사용함
import time


def handler(event, sender, data, **args):
    drone = sender
    if event is drone.EVENT_FLIGHT_DATA:
        print(data)


def key_press_event(e):
    try:
        if e.name == "q":
            drone.land()
            drone.quit()
            return False  # 리스너 종료

        if e.name == "t":
            drone.takeoff()
        elif e.name == "l":
            drone.land()
        elif e.name == "w":
            drone.up(20)
        elif e.name == "s":
            drone.down(20)
        elif e.name == "a":
            drone.counter_clockwise(30)
        elif e.name == "d":
            drone.clockwise(30)
        elif e.name == "u":
            drone.forward(30)
        elif e.name == "j":
            drone.backward(30)
        elif e.name == "h":
            drone.left(30)
        elif e.name == "k":
            drone.right(30)
    except Exception as ex:
        print("Error in key_press_event:", ex)


def main():
    global drone
    drone = tellopy.Tello()

    try:
        drone.connect()
        drone.wait_for_connection(60.0)
        drone.subscribe(drone.EVENT_FLIGHT_DATA, handler)

        # keyboard 이벤트 리스너 등록
        keyboard.on_press(key_press_event)

        while True:
            time.sleep(0.1)  # 메인 스레드를 지속적으로 실행 상태로 유지
    except Exception as ex:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exception(exc_type, exc_value, exc_traceback)
        print(ex)
    finally:
        drone.quit()
        print("Program terminated")


if __name__ == "__main__":
    main()
