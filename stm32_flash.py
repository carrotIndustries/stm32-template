#!/usr/bin/python

#from https://github.com/Selfnet/self-control-led/blob/master/stm32_flash.py

import sys
import traceback
import telnetlib
import logging


HOST = "localhost"
PORT = 4444
TIMEOUT = 1


logging.basicConfig(level=logging.INFO,
					format='%(asctime)s %(levelname)s %(message)s')


class OOCDTelnet(object):
	def __init__(self, host, port,timeout): 
		self.tel = telnetlib.Telnet(host, port) 
		self.timeout = timeout
		self.read_data()
	
	def close(self): 
		self.tel.close()

	def read_data(self): 
		return self.tel.read_until(b"\r\n\r", self.timeout).decode()

	def command(self, com): 
		self.tel.write(("%s\r\n" % com).encode()) 
		return self.read_data()


def main():
	global HOST, PORT
	args = sys.argv

	filename = args[1]

	try:
		addr = '0x%08x'%int(args[2],0)
	except Exception:
			tb = traceback.format_exc()
			logging.info('%s' % tb)
			sys.exit(0)
	if len(args) >= 4 :
		HOST = args[3]
	
	if len(args) >= 5 :
		PORT = int(args[4])
	
	tn = OOCDTelnet(HOST,PORT,TIMEOUT)
	logging.info('\n'+tn.command("poll"))
	logging.info('\n'+tn.command("reset halt"))
	logging.info('\n'+tn.command("flash probe 0"))
	#logging.info('\n'+tn.command("stm32f2x mass_erase 0"))
	logging.info('\n'+tn.command("flash write_image erase %s %s\n"%(filename,addr)))
	logging.info('\n'+tn.command("reset"))
	logging.info('\n'+tn.command("exit"))
	
	tn.close()

if __name__ == "__main__":
	main()
