# Setup
```
mkdir -p Workspace/TOFPET
cd Workspace/TOFPET
git clone https://github.com/CMSROMA/Timing-TOFPET2.git
cd Timing-TOFPET2
cmake .
make
```

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
