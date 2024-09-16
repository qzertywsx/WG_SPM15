# WG_SPM15
Python module for the Wandel &amp; Goltermann SPM-15 selective voltmeter.

You must use my GPIB or GPIB_WIFI module to use this module.

## Supported command:
### waitBusyFlag()
Wait untile end of measurement

### reset()
Reset the instrument to the default state

### setFrequency(freq)
Set the frequancy of the instrument

### setAmplitude(val)
Set the generator amplitude

### measure()
Take a measurement

Return the measurement as real value, a list if more than one value or `False` in case of problem

### setBandwidth(bw)
Set the bandwidth of the receiver
<table>
  <tr><td>bw</td><td>Description</td></tr>
  <tr><td>WG_SPM15.Bandwidth.WIDEBAND</td><td>Wideband</td></tr>
  <tr><td>WG_SPM15.Bandwidth.B25</td><td>25 Hz</td></tr>
  <tr><td>WG_SPM15.Bandwidth.B1740</td><td>1.74 kHz</td></tr>
  <tr><td>WG_SPM15.Bandwidth.B3100</td><td>3.1 kHz</td></tr>
  <tr><td>WG_SPM15.Bandwidth.LSB</td><td>Lower side band demodulator</td></tr>
  <tr><td>WG_SPM15.Bandwidth.USB</td><td>Upper side band demodulator</td></tr>
</table>
The default instrument mode is WG_SPM15.Bandwidth.B3100

### setOutputImpedance(z)
Set the output (generator) impedance
<table>
  <tr><td>z</td><td>Description</td></tr>
  <tr><td>WG_SPM15.OutputImpedance.COAX75</td><td>75 &Omega; coaxial output</td></tr>
  <tr><td>WG_SPM15.OutputImpedance.BAL124</td><td>124 &Omega; balanced output</td></tr>
  <tr><td>WG_SPM15.OutputImpedance.BAL150</td><td>150 &Omega; balanced output</td></tr>
  <tr><td>WG_SPM15.OutputImpedance.BAL600</td><td>600 &Omega; balanced output</td></tr>
  <tr><td>WG_SPM15.OutputImpedance.BAL0</td><td>0 &Omega; balanced output</td></tr>
</table>
The default instrument mode is WG_SPM15.OutputImpedance.COAX75

### setInputImpedance(z)
Set the input (receiver) impedance
<table>
  <tr><td>z</td><td>Description</td></tr>
  <tr><td>WG_SPM15.InputImpedance.COAX75</td><td>75 &Omega; coaxial input</td></tr>
  <tr><td>WG_SPM15.InputImpedance.COAX75_INF</td><td>High impedance coaxial input</td></tr>
  <tr><td>WG_SPM15.InputImpedance.BAL124</td><td>124 &Omega; balanced input</td></tr>
  <tr><td>WG_SPM15.InputImpedance.BAL124_INF</td><td>High impedance balanced input</td></tr>
  <tr><td>WG_SPM15.InputImpedance.BAL150</td><td>150 &Omega; balanced input</td></tr>
  <tr><td>WG_SPM15.InputImpedance.BAL150_INF</td><td>High impedance balanced input</td></tr>
  <tr><td>WG_SPM15.InputImpedance.BAL600</td><td>600 &Omega; balanced input</td></tr>
  <tr><td>WG_SPM15.InputImpedance.BAL600_INF</td><td>High impedance balanced input</td></tr>
</table>
The default instrument mode is WG_SPM15.InputImpedance.COAX75

### enableGenerator(on)
Switch the genarator on or off
<table>
  <tr><td>on</td><td>Description</td></tr>
  <tr><td>True</td><td>Switch on the generator</td></tr>
  <tr><td>False</td><td>Switch off the generator</td></tr>
</table>
The default instrument mode is False (Generator OFF)

### setCalibration(cal)
Set the auto calibration mode
<table>
  <tr><td>cal</td><td>Description</td></tr>
  <tr><td>WG_SPM15.Calibration.OFF</td><td>Auto calibration off</td></tr>
  <tr><td>WG_SPM15.Calibration.ON</td><td>Auto calibration on</td></tr>
  <tr><td>WG_SPM15.Calibration.NEXT_MEAS</td><td>Calibrate with next measurement</td></tr>
</table>
The default instrument mode is WG_SPM15.Calibration.ON

### setOutputValue(ov)
Choose the output (measurement) value
<table>
  <tr><td>ov</td><td>Description</td></tr>
  <tr><td>WG_SPM15.OutputValue.MEAS_LEVEL</td><td>Measured level</td></tr>
  <tr><td>WG_SPM15.OutputValue.GEN_LEVEL</td><td>Generated level</td></tr>
  <tr><td>WG_SPM15.OutputValue.FREQ</td><td>Frequency of the instrument</td></tr>
  <tr><td>WG_SPM15.OutputValue.MEAS_GEN_LEVEL</td><td>Measured and generated level</td></tr>
  <tr><td>WG_SPM15.OutputValue.MEAS_LEVEL_FREQ</td><td>Measured level and frequency</td></tr>
  <tr><td>WG_SPM15.OutputValue.MEAS_GEN_LEVEL_FREQ</td><td>Measured and generated level and frequency</td></tr>
  <tr><td>WG_SPM15.OutputValue.GEN_LEVEL_FREQ</td><td>Generated level and frequency</td></tr>
  <tr><td>WG_SPM15.OutputValue.ERROR</td><td>Return the last error (0000 if no error)</td></tr>
</table>
The default instrument mode is WG_SPM15.OutputValue.MEAS_LEVEL

### setTriggerMode(t)
Set the trigger mode
<table>
  <tr><td>t</td><td>Description</td></tr>
  <tr><td>WG_SPM15.TriggerMode.CONTINUOUS</td><td>Continuous triggering of measurement</td></tr>
  <tr><td>WG_SPM15.TriggerMode.SINGLE</td><td>Single trigger</td></tr>
</table>
The default instrument mode is WG_SPM15.TriggerMode.CONTINUOUS

### setLevelMeasurement(levDisp, measType)
Set the level display and measurement type

<table>
  <tr><td>levDisp</td><td>Description</td></tr>
  <tr><td>WG_SPM15.LevelDisplay.ABS</td><td>Absolute level</td></tr>
  <tr><td>WG_SPM15.LevelDisplay.REF</td><td>Reference level</td></tr>
  <tr><td>WG_SPM15.LevelDisplay.ABS_REF</td><td>Level difference (ABS-REF)</td></tr>
  <tr><td>WG_SPM15.LevelDisplay.ABS_TO_REF</td><td>Set a measurement value as the reference</td></tr>
</table>

The default instrument mode is WG_SPM15.LevelDisplay.ABS

<table>
  <tr><td>measType</td><td>Description</td></tr>
  <tr><td>WG_SPM15.MeasurementType.DIGITAL_AUTORANGE</td><td>Digital measurement with autorange</td></tr>
  <tr><td>WG_SPM15.MeasurementType.DIGITAL_LOW_NOISE</td><td>Digital measurement - Low noise drive condition</td></tr>
  <tr><td>WG_SPM15.MeasurementType.DIGITAL_NORMAL_DRIVE</td><td>Digital measurement - Normal drive condition</td></tr>
  <tr><td>WG_SPM15.MeasurementType.DIGITAL_LOW_DIST</td><td>Digital measurement - Low distortion drive condition</td></tr>
  <tr><td>WG_SPM15.MeasurementType.ANALOG_1</td><td>Analog measurement - 1 dB scale with autorange</td></tr>
  <tr><td>WG_SPM15.MeasurementType.ANALOG_20</td><td>Analog measurement - 20 dB scale with autorange</td></tr>
</table>

The default instrument mode is WG_SPM15.MeasurementType.ANALOG_20

### local()
Go to local mode (Reenable the front panel control)

## Usage:
```python
from GPIB_WIFI import AR488_WIFI
from WG_SPM15 import WG_SPM15

gpib = AR488_WIFI('192.168.178.36', timeout=5)
vsel = WG_SPM15(gpib, 2)
vsel.setLevelMeasurement(WG_SPM15.LevelDisplay.ABS, WG_SPM15.MeasurementType.DIGITAL_AUTORANGE)
vsel.setCalibration(WG_SPM15.Calibration.OFF)
vsel.setTriggerMode(WG_SPM15.TriggerMode.CONTINUOUS)#SINGLE)
vsel.setBandwidth(WG_SPM15.Bandwidth.B25)
vsel.setOutputImpedance(WG_SPM15.OutputImpedance.COAX75)
vsel.setInputImpedance(WG_SPM15.InputImpedance.COAX75)
vsel.enableGenerator(True)
vsel.setOutputValue(WG_SPM15.OutputValue.MEAS_LEVEL)
vsel.setAmplitude(-27.5)
vsel.setFrequency(17200)
print(vsel.measure())
vsel.local()
```
## Result of executing the above code (Not done yet):
```
GPIB address: 2, IP: 192.168.178.36
```
