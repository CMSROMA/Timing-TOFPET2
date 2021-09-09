# Setup
```
mkdir -p Workspace/TOFPET
cd Workspace/TOFPET
git clone https://github.com/CMSROMA/Timing-TOFPET2.git
cd Timing-TOFPET2
cmake .
make
```

# TOFPET Calibration
Switch on TOFPET and wait until system is stable
./start_gui
daq comm server = GBE
ON 
Working dir = es. /home/cmsdaq/Workspace/TOFPET/Timing-TOFPET2/data/calib/1bar_4arrays_5degreeSet_2021_09_08 --> ENTER --> YES to create new dir
System Configuration --> DETECT --> YES

Edit config.ini (section asic_parameter):
```
global.disc_lsb_t1 = 60
global.disc_lsb_t2 = 60 
channel.min_intg_time = 34
channel.max_intg_time = 34
global.v_att_diff_bias_ig=56
channel.att=3
channel.fe_delay=16
channel.trigger_mode_2_t=0
channel.trigger_mode_2_q=0
channel.trigger_mode_2_e=2
channel.trigger_mode_2_b=4
```
This is the cut&paste of the config_current.ini.
--> SAVE

SiPM Bias Settings:
```
PreBDV = 46.40 
BDV = 51.40
OV = 8.00
```
These are the values for SiPM arrays
--> SAVE
--> Edit (to change the HV 7 channel where single bar is connected 
```
0       0       7       0.75    45.6    50.60   8 )
```

ASIC Calibration: 
Discriminator, TDC, QCD flagged.
Start Calibration
wait for 1-2 hours untile completed.

daq comm server OFF
Close the GUI.

Edit the 4 configuration files for each array:
config_main_array_0.txt  , config_main_array_1.txt , config_main_array_2.txt , 
config_main_array_3.txt
```
CALIB_DIR /home/cmsdaq/Workspace/TOFPET/Timing-TOFPET2/data/calib/1bar_4arrays_5degreeSet_2021_09_08
```
where the path corresponds to the new folder just created.

Ready to take data.

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


