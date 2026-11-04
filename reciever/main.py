# Local Libraries
from lib.servo import Servo
from lib.config import Config

# Micropython Libraries
import network
import socket
import utime
import json

def extend_servo(servo: Servo) -> None: 
    """
    Rotates the servo to the extended position.
    """
    servo.write(Config.SERVO_CONFIG["SERVO_EXTENDED_DEG"])

def retract_servo(servo: Servo) -> None:
    """
    Rotates the servo to the retracted position.
    """
    servo.write(Config.SERVO_CONFIG["SERVO_RETRACTED_DEG"])

def toggle_servo(servo: Servo) -> None:
    """
    Checks if the servo is already extended. Extends then retracts the servo.
    """
    if (get_servo_extended(servo)):
        retract_servo(servo)
        utime.sleep(0.5)
    extend_servo(servo)
    utime.sleep(2)
    retract_servo(servo)


def get_servo_extended(servo: Servo) -> bool:
    # If the servo is within 20 degrees of the extended position returns true
    if (abs(servo.read() - Config.SERVO_CONFIG["SERVO_EXTENDED_DEG"]) < 20):
        return True
    return False

def main():
    # Create Servo with config
    switchServo = Servo(pin_id=Config.SERVO_CONFIG["MOTOR_PIN"], min_deg=Config.SERVO_CONFIG["MIN_DEG"], max_deg=Config.SERVO_CONFIG["MAX_DEG"])
    print(f"Created Servo on pin {Config.SERVO_CONFIG['MOTOR_PIN']}")

    # Create wifi network
    ap = network.WLAN(network.WLAN.IF_AP)
    ap.active(True)
    ap.config(ssid=Config.NETWORK_CONFIG["SSID"], password=Config.NETWORK_CONFIG["PASSWORD"], authmode=3)
    while not ap.active():
        pass

    print(f"Created WIFI network: {Config.NETWORK_CONFIG['SSID']}")
    print(f"Network Info {ap.ifconfig()}")

    # Reset servo position to retracted state
    retract_servo(switchServo)

    # Create Webserver
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.listen()

    print('Listening on', addr)

    while True:
        conn = None
        try:
            conn, addr = s.accept()
            print('Got a connection from', addr)
            
            # Receive and parse the request
            request = conn.recv(1024)
            request = str(request)
            print('Request content = %s' % request)

            try:
                request = request.split()[1]
                print('Request:', request)
            except IndexError:
                pass

            response = {
                "message": "ok"
            }

            try:
                match request:
                    case "/toggle?":
                        toggle_servo(switchServo)
                    case "/get_extended?":
                        response = {
                            "message": get_servo_extended(switchServo)
                        }
            except Exception as e:
                response = {
                    "message": f"uh oh: {repr(e)}"
                }

            conn.send('HTTP/1.0 200 OK\r\nContent-type: application/json\r\n\r\n')
            conn.send(json.dumps(response))
            conn.close()
            
        except OSError as e:
            conn.close()
            print('Connection closed')


if __name__ == "__main__":
    main()
