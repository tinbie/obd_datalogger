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
        logging_duration = 1200

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
        sleep(10)
        obd_logger = obd.OBD()
        sys.stdout.flush()

    print "####################################"
    print "Requested Commands are: "
    for x in commands:
        print x,
    print ""
    print "####################################"
    print "Logging duration: " + str(logging_duration) + " s"
    raw_input("Press Enter to start...")
    sys.stdout.flush()

    logging_duration = int(logging_duration) * 10
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
        sleep(0.1)

    # write values to file
    for item in values:
        logging_file.write(str(item) + " ")

    logging_file.close()
    print "logging successfully saved"
