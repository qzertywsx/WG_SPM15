"""Module providing an interface to the Wandel & Goltermann SPM-15 selective voltmeter"""
from enum import Enum
import time
import re

class DontExistError(Exception):
    """Don't exist exception"""

class WGSPM15():
    """Class to represent the Wandel & Goltermann SPM-15 selective voltmeter"""
    def __init__(self, _gpib, addr):
        self.address = addr
        self.gpib = _gpib
        self.first_time = True
        self._pre_command()
        self.gpib.query("++read eoi")
        self.gpib.write("++spoll")

    class Bandwidth(Enum):
        """Enum with the available bandwidth"""
        WIDEBAND = 0
        B25      = 1
        B1740    = 2
        B3100    = 3
        LSB      = 4
        USB      = 5

    class OutputImpedance(Enum):
        """Enum with the available output impedance"""
        COAX75 = 0
        BAL124 = 1
        BAL150 = 2
        BAL600 = 3
        BAL0   = 4

    class InputImpedance(Enum):
        """Enum with the available input impedance"""
        COAX75     = 0
        COAX75_INF = 1
        BAL124     = 2
        BAL124_INF = 3
        BAL150     = 4
        BAL150_INF = 5
        BAL600     = 6
        BAL600_INF = 7

    class Calibration(Enum):
        """Enum with the auto calibration mode"""
        OFF       = 0
        ON        = 1
        NEXT_MEAS = 2

    class OutputValue(Enum):
        """Enum with the output value"""
        MEAS_LEVEL          = 0
        GEN_LEVEL           = 1
        FREQ                = 2
        MEAS_GEN_LEVEL      = 3
        MEAS_LEVEL_FREQ     = 4
        MEAS_GEN_LEVEL_FREQ = 5
        GEN_LEVEL_FREQ      = 6
        ERROR               = 7

    class LevelDisplay(Enum):
        """Enum with the level display"""
        ABS        = 0
        REF        = 1
        ABS_REF    = 2
        ABS_TO_REF = 3

    class MeasurementType(Enum):
        """Enum with the display mode"""
        DIGITAL_AUTORANGE    = 0
        DIGITAL_LOW_NOISE    = 1
        DIGITAL_NORMAL_DRIVE = 2
        DIGITAL_LOW_DIST     = 3
        ANALOG_1             = 4
        ANALOG_20            = 5

    class TriggerMode(Enum):
        """Enum with the display mode"""
        CONTINUOUS = 0
        SINGLE     = 1

    def __str__(self):
        return "W&G SPM15 address: " + str(self.address)

    def _pre_command(self):
        """Command to be executed before every other command"""
        if self.gpib.address != self.address or self.first_time:
            self.first_time = False
            self.gpib.set_address(self.address)
            #self.gpib.write("++eor 2")

    def reset(self):
        """Reset the instrument to the default state"""
        self._pre_command()
        self.gpib.query("++clr")

    def _wait_busy_flag(self):
        """Write message to GPIB bus and read results."""
        while True:
            self.gpib.write('++spoll') #Request the status from the instrument
            flag = self.gpib.read()    #Read the status
            if flag != '':             #If the status is not empty
                try:
                    flag = int(flag.replace("\n", "").replace("\r", "")) #    Transform it to int
                except (ValueError, AttributeError):
                    flag = 16          #    Default to the instrument being busy
            else:                      #Else
                flag = 16              #    Default to the instrument being busy
            if not flag & 0b00010000:  #If the instrument is not busy
                break                  #    Escape the loop
            time.sleep(0.1)

    def set_frequency(self, freq):
        """Set the frequancy of the instrument"""
        self._pre_command()
        if 50 <= freq < 10e6:
            self.gpib.write(f"F{freq:0>8},")

    def set_amplitude(self, val):
        """Set the generator amplitude"""
        self._pre_command()
        if -50.9 <= val <= 10.03:
            self.gpib.write(f"L{val:+06.1f},")

    def measure(self):
        """Take a measurement"""
        self._pre_command()
        #self.gpib.write("\n")
        #self.gpib.read()
        self.gpib.write("++trg")
        self._wait_busy_flag()
        #time.sleep(10)
        try:
            tmp = self.gpib.query("++read eoi")
            #print("tmp:", tmp)
            if "," not in tmp:
                return float(re.sub("[ a-zA-Z]", "", tmp))
            tmp = tmp.split(",")
            for i, v in enumerate(tmp):
                if v[0] != "F":
                    tmp[i] = float(re.sub("[ a-zA-Z]", "", v))
                else:
                    tmp[i] = int(re.sub("[ a-zA-Z]", "", v))
            return tmp
        except (ValueError, AttributeError):
            return False

    def set_bandwidth(self, bw):
        """Set the bandwidth of the receiver"""
        self._pre_command()
        if bw == self.Bandwidth.WIDEBAND:
            self.gpib.write('B0,')
        elif bw == self.Bandwidth.B25:
            self.gpib.write('B1,')
        elif bw == self.Bandwidth.B1740:
            self.gpib.write('B3,')
        elif bw == self.Bandwidth.B3100:
            self.gpib.write('B4,')
        elif bw == self.Bandwidth.LSB:
            self.gpib.write('B6,')
        elif bw == self.Bandwidth.USB:
            self.gpib.write('B7,')
        else:
            raise DontExistError("Selected bandwidth don't exist")

    def set_output_impedance(self, z):
        """Set the output (generator) impedance"""
        self._pre_command()
        if z == self.OutputImpedance.COAX75:
            self.gpib.write('P0,')
        elif z == self.OutputImpedance.BAL124:
            self.gpib.write('P1,')
        elif z == self.OutputImpedance.BAL150:
            self.gpib.write('P2,')
        elif z == self.OutputImpedance.BAL600:
            self.gpib.write('P5,')
        elif z == self.OutputImpedance.BAL0:
            self.gpib.write('P6,')
        else:
            raise DontExistError("Selected output Impedance don't exist")

    def set_input_impedance(self, z):
        """Set the input (receiver) impedance"""
        self._pre_command()
        if z == self.InputImpedance.COAX75:
            self.gpib.write('Q01,')
        elif z == self.InputImpedance.COAX75_INF:
            self.gpib.write('Q08,')
        elif z == self.InputImpedance.BAL124:
            self.gpib.write('Q11,')
        elif z == self.InputImpedance.BAL124_INF:
            self.gpib.write('Q18,')
        elif z == self.InputImpedance.BAL150:
            self.gpib.write('Q21,')
        elif z == self.InputImpedance.BAL150_INF:
            self.gpib.write('Q28,')
        elif z == self.InputImpedance.BAL600:
            self.gpib.write('Q41,')
        elif z == self.InputImpedance.BAL600_INF:
            self.gpib.write('Q48,')
        else:
            raise DontExistError("Selected input Impedance don't exist")

    def enable_generator(self, on):
        """Switch the genarator on or off"""
        self._pre_command()
        if on:
            self.gpib.write("G0210,")
        else:
            self.gpib.write("G1210,")

    def set_calibration(self, cal):
        """Set the auto calibration mode"""
        self._pre_command()
        if cal == self.Calibration.OFF:
            self.gpib.write('C0,')
        elif cal == self.Calibration.ON:
            self.gpib.write('C1,')
        elif cal == self.Calibration.NEXT_MEAS:
            self.gpib.write('C3,')
        else:
            raise DontExistError("Selected calibration don't exist")

    def set_output_value(self, ov):
        """Choose the output (measurement) value"""
        self._pre_command()
        if ov == self.OutputValue.MEAS_LEVEL:
            self.gpib.write('D11,')
        elif ov == self.OutputValue.GEN_LEVEL:
            self.gpib.write('D12,')
        elif ov == self.OutputValue.FREQ:
            self.gpib.write('D13,')
        elif ov == self.OutputValue.MEAS_GEN_LEVEL:
            self.gpib.write('D14,')
        elif ov == self.OutputValue.MEAS_LEVEL_FREQ:
            self.gpib.write('D15,')
        elif ov == self.OutputValue.MEAS_GEN_LEVEL_FREQ:
            self.gpib.write('D16,')
        elif ov == self.OutputValue.GEN_LEVEL_FREQ:
            self.gpib.write('D17,')
        elif ov == self.OutputValue.ERROR:
            self.gpib.write('D99,')
        else:
            raise DontExistError("Selected output value don't exist")

    def set_trigger_mode(self, t):
        """Set the trigger mode"""
        self._pre_command()
        if t == self.TriggerMode.CONTINUOUS:
            self.gpib.write('T0,')
        elif t == self.TriggerMode.SINGLE:
            self.gpib.write('T1,')
        else:
            raise DontExistError("Selected trigger mode don't exist")

    def set_level_measurement(self, lev_disp, meas_type):
        """Set the level display and measurement type"""
        self._pre_command()
        command = "R"
        if lev_disp == self.LevelDisplay.ABS:
            command += "0"
        elif lev_disp == self.LevelDisplay.REF:
            command += "1"
        elif lev_disp == self.LevelDisplay.ABS_REF:
            command += "2"
        elif lev_disp == self.LevelDisplay.ABS_TO_REF:
            command += "8"
        else:
            raise DontExistError("Selected XXX don't exist")

        if meas_type == self.MeasurementType.DIGITAL_AUTORANGE:
            command += "02"
        elif meas_type == self.MeasurementType.DIGITAL_LOW_NOISE:
            command += "12"
        elif meas_type == self.MeasurementType.DIGITAL_NORMAL_DRIVE:
            command += "22"
        elif meas_type == self.MeasurementType.DIGITAL_LOW_DIST:
            command += "32"
        elif meas_type == self.MeasurementType.ANALOG_1:
            command += "42"
        elif meas_type == self.MeasurementType.ANALOG_20:
            command += "52"
        else:
            raise DontExistError("Selected YYY don't exist")
        self.gpib.write(command+',')

    def local(self):
        """Go to local mode (Reenable the front panel control)"""
        self._pre_command()
        self.gpib.local()
