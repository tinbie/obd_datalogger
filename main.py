#py2.7 utf8

import obd
import sys
from datetime import datetime
import string
from obd import OBDStatus
from time import sleep

commands = ['RPM', 'INTAKE_PRESSURE', 'ENGINE_LOAD', 'TIMING_ADVANCE', 'THROTTLE_POS']  # requested commands
values = []                             # holding responses


if __name__ == "__main__":

    # get duration of logging
    if len(sys.argv) > 1:
        logging_duration = sys.argv[1]
    else:
        logging_duration = 120

    print "####################################"
    print "OBD DATALOGGER - connecting..."
    print "####################################"

    # open instances
    obd_logger = obd.OBD()
    logging_time = datetime.now()

    # prepare file name
    logging_file_name = str(logging_time).replace(":", "_")
    logging_file_name = "obd_log_" + logging_file_name[:19]

    # open file
    logging_file = open(logging_file_name, "w")

    # connect to ECU
    while obd_logger.status() != OBDStatus.CAR_CONNECTED:
        sleep(5)
        obd_logger = obd.OBD()
        sys.stdout.flush()

    print "####################################"
    print "Requested Commands are: "
    for x in commands:
        print x,
    print ""
    print "####################################"
    print "Logging " + str(logging_duration) + " values"
    raw_input("Press Enter to start...")
    sys.stdout.flush()
    print "Logging started..."

    logging_duration = int(logging_duration)
    for cnt in range(logging_duration):
        # get rpm, engine load
        # timing, throttle pos
        for x in commands:
            obd_response = obd_logger.query(obd.commands[x])

            # append if not empty
            if not obd_response.is_null():
                values.append(obd_response.value)
            else:
                values.append(0)

        # add linefeed
        values.append("\n")

        # show process
        if cnt % 10 == 0:
            print cnt

    # write values to file
    for item in values:
        logging_file.write(str(item) + " ")

    logging_file.close()
    print "logging successfully saved"
