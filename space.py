import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

#Background color
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt
#Image
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QIcon, QPixmap

#Graph
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, QPushButton
from PyQt5.QtGui import QIcon


from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import random

#Thingspeak
import http.client

#Time
from time import gmtime, strftime

#The temperature sensor Library
import Adafruit_DHT

#
import numpy as np

class App(QWidget):

	def __init__(self):
		super().__init__()
		self.title = 'Weather Station'
		self.left = 10
		self.top = 10
		self.width = 400
		self.height = 400
		self.units = "Celsius"
		self.initUI()

	def initUI(self):
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)

		# Set window background color
		'''self.setAutoFillBackground(True)
		p = self.palette()
		p.setColor(self.backgroundRole(), QColor(200, 0, 0))
		self.setPalette(p)'''

		# Create widget
		label = QLabel(self)
		pixmap = QPixmap('image.jpg')
		label.setPixmap(pixmap)
		#Resize window based on image dimentsions
		self.resize(pixmap.width(),pixmap.height())


		#Set units:
		#layout = QHBoxLayout()
		#self.b1 = QRadioButton("Button1")
		#self.b1.move(150,50)
		#self.b1.setChecked(True)
		#self.b1.toggled.connect(lambda:self.btnstate(self.b1))
		#layout.addWidget(self.b1)

		#Set units
		self.buttonA = QPushButton("C", self)
		self.buttonA.move(75,50)
		# connect button to function on_click
		self.buttonA.clicked.connect(self.on_click_celsius)

		self.buttonB = QPushButton("F", self)
		self.buttonB.move(150,50)
		# connect button to function on_click
		self.buttonB.clicked.connect(self.on_click_fahrenheit)

		#Temperature Button      
		# Create a button in the window
		self.button = QPushButton('Show Temperature', self)
		self.button.move(150,100)
		# connect button to function on_click
		self.button.clicked.connect(self.on_click_temperature)

		#Humidity button
		# Create a button in the window
		self.button2 = QPushButton('Show Humidity', self)
		self.button2.move(150,150)
		# connect button to function on_click
		self.button2.clicked.connect(self.on_click_humidity)   

		'''
		#Record multiple data
		# Create a button in the window
		self.button3 = QPushButton('Record Data', self)
		self.button3.move(150,200)
		# connect button to function on_click
		self.button3.clicked.connect(self.on_click_record) 

		#Plot Graph
		# Create a button in the window
		self.button4 = QPushButton('Plot Graph', self)
		self.button4.move(150,250)
		# connect button to function on_click
		self.button4.clicked.connect(self.on_click_plot) '''

		#Send data to Thingspeak
		# Create a button in the window
		self.button5 = QPushButton('Send to Cloud', self)
		self.button5.move(150,200)
		# connect button to function on_click
		self.button5.clicked.connect(self.on_click_server) 

		self.show()
	
	def btnstate(self,b):
		if b.text() == "Button1":
			if b.isChecked() == True:
				print (b.text()+" is selected")
			else:
				print (b.text()+" is deselected")
	@pyqtSlot()
	def on_click_fahrenheit(self):
		self.units="Fahrenheit"
	def on_click_celsius(self):
		self.units="Celsius"
	def on_click_temperature(self):
		value=get_data(self, 'temperature', self.units)
		QMessageBox.information(self, 'Weather App', "The Temperature is: " + value+ self.units +"\nTime is:"+strftime("%Y-%m-%d %H:%M:%S", gmtime()), QMessageBox.Ok, QMessageBox.Ok)
	def on_click_humidity(self):
		value=get_data(self, 'humidity', self.units)
		QMessageBox.information(self, 'Weather App', "The Humidty is: " + value +"Percent\nTime is:"+strftime("%Y-%m-%d %H:%M:%S", gmtime()),QMessageBox.Ok, QMessageBox.Ok)
	def on_click_record(self):
		QMessageBox.information(self, 'Weather App', "Recording multiple values"+"\nTime is:"+strftime("%Y-%m-%d %H:%M:%S", gmtime()),QMessageBox.Ok, QMessageBox.Ok)
		
		for i in range (0,9):
			valueTemperature[i]=get_data(self, 'temperature', self.units)
			valueHumidity[i]=get_data(self, 'humidity', self.units)
		QMessageBox.information(self, 'Weather App', "Done Recording values",QMessageBox.Ok, QMessageBox.Ok)
		for i in range (0,9):
			print ("Values are: "+ valueTemperature[i] +"\t"+ valueHumidity[i]+"\n")
		QMessageBox.information(self, 'Weather App', "Done Printing values"+"\nTime is:"+strftime("%Y-%m-%d %H:%M:%S", gmtime()),QMessageBox.Ok, QMessageBox.Ok)
		
	def on_click_plot(self):
		QMessageBox.information(self, 'Weather App', "Plotting Graph when you press OK",QMessageBox.Ok, QMessageBox.Ok)
		PlotGraph(self)
	def on_click_server(self):
		valueTemperature=get_data(self, 'temperature', "Celsius")				#To have consistency in server data, send only Celsius temperature
		valueHumidity=get_data(self, 'humidity', "Celsius")
		QMessageBox.information(self, 'Weather App', "Temperature is: " + valueTemperature + "Celsius" +"\nHumidity is: "+valueHumidity+"Percent" , QMessageBox.Ok)
		sendToCloud(self,valueTemperature,valueHumidity)
		QMessageBox.information(self, 'Weather App', "Sent data to ThingSpeak Server"+"\nTime is:"+strftime("%Y-%m-%d %H:%M:%S", gmtime()),QMessageBox.Ok, QMessageBox.Ok)

def get_data(self, which_data, units):
	sensor = 22
	pin = 4

	humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

	# Un-comment the line below to convert the temperature to Fahrenheit.
	if units == "Fahrenheit":
		temperature = temperature * 9/5.0 + 32
		
	# Note that sometimes you won't get a reading and
	# the results will be null (because Linux can't
	# guarantee the timing of calls to read the sensor).
	# If this happens try again!
	if humidity is not None and temperature is not None:
		print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
		if(which_data=='temperature'):
			return str(temperature)
		else:
			return str(humidity)
		
	else:
		print('Failed to get reading. Try again!')
		QMessageBox.warning(self, 'Weather App', "DHT sensor didn't respond!",QMessageBox.Ok, QMessageBox.Ok)
				
	#sys.exit(1)

	

class PlotCanvas(FigureCanvas):

	def __init__(self, parent=None, width=5, height=4, dpi=100):
		fig = Figure(figsize=(width, height), dpi=dpi)
		self.axes = fig.add_subplot(111)

		FigureCanvas.__init__(self, fig)
		self.setParent(parent)

		FigureCanvas.setSizePolicy(self,
		QSizePolicy.Expanding,
		QSizePolicy.Expanding)
		FigureCanvas.updateGeometry(self)
		self.plot()


	def plot(self):
		data = [random.random() for i in range(25)]
		ax = self.figure.add_subplot(111)
		ax.plot(data, 'r-')
		ax.set_title('PyQt Matplotlib Example')
		self.draw()

def PlotGraph(self):
	#Graph
	m = PlotCanvas(self, width=5, height=4)
	m.move(0,0)

def sendToCloud(self,temperature, humidity):
	#Thingspeak http
	#temp=str(22)
	conn = http.client.HTTPConnection("52.5.13.84")
	conn.request("GET","/update?key=7BT0BLXRFDFWGVWL&field1=%s&field2=%s\n"%(temperature,humidity))
	conn.close()

if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = App()
	sys.exit(app.exec_())
