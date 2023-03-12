**** Documentation for this NEC controller ****

**RUNNING THE CODE**

**Disclaimer:** I have not tested this with the actual nec monitor. I spent considerable time trying to get the byte strings correct, but there could still be some issues.

**INSTALLATION:**
I have tried to use only python built-in functions, so pip installing additional libraries should not be required.

To use, simply pull down the repo in an environment with python 3.7 or greater. Also, you may have to change local IP/ports of main, nec_controller, or monitor_simulator, as needed depending on your machine.

**WITH REAL MONITOR - THIS IS DEFAULT:** 

All you have to do is run main.py and go to the local/ip port the web form is hosted at. Default is 127.0.0.1:8000. Then open up the web browser at http://127.0.0.1:8080/form.html


**WITH SIMULATED TEST MONITOR:**

Run - python monitor_simulator.py

There should be an output to the terminal indicating it was successfully bound/connected. Default IP/Port is local 127.0.0.1:7142

Change the IP/port in the connect_to_nec_monitor() inside nec_controller.py to be local "127.0.0.1", 7142 so that it can talk to the simulated monitor. There should be a line already commented out there for that.


**RUNNING UNIT TESTS:**

python unittests.py


**TECHNICAL INFORMATION:**

main.py - serves up and handle web form.html requests to python http server.

nec_controller.py - This handles piecing together the monitor commands, calculating check code, converting to ascii, sending the commands and does the grunt, controller work.

monitor_commands.py - hard coded lists of hex bytes, representing the commands outlined in the NEC technical manual.

monitor_simulator.py - This "simulated monitor" just prints out all the commands that hit it through TCP/IP as well as track through a global variable the power state and reply back when requested in a simulated fashion, in the manner that the real monitor is expected to do.

unittests.py - These are a couple simple unit tests for the helper functions for the controller. It tests the calculate_bcc function, the convert_to_ascii function as well as the volume_four_byte_calculator function, which is supposed to convert the volume command 0-100 in decimal to the appropriate 4 byte sequence required by the monitor.
