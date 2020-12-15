# Setup
```
mkdir -p Workspace/TOFPET
cd Workspace/TOFPET
git clone https://github.com/CMSROMA/Timing-TOFPET2.git
cd Timing-TOFPET2
cmake .
make
```

# Temperature sensors
Open a new terminal
```
cd /home/cmsdaq/Workspace/TOFPET/Timing-TOFPET2/arduino/temperature
python2 serial_monitor.py -d /dev/ttyACM0 -l temperature_tmp.txt &
```
keep terminal open


# Motors
Open a new terminal
```
cd /home/cmsdaq/Workspace/TOFPET/Timing-TOFPET2/arduino/motors
python3 grblServer.py --usb /dev/ttyUSB0 -l /tmp/test.log --port=8820
```
keep terminal open


# Run DAQ
Edit config_main_bar.txt, config_main_array.txt and run_DAQ.py

Run daq:
```
python run_DAQ.py -c config_main_bar.txt -o data/LYSOTEST -n TEST_NOSOURCE
```

Create root files:
```
python process_runs.py -r 1-4 -d data/LYSOTEST/
```
