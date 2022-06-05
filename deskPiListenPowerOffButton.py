import serial
import sys
import time
import os
import signal
import logging

SERIAL_PORT = "/dev/ttyUSB0"
BAUD_RATE = 9600

shutdownCompleted = False

# ----------------------------
def shutdown(signum = None, frame = None):
    logging.info(f"A system shutdown is on-going")
    shutdownCompleted = True

# ----------------------------
def main():

    # Setup logging.
    logging.basicConfig(filename=f"DeskPi-ListenPowerOffButton.log", level=logging.DEBUG, format="%(asctime)s %(levelname)s [%(name)s] %(message)s")

    logging.info("Running DeskPi listen power off button service...")

    # Register signal handler.
    for sig in [signal.SIGTERM]: # , signal.SIGHUP, signal.SIGQUIT
        logging.debug(f"Registering signal {sig}...")
        signal.signal(sig, shutdown)
        logging.debug(f"Signal {sig} registered successfully")

    logging.info("Listening for power off button to be pressed...")
    with serial.Serial(SERIAL_PORT,BAUD_RATE,timeout=1) as ser:

        while True:
            data = ser.read(1)
            data += ser.read(ser.in_waiting)
            state = data.decode("ascii")
            if len(state) > 0:
                logging.info(f"DeskPi state='{state}'")
                if state == "poweroff":
                    logging.info("The power off button has been pressed. Shuttting down the system...")
                    os.system("sudo shutdown --poweroff") 
                    break

    while not shutdownCompleted:
        logging.info("Waiting for the system to shut down...")
        time.sleep(5)

    logging.info("DeskPi listen power off button service stopped successfully")

    logging.shutdown()
    sys.exit(0)

# ----------------------------
if __name__ == '__main__':
    sys.exit(main())
