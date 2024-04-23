#!/usr/bin/python3
# -*- coding: utf-8 -*-
 
# ***
# flapcx25617% pip show asyncua
# Name: asyncua
# Version: 0.9.92
# ... python3
# Python 3.8.10 (default, Nov 26 2021, 20:14:08)
# [GCC 9.3.0] on linux
# ***
 
 
import asyncio
import datetime
import time
 
from asyncua import ua, Server
from asyncua.common.methods import uamethod
 
 
@uamethod
def func(parent, value):
   return value * 2
 
 
async def main():
   # setup our server
   server = Server()
   await server.init()
   server.set_endpoint('opc.tcp://0.0.0.0:4840')
    
   # setup our own namespace, not really necessary but should as spec
   uri = 'OPC_SIMULATION_SERVER'
   idx = await server.register_namespace(uri)
    
   # populating our address space
   # server.nodes, contains links to very common nodes like objects and root
   myobj = await server.nodes.objects.add_object(idx, 'Parameters')
   _Text = await myobj.add_variable(idx, 'Text', ' ')
   _Count = await myobj.add_variable(idx, 'Count', 0)
   _Value = await myobj.add_variable(idx, 'Value', 0)
   _Node = await myobj.add_variable(idx, 'Node', 0)
    
   # Set variable permissions to be readable and/or writable by clients
   await _Text.set_read_only()
   await _Count.set_read_only()
   await _Value.set_writable()
   await _Node.set_writable()

   await server.nodes.objects.add_method(ua.NodeId('ServerMethod', 2), ua.QualifiedName('ServerMethod', 2), func,
                                         [ua.VariantType.Int64], [ua.VariantType.Int64],[ua.VariantType.Int64])
   async with server:
       
      i = 0
      TEXT = ' '
       
      while True:
         # ***********
         # ***variable 'Text' start***
         if i == 1:
            TEXT = 'Hallo'
         if i == 2:
            TEXT = 'ich bin ein'
         if i == 3:
            TEXT = 'Python-OPCUA-Server'
         if i == 4:
            TEXT = 'auf einem stinknormalen'
         if i == 5:
            TEXT = 'Linux PC - flalxpcx25617'
         await _Text.write_value(TEXT)
         # ***variable 'Text' end***
         # ***********
         # ***variable 'Count' start***
         if i == 0:
            COUNT = 0
            COUNTlastCYCLE = -1
         else:
            if COUNTlastCYCLE < COUNT:
               COUNTlastCYCLE = COUNT
               COUNT = COUNT + 1
            if COUNTlastCYCLE > COUNT:
               COUNTlastCYCLE = COUNT
               COUNT = COUNT - 1
            if COUNT == 5:
               COUNTlastCYCLE = COUNT + 1
            if COUNT == -5:
               COUNTlastCYCLE = COUNT - 1
         await _Count.write_value(COUNT)
         # ***variable 'Count' end***
         # ***********
          
         await asyncio.sleep(5)
          
         # example for ... .get_value()
         # new_val = await myvar.get_value()
         await _Node.write_value(1*time.time())

         i = i + 1
         if i > 5:
            i = 1
 
 
if __name__ == '__main__':
   asyncio.run(main())