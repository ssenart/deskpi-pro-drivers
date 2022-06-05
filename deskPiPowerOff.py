import serial
import sys
import logging


SERIAL_PORT = "/dev/ttyUSB0"
BAUD_RATE = 9600

# ----------------------------
def powerOffDeskPi():

    logging.info("A system shutdown is on-going, power off the DeskPi mainboard")

    with serial.Serial(SERIAL_PORT,BAUD_RATE, timeout=30) as ser:
        ser.write(b'power_off')

# ----------------------------
def main():

    # Setup logging.
    logging.basicConfig(filename=f"DeskPi-PowerOff.log", level=logging.DEBUG, format="%(asctime)s %(levelname)s [%(name)s] %(message)s")

    # Send the power off command to the DeskPi mainboard.
    powerOffDeskPi()

# ----------------------------
if __name__ == '__main__':
    sys.exit(main())
