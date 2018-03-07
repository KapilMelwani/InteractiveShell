#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
-Configurar nombre del switch
-Guardar configuracion: write memory
- CREAR VLAN:
	S1(config)# vlan 20
	S1(config-vlan)# name profesores
	S1(config-vlan)# exit

- ASIGNAR PUERTOS DE ACCESO 
	S1(config)# interface eth2
	S1(config-if)# switchport mode access
	S1(config-if)# switchport access vlan 10
	S1(config-if)# no shutdown
	S1(config-if)# end

- CONFIGURAR ENLACES TRONCALES
	S1(config)# interface eth0
	S1(config-if)# switchport mode trunk
	S1(config-if)# switchport trunk allowed vlan 10,20
	S1(config-if)# no shutdown
	S1(config-if)# end

- ASIGNAR INTERFAZ DE ADMIN EN LA VLAN 20
	S1(config)# interface vlan 20
	S1(config)# ip address 192.168.1.3 255.255.255.

- ENRUTAMIENTO ENTRE VLAN
	vyos@vyos# set interface ethernet eth0 vif 10 address 192.168.0.1/24
'''

from ishell.command import Command
from ishell.console import Console
from ishell.utils import _print

import subprocess
import getpass

console = Console("S1@LisaSwitch:~", '#')
user_name = "S1@LisaSwitch:~"
array_history = []
array_vlan_id = []
array_vlan_name = []

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class SwitchName(Command):
    name = []
    def run(self, line):
        array_history.append(line)
        args = line.split()
        command = ['switchname']
        if len(line) > 1:
            name = args[1:]
            console.prompt = str(name).strip('[]').strip('\'"')  + "@LisaSwitch:~"
            user_name = console.prompt
            print Colors.OKGREEN + "[OK] " + Colors.ENDC + "New session has been opened"
            console.loop()
            print Colors.OKBLUE + "Session closed" + Colors.ENDC
        else:
        	print Colors.FAIL + "[ERROR] " + Colors.ENDC + "Bad command use"

    def get_name(self):
        return self.name


class ConfigureSwitch(Command):
    configure_counter = 0
    def run(self,line):
        array_history.append(line)
        console.prompt = "(config)"
        console.loop()

class Vlan(Command):
    vlan_id = []
    def run(self,line):
        array_history.append(line)
        if console.prompt == "(config)":
            args = line.split()
            vlan_id = args[1:]
            str_vlan_id = str(vlan_id).strip('[]').strip('\'"')
            array_vlan_id.append(str_vlan_id)
            print Colors.OKGREEN + "[OK] " + Colors.ENDC + "Vlan " + str_vlan_id  + " has been created"
            console.prompt = "(config-vlan)"
            console.loop() 
            #llamar a funcion de vswitch.py
        else:
            print Colors.FAIL + "[ERROR] " + Colors.ENDC + "Bad command use"


class VlanName(Command):
    vlan_name = []
    def run(self,line):
        array_history.append(line)
        if console.prompt == "(config-vlan)":
            args = line.split()
            vlan_name = args[1:]
            str_vlan_name = str(vlan_name).strip('[]').strip('\'"')
            array_vlan_name.append(str_vlan_name)
            print Colors.OKGREEN + "[OK] " + Colors.ENDC + "Vlan name " + str_vlan_name  + " assigned"
        else:
            print Colors.FAIL + "[ERROR] " + Colors.ENDC + "Bad command use"


class ShowVlan(Command):
    def run(self,line):
        array_history.append(line)
        print "\tVLAN NAME\t\t VLAN ID"
        for i in range (len(array_vlan_name)):
            print "\t" + array_vlan_name[i] + ":" + "\t\t" + array_vlan_id[i] + "\n"

class Exit(Command):
    def run(self,line):
        array_history.append(line)
        if console.prompt == "(config-vlan)":
            console.prompt = "(config)"
            console.loop()
            console.exit()
        else:
            if console.prompt == "(config)":
                console.prompt = user_name
                console.loop()
                console.exit()

class History(Command):
    def run(self,line):
        for i in range (len(array_history)):
            print str(i) + array_history + "\n"
def main():
    switchname = SwitchName("switchname",help="Usage: switchname [name]")
    configureswitch = ConfigureSwitch("configure",help="Usage: configure to access to the switch configuration")
    vlan = Vlan("vlan",help="Usage: vlan [vlan id]")
    vlan_name = VlanName("name",help="Usage: name [vlan_name]")
    show_vlan = ShowVlan("show",help="Usage: show (shows all vlan created")
    exit = Exit("out",help="Usage: exit")
    history = History("history",help="Usage: history")
    console.addChild(configureswitch)
    console.addChild(switchname)
    console.addChild(vlan)
    console.addChild(vlan_name)
    console.addChild(exit)
    console.addChild(show_vlan)
    console.addChild(history)
    console.loop()
    print Colors.OKBLUE + "Bye" + Colors.ENDC

if __name__ == '__main__':
    main()