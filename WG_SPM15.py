from enum import Enum
import time
import re

class WG_SPM15(object):
	def __init__(self, gpib, addr):
		self.address = addr
		self.gpib = gpib
		self.firstTime = True
		self._preCommand()
		gpib.query("++read eoi")
		gpib.write("++spoll")
	
	class Bandwidth(Enum):
		WIDEBAND = 0
		B25      = 1
		B1740    = 2
		B3100    = 3
		LSB      = 4
		USB      = 5
	
	class OutputImpedance(Enum):
		COAX75 = 0
		BAL124 = 1
		BAL150 = 2
		BAL600 = 3
		BAL0   = 4
	
	class InputImpedance(Enum):
		COAX75     = 0
		COAX75_INF = 1
		BAL124     = 2
		BAL124_INF = 3
		BAL150     = 4
		BAL150_INF = 5
		BAL600     = 6
		BAL600_INF = 7
	
	class Calibration(Enum):
		OFF       = 0
		ON        = 1
		NEXT_MEAS = 2
	
	class OutputValue(Enum):
		MEAS_LEVEL          = 0
		GEN_LEVEL           = 1
		FREQ                = 2
		MEAS_GEN_LEVEL      = 3
		MEAS_LEVEL_FREQ     = 4
		MEAS_GEN_LEVEL_FREQ = 5
		GEN_LEVEL_FREQ      = 6
		ERROR               = 7
	
	class LevelDisplay(Enum):
		ABS        = 0
		REF        = 1
		ABS_REF    = 2
		ABS_TO_REF = 3
	
	class MeasurementType(Enum):
		DIGITAL_AUTORANGE    = 0
		DIGITAL_LOW_NOISE    = 1
		DIGITAL_NORMAL_DRIVE = 2
		DIGITAL_LOW_DIST     = 3
		ANALOG_1             = 4
		ANALOG_20            = 5
	
	class TriggerMode(Enum):
		CONTINUOUS = 0
		SINGLE     = 1
	
	def __str__(self):
		return "W&G SPM15 address: " + str(self.address)
	
	def _preCommand(self):
		"""Command to be executed before every other command"""
		if self.gpib.address != self.address or self.firstTime:
			self.firstTime = False
			self.gpib.set_address(self.address)
			#self.gpib.write("++eor 2")
	
	def reset(self):
		"""Reset the instrument to the default state"""
		self._preCommand()
		gpib.query("++clr")
	
	def _waitBusyFlag(self):
		"""Write message to GPIB bus and read results."""
		while True:
			self.gpib.write('++spoll')																									#Request the status from the instrument
			try:
				flag = self.gpib.read()																										#Read the status
			except:
				continue
			if flag != '':																															#If the status is not empty
				try:
					flag = int(flag.replace("\n", "").replace("\r", ""))										#	Transform it to integer
				except:
					flag = 16																																#	Default to the instrument being busy
			else:																																				#Else
				flag = 16																																	#	Default to the instrument being busy
			if not (flag & 0b00010000):																									#If the instrument is not busy
				break																																			#	Escape the loop
			time.sleep(0.1)
	
	def setFrequency(self, freq):
		"""Set the frequancy of the instrument"""
		self._preCommand()
		if freq < 10e6:
			self.gpib.write("F{:0>8},".format(freq))
	
	def setAmplitude(self, val):
		"""Set the generator amplitude"""
		self._preCommand()
		if val >= -50.9 and val <= 10.03:
			self.gpib.write("L{:+06.1f},".format(val))
	
	def measure(self):
		"""Take a measurement"""
		self._preCommand()
		#self.gpib.write("\n")
		self.gpib.read()
		self.gpib.write("++trg")
		self._waitBusyFlag()
		#time.sleep(10)
		try:
			tmp = self.gpib.query("++read eoi")
			#print("tmp:", tmp)
			if "," not in tmp:
				return float(re.sub("[ a-zA-Z]", "", tmp))
			else:
				tmp = tmp.split(",")
				for i, v in enumerate(tmp):
					if v[0] != "F":
						tmp[i] = float(re.sub("[ a-zA-Z]", "", v))
					else:
						tmp[i] = int(re.sub("[ a-zA-Z]", "", v))
				return tmp
		except:
			return False
	
	def setBandwidth(self, bw):
		"""Set the bandwidth of the receiver"""
		self._preCommand()
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
			raise Exception("Selected bandwidth don't exist")
	
	def setOutputImpedance(self, z):
		"""Set the output (generator) impedance"""
		self._preCommand()
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
			raise Exception("Selected output Impedance don't exist")
	
	def setInputImpedance(self, z):
		"""Set the input (receiver) impedance"""
		self._preCommand()
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
			raise Exception("Selected input Impedance don't exist")
	
	def enableGenerator(self, on):
		"""Switch the genarator on or off"""
		self._preCommand()
		if on:
			self.gpib.write("G0210,")
		else:
			self.gpib.write("G1210,")
	
	def setCalibration(self, cal):
		"""Set the auto calibration mode"""
		self._preCommand()
		if cal == self.Calibration.OFF:
			self.gpib.write('C0,')
		elif cal == self.Calibration.ON:
			self.gpib.write('C1,')
		elif cal == self.Calibration.NEXT_MEAS:
			self.gpib.write('C3,')
		else:
			raise Exception("Selected calibration don't exist")
	
	def setOutputValue(self, ov):
		"""Choose the output (measurement) value"""
		self._preCommand()
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
			raise Exception("Selected output value don't exist")
	
	def setTriggerMode(self, t):
		"""Set the trigger mode"""
		self._preCommand()
		if t == self.TriggerMode.CONTINUOUS:
			self.gpib.write('T0,')
		elif t == self.TriggerMode.SINGLE:
			self.gpib.write('T1,')
		else:
			raise Exception("Selected trigger mode don't exist")
	
	def setLevelMeasurement(self, levDisp, measType):
		"""Set the level display and measurement type"""
		self._preCommand()
		command = "R"
		if levDisp == self.LevelDisplay.ABS:
			command += "0"
		elif levDisp == self.LevelDisplay.REF:
			command += "1"
		elif levDisp == self.LevelDisplay.ABS_REF:
			command += "2"
		elif levDisp == self.LevelDisplay.ABS_TO_REF:
			command += "8"
		else:
			raise Exception("Selected XXX don't exist")
		
		if measType == self.MeasurementType.DIGITAL_AUTORANGE:
			command += "02"
		elif measType == self.MeasurementType.DIGITAL_LOW_NOISE:
			command += "12"
		elif measType == self.MeasurementType.DIGITAL_NORMAL_DRIVE:
			command += "22"
		elif measType == self.MeasurementType.DIGITAL_LOW_DIST:
			command += "32"
		elif measType == self.MeasurementType.ANALOG_1:
			command += "42"
		elif measType == self.MeasurementType.ANALOG_20:
			command += "52"
		else:
			raise Exception("Selected YYY don't exist")
		self.gpib.write(command+',')
		
	def local(self):
		"""Go to local mode (Reenable the front panel control)"""
		self._preCommand()
		self.gpib.local()
