# Setup
```
mkdir -p Workspace/TOFPET
cd Workspace/TOFPET
git clone https://github.com/CMSROMA/Timing-TOFPET2.git
cd Timing-TOFPET2
cmake .
make
```

# Alignment

Edit config_main_array_0,1,2,3.txt and run_DAQ_multiarrays_align.py as needed

Run daq:
```
python run_DAQ_multiarrays_align.py -c list_config_main_array.txt -o data/LYSOMULTIARRAYALIGNTEST5DEGREE_18_01_2021_FULLSCANBAR8 -n TEST
```

Create root files:
```
python process_runs.py -r 1-34 -d data/LYSOMULTIARRAYALIGNTEST5DEGREE_18_01_2021_FULLSCANBAR8
```

Analyze data:
```
python analysis/analyze_alignArray_with_barRef.py -i /home/cmsdaq/Workspace/TOFPET/Timing-TOFPET2/data/LYSOMULTIARRAYALIGNTEST5DEGREE_18_01_2021_FULLSCANBAR8/ -o /home/cmsdaq/Workspace/TOFPET/Timing-TOFPET2/data/LYSOMULTIARRAYALIGNTEST5DEGREE_18_01_2021_FULLSCANBAR8/
```

Check plots:
display  /home/cmsdaq/Workspace/TOFPET/Timing-TOFPET2/data/LYSOMULTIARRAYALIGNTEST5DEGREE_18_01_2021_FULLSCANBAR8/*.png

Finally edit run_DAQ_multiarrays.py with the positions of the arrays:
```
dict_array_x_y_z = {
    0: np.array([70., 40., 25.]),
    1: np.array([45., 140., 25.]),
    2: np.array([195., 140., 25.]),
    3: np.array([195., 40., 25.]),
}
```

# Run DAQ multiarrays
Edit config_main_array_0,1,2,3.txt and run_DAQ_multiarrays.py as needed

Run daq:
```
python run_DAQ_multiarrays.py  -c list_config_main_array.txt -o data/LYSOTEST -n TEST_NOSOURCE
```

Create root files:
```
python process_runs.py -r 1-3 -d data/LYSOTEST/
```


