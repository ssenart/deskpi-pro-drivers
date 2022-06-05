import serial
import sys
import logging
import subprocess
import time


SERIAL_PORT = "/dev/ttyUSB0"
BAUD_RATE = 9600

# ----------------------------
def readCPUTemperature() -> float:

    cpuTemp = subprocess.getoutput('vcgencmd measure_temp|awk -F\'=\' \'{print $2\'}')
    res = float(cpuTemp.split('\'')[0])

    return res

# ----------------------------
def computeFanCommand(cpuTemperature: float) -> str:

    if cpuTemperature <= 50:
        res = "pwm_000"
    # elif cpuTemperature > 50 and cpuTemperature <= 50:
    #     res = "pwm_025"
    elif cpuTemperature > 50 and cpuTemperature <= 65:
        res = "pwm_050"
    elif cpuTemperature > 65 and cpuTemperature <= 75:
        res = "pwm_075"
    elif cpuTemperature > 75:
        res = "pwm_100"

    return res

# ----------------------------
def controlFanSpeed(fanCommand: str):

    logging.info(f"Fan command = {fanCommand}")

    with serial.Serial(SERIAL_PORT,BAUD_RATE, timeout=30) as ser:
        ser.write(fanCommand.encode("ascii"))

# ----------------------------
def main():

    # Setup logging.
    logging.basicConfig(filename=f"DeskPi-FanSpeedController.log", level=logging.DEBUG, format="%(asctime)s %(levelname)s [%(name)s] %(message)s")

    logging.info("Running DeskPi fan speed controller service...")

    lastFanCommand = None

    try: 

        while True:
            # Read the CPU temperature.
            cpuTemperature = readCPUTemperature()

            # Get the corresponding fan command.
            fanCommand = computeFanCommand(cpuTemperature)

            if fanCommand != lastFanCommand:

                logging.info(f"CPU temperature = {cpuTemperature}°C")

                # Control the fan speed.
                controlFanSpeed(fanCommand)

                lastFanCommand = fanCommand

            # Sleep for 10s before next reading.
            time.sleep(10)

    except KeyboardInterrupt:
        controlFanSpeed("pwm_000")          

        logging.info("DeskPi fan speed controller service stopped successfully")

# ----------------------------
if __name__ == '__main__':
    sys.exit(main())
