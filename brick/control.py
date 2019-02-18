__author__ = 'Brick'
import serial
import serial.tools.list_ports
import string
import time

		
		
class Car:
	def __init__(self):
		self.COM="/dev/ttyUSB1"
		self.open = False
		self.buf=''
		self.data=''
		res=self.create_com()
		self.LastError=0
		self.LastErrorR=0
	def create_com(self,COM='auto', baud_rate=115200):
		if self.open == True:
			self.ser.close()
		self.baud_rate = baud_rate		
		try:
			self.ser=serial.Serial(self.COM, self.baud_rate)
			self.open=True
		except:
			print('Error:Couldn\'t open serial port!')
			self.open = False
			time.sleep(1)
		return self.open
			

		
		
	def receive(self,count):
		if self.open==True:
			self.buf=self.ser.read(count)
			#self.data= str(binascii.b2a_hex(self.buf))[2:-1]
			print(self.buf)	
			
	def Forward(self):
		
		self.ser.write('Aq=-500,e=-500,z=-500,c=-500,z=-500!'.encode())
	def Backward(self):
		self.ser.write('Aq=500,e=500,z=500,c=500,z=500!'.encode())
	
	def Left(self):
		
		self.ser.write('Aq=-400,z=-400,e=400,c=400,z=-400!'.encode())
	def Right(self):
		self.ser.write('Aq=400,z=400,e=-400,c=-400,z=400!'.encode())
	def LL(self):
		self.ser.write('Aq=500,e=-500,z=-500,c=500,z=-500!'.encode())
	def RR(self):	
		self.ser.write('Aq=-500,e=500,z=500,c=-500,z=500!'.encode())
	
	def MoveI(self,q,e,z,c):
		cmd='A'+'q='+str(-q)+','+'e='+str(-e)+','+'z='+str(-z)+','+'c='+str(-c)+ ','  +'z='+str(-z)+'!'
		#print(cmd)
		self.ser.write(cmd.encode())

	def Stop(self):
		self.ser.write('Aq=0,e=0,z=0,c=0!'.encode())

	def auto_control(self,Dangle,dist,angleTH=70.0):
		if abs(Dangle)>angleTH:
			self.rotate_track(Dangle)
		else:
			self.line_track(Dangle)


	def rotate_track(self,Dangle,P=2.3,D=1):
		dV = P*Dangle 
		if abs(dV)<310:
			dV=310*(dV/abs(dV))
		#print('rotate',Dangle,dV)
		self.MoveI(dV,-dV,dV,-dV)

	def line_track(self,Dangle,BaseSpeed=380,BP=2.0,PP=0.00015,D=7):
		P=BP+PP*(Dangle**2)
		dV=P*Dangle + D*(Dangle - self.LastError)
		self.LastError=Dangle
		BaseSpeed=500-1000.0*abs(Dangle)/180.0
		self.MoveI(BaseSpeed+dV,BaseSpeed-dV,BaseSpeed+dV,BaseSpeed-dV)

	def Lidar_process(self):
		i=0
		j=0
		while True:
			
			if self.open == False:
				res=self.create_com()
			
			self.Lidar_Get()
			count = self.ser.inWaiting()  
			if count != 0: 
				self.receive(count)
				j=j+1

				self.ser.write(s)
				
				

			
if __name__ == "__main__":
	ldr=Car()
	#ldr.Lidar_process()
			
			
			
		
		
		
		
		
		
		
		
		
		
		
		
