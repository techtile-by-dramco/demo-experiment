import RPi.GPIO as GPIO
import time
import argparse

def main():
    parser = argparse.ArgumentParser(description="Toggle a GPIO pin")
    parser.add_argument("pin", type=int, help="GPIO pin number (BCM)")
    parser.add_argument("count", type=int, help="Number of toggle cycles")
    parser.add_argument("--delay", type=float, default=1.0, help="Delay in seconds (default: 1.0)")
    
    args = parser.parse_args()

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(args.pin, GPIO.OUT)

    try:
        for i in range(args.count):
            GPIO.output(args.pin, GPIO.HIGH)
            print(f"[{i+1}] ON")
            time.sleep(args.delay)

            GPIO.output(args.pin, GPIO.LOW)
            print(f"[{i+1}] OFF")
            time.sleep(args.delay)

    except KeyboardInterrupt:
        print("Interrupted")

    finally:
        GPIO.cleanup()


if __name__ == "__main__":
    main()