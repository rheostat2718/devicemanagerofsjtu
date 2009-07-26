#! /usr/bin/python
# -*- coding: utf-8 -*-
# CDDL HEADER START
#
# The contents of this file are subject to the terms of the
# Common Development and Distribution License (the "License").
# You may not use this file except in compliance with the License.
#
# You can obtain a copy of the license at usr/src/OPENSOLARIS.LICENSE
# or http://www.opensolaris.org/os/licensing.
# See the License for the specific language governing permissions
# and limitations under the License.
#
# When distributing Covered Code, include this CDDL HEADER in each
# file and include the License file at usr/src/OPENSOLARIS.LICENSE.
# If applicable, add the following below this CDDL HEADER, with the
# fields enclosed by brackets "[]" replaced with your own identifying
# information: Portions Copyright [yyyy] [name of copyright owner]
#
# CDDL HEADER END
#
# Copyright 2009 Sun Microsystems, Inc. All rights reserved.
# Use is subject to license terms.
#
# ident "@(#)ddu.py 1.26 09/01/05 SMI"
#

import sys
import os
import gnome
from xml.dom import minidom
from xml.dom import Node
import commands
import httplib,urllib

try:
  import pygtk
  pygtk.require("2.0")
except:
  print "Please install pyGTK or GTKv2 or set your PYTHONPATH correctly"
  sys.exit(1)

import gtk
import gtk.glade
import gobject
import cairo
import pango
import threading
from threading import *
import time
from time import gmtime, strftime
import math
import re
from xml.dom.minidom import Document
import httplib
import urllib,urllib2
import base64
import gettext
try:
	gettext.bindtextdomain('ddu','/usr/ddu/i18n')
	gettext.textdomain('ddu')
	gtk.glade.bindtextdomain('ddu','/usr/ddu/i18n')
except:
	pass
gtk.glade.textdomain('ddu')
_ = gettext.gettext


def insert_one_tag_into_buffer(textbuffer, name, *params):
	tag = gtk.TextTag(name)
	while(params):
        	tag.set_property(params[0], params[1])
        	params = params[2:]
	table = textbuffer.get_tag_table()
        if table.lookup("tag") is None:
		table.add(tag)
	return

def insert_col_info(name_ent,email_ent,server_com,manu_text,manu_modle,cpu_type,firmware_maker,bios_set,general_ent,inform_c):
	abspath="/usr/ddu"
	status,output=commands.getstatusoutput('/sbin/uname -p')
	bindir=abspath+'/bin/'+output
	
	textbuffer = inform_c.get_buffer()
	textbuffer.delete(textbuffer.get_start_iter(),textbuffer.get_end_iter())
	line_iter = textbuffer.get_iter_at_offset (0)


	line_iter = textbuffer.get_end_iter()

        textbuffer.insert_with_tags_by_name (line_iter,_("Manufacture name:"),"bold")
	textbuffer.insert(line_iter,str(manu_text.get_text().strip()))

	line_iter = textbuffer.get_end_iter()
        textbuffer.insert_with_tags_by_name (line_iter,"\nManufacture model:","bold")
	textbuffer.insert(line_iter,str(manu_modle.get_text().strip()))


	status,output=commands.getstatusoutput('isainfo -b')

	line_iter = textbuffer.get_end_iter()
        textbuffer.insert_with_tags_by_name (line_iter,"\n64 Bit:","bold")
	if output == '32':
		textbuffer.insert(line_iter,'False')
	elif output == '64':
		textbuffer.insert(line_iter,'True')


	status,output=commands.getstatusoutput('uname -a')
	line_iter = textbuffer.get_end_iter()
        textbuffer.insert_with_tags_by_name (line_iter,"\nOS version:","bold")
	textbuffer.insert(line_iter,str(output.strip()))
		
	
	status,output=commands.getstatusoutput('%s/dmi_info -C' % bindir)
	inpt=output.splitlines()
	line_iter = textbuffer.get_end_iter()
        textbuffer.insert_with_tags_by_name (line_iter,"\nCPU Type:","bold")
	textbuffer.insert(line_iter,str(inpt[0].split(':')[1].strip()))
	line_iter = textbuffer.get_end_iter()
        textbuffer.insert_with_tags_by_name (line_iter,"\nCPU Number:","bold")
	textbuffer.insert(line_iter,str(inpt[1].split(':')[1].strip()))
	line_iter = textbuffer.get_end_iter()
        textbuffer.insert_with_tags_by_name (line_iter,"\nNumber Of Cores Per Processor:","bold")
	textbuffer.insert(line_iter,str(inpt[2].split(':')[1].strip()))
	line_iter = textbuffer.get_end_iter()
        textbuffer.insert_with_tags_by_name (line_iter,"\nNumber Of Threads Per Processor:","bold")
	textbuffer.insert(line_iter,str(inpt[3].split(':')[1].strip()))

	line_iter = textbuffer.get_end_iter()
        textbuffer.insert_with_tags_by_name (line_iter,"\nBios/Firmware Maker:","bold")
	textbuffer.insert(line_iter,str(firmware_maker.get_text().strip()))


	line_iter = textbuffer.get_end_iter()
	textbuffer.insert_with_tags_by_name (line_iter,"\nprtconf -pv:\n","bold")
	status,output=commands.getstatusoutput('/usr/sbin/prtconf -pv')	
	textbuffer.insert(line_iter,output)

	line_iter = textbuffer.get_end_iter()
	textbuffer.insert_with_tags_by_name (line_iter,"\nprtdiag:\n","bold")
	status,output=commands.getstatusoutput('/usr/sbin/prtdiag')	
	textbuffer.insert(line_iter,output)

	line_iter = textbuffer.get_end_iter()
	textbuffer.insert_with_tags_by_name (line_iter,"\n\n","bold")
	status,output=commands.getstatusoutput('%s/dmi_info' % bindir)	
	textbuffer.insert(line_iter,output)

	return 



def insert_col(name_ent,email_ent,server_com,manu_text,manu_modle,cpu_type,firmware_maker,bios_set,general_ent,inform_c,dev_submit):
	abspath="/usr/ddu"
	status,output=commands.getstatusoutput('/sbin/uname -p')
	bindir=abspath+'/bin/'+output
	scriptsdir=abspath+'/scripts'
        model = server_com.get_model()
        active = server_com.get_active()
        server_inf=model[active][0]

	status,isa_output=commands.getstatusoutput('isainfo -b')

	status,os_output=commands.getstatusoutput('uname -a')
	
	status,dmic_output=commands.getstatusoutput('%s/dmi_info -C' % bindir)
	dmic_inpt=dmic_output.splitlines()

	textbuffer_g = general_ent.get_buffer()	
        startiter = textbuffer_g.get_start_iter()
        enditer = textbuffer_g.get_end_iter()

	status,prt_output=commands.getstatusoutput('/usr/sbin/prtconf -pv')	

	status,prtd_output=commands.getstatusoutput('/usr/sbin/prtdiag')	

	status,dmi_output=commands.getstatusoutput('%s/dmi_info' % bindir)	

	doc = Document()
	
	HCLSubmittal = doc.createElement("HCLSubmittal")
	doc.appendChild(HCLSubmittal)

	tierLevel = doc.createElement("tierLevel")
	HCLSubmittal.appendChild(tierLevel)
	
	tierLevelText = doc.createTextNode("3")
	tierLevel.appendChild(tierLevelText)

	submittalType = doc.createElement("submittalType")
	HCLSubmittal.appendChild(submittalType)

	submittalTypeText = doc.createTextNode("system")
	submittalType.appendChild(submittalTypeText)	


	entryType = doc.createElement("entryType")
	HCLSubmittal.appendChild(entryType)

	entryTypeText = doc.createTextNode(server_inf)
	entryType.appendChild(entryTypeText)	

	mfg = doc.createElement("mfg")
	HCLSubmittal.appendChild(mfg)

	mfgText = doc.createTextNode(manu_text.get_text())
	mfg.appendChild(mfgText)	

	model = doc.createElement("model")
	HCLSubmittal.appendChild(model)

	modelText = doc.createTextNode(manu_modle.get_text())
	model.appendChild(modelText)	

	osRevision = doc.createElement("osRevision")
	HCLSubmittal.appendChild(osRevision)

	osRevisionText = doc.createTextNode(os_output)
	osRevision.appendChild(osRevisionText)	

	
	cpuType = doc.createElement("cpuType")
	HCLSubmittal.appendChild(cpuType)

	cpuTypeText = doc.createTextNode(dmic_inpt[0].split(':')[1])
	cpuType.appendChild(cpuTypeText)	

	numCPU = doc.createElement("numCPU")
	HCLSubmittal.appendChild(numCPU)

	numCPUText = doc.createTextNode(dmic_inpt[1].split(':')[1])
	numCPU.appendChild(numCPUText)	


	patchesTested = doc.createElement("patchesTested")
	HCLSubmittal.appendChild(patchesTested)

	chipSet = doc.createElement("chipSet")
	HCLSubmittal.appendChild(chipSet)

	sixty_four_bit = doc.createElement("sixty_four_bit")
	HCLSubmittal.appendChild(sixty_four_bit)

	sixty_four_bitText = doc.createTextNode(str(isa_output=='64'))
	sixty_four_bit.appendChild(sixty_four_bitText)	


	firmware = doc.createElement("biosMaker")
	HCLSubmittal.appendChild(firmware)

	firmwareText = doc.createTextNode(firmware_maker.get_text())
	firmware.appendChild(firmwareText)	


	biosSettings = doc.createElement("biosSettings")
	HCLSubmittal.appendChild(biosSettings)


	boardRevLvl = doc.createElement("boardRevLvl")
	HCLSubmittal.appendChild(boardRevLvl)

	driverName = doc.createElement("driverName")
	HCLSubmittal.appendChild(driverName)

	driverVersion = doc.createElement("driverVersion")
	HCLSubmittal.appendChild(driverVersion)

	techType = doc.createElement("techType")
	HCLSubmittal.appendChild(techType)

	cardType = doc.createElement("cardType")
	HCLSubmittal.appendChild(cardType)


	driverInfo = doc.createElement("driverInfo")
	HCLSubmittal.appendChild(driverInfo)


	testSuite = doc.createElement("testSuite")
	HCLSubmittal.appendChild(testSuite)
	testSuiteText = doc.createTextNode('False')
	testSuite.appendChild(testSuiteText)	


	testResults = doc.createElement("testResults")
	HCLSubmittal.appendChild(testResults)

	testLevel = doc.createElement("testLevel")
	HCLSubmittal.appendChild(testLevel)
	testLevelText = doc.createTextNode(str(0))
	testLevel.appendChild(testLevelText)
	

	genNotes = doc.createElement("genNotes")
	HCLSubmittal.appendChild(genNotes)
	genNotesText = doc.createTextNode(textbuffer_g.get_text(startiter, enditer))
	genNotes.appendChild(genNotesText)

	numComponents = doc.createElement("numComponents")
	HCLSubmittal.appendChild(numComponents)
	numComponentsText = doc.createTextNode(str(0))
	numComponents.appendChild(numComponentsText)


	sysComponents = doc.createElement("sysComponents")
	sysComponents.setAttribute("number", "0")
	HCLSubmittal.appendChild(sysComponents)

	prtConfOutput = doc.createElement("prtConfOutput")
	HCLSubmittal.appendChild(prtConfOutput)
	prtConfOutputText = doc.createTextNode(str(prt_output))
	prtConfOutput.appendChild(prtConfOutputText)

	prtDiagOutput = doc.createElement("prtDiagOutput")
	HCLSubmittal.appendChild(prtDiagOutput)
	prtDiagOutputText = doc.createTextNode(str(prtd_output))
	prtDiagOutput.appendChild(prtDiagOutputText)
	
	dateSubmitted = doc.createElement("dateSubmitted")
	HCLSubmittal.appendChild(dateSubmitted)
	dateSubmittedText = doc.createTextNode(str(strftime("%Y-%m-%d", gmtime())))
	dateSubmitted.appendChild(dateSubmittedText)
	
	submitter = doc.createElement("submitter")
	HCLSubmittal.appendChild(submitter)

	submitterName = doc.createElement("submitterName")
	submitter.appendChild(submitterName)

	submitterNameText = doc.createTextNode(name_ent.get_text())
	submitterName.appendChild(submitterNameText)	

	submitterEmail = doc.createElement("submitterEmail")
	submitter.appendChild(submitterEmail)

	submitterEmailText = doc.createTextNode(email_ent.get_text())
	submitterEmail.appendChild(submitterEmailText)	

	emailPrivate = doc.createElement("emailPrivate")
	submitter.appendChild(emailPrivate)

	emailPrivateText = doc.createTextNode('True')
	emailPrivate.appendChild(emailPrivateText)

	submitterCompany = doc.createElement("submitterCompany")
	submitter.appendChild(submitterCompany)	

	country = doc.createElement("country")
	submitter.appendChild(country)	

	auditingNotes = doc.createElement("auditingNotes")
	HCLSubmittal.appendChild(auditingNotes)
	auditingNotesText = doc.createTextNode('Opensolaris DDU v1.2')
	auditingNotes.appendChild(auditingNotesText)

	systemDetails = doc.createElement("systemDetails")
	HCLSubmittal.appendChild(systemDetails)


	status,dmiS_output=commands.getstatusoutput('%s/dmi_info -S' % bindir)
	dmiS_inpt=dmiS_output.splitlines()

	system_inf = doc.createElement("system")
	systemDetails.appendChild(system_inf)


	product_inf = doc.createElement("product")
	system_inf.appendChild(product_inf)

	product_infText = doc.createTextNode(dmiS_inpt[2].split(':')[1])
	product_inf.appendChild(product_infText)


	manufacturer_inf = doc.createElement("manufacturer")
	system_inf.appendChild(manufacturer_inf)
	manufacturer_infText = doc.createTextNode(dmiS_inpt[1].split(':')[1])
	manufacturer_inf.appendChild(manufacturer_infText)

	boot_env = doc.createElement("BootFromHd")
	systemDetails.appendChild(boot_env)

	storage_env=doc.createElement("Storage")	
	systemDetails.appendChild(storage_env)

	zpool_env = doc.createElement("ZpoolStatus")
	storage_env.appendChild(zpool_env)

	zfs_env = doc.createElement("ZfsList")
	storage_env.appendChild(zfs_env)

	disk_env = doc.createElement("DiskInfo")
	storage_env.appendChild(disk_env)

	status,boot_output=commands.getstatusoutput('pfexec df / | grep ramdisk')
	if status == 0:
		boot_infText = doc.createTextNode("No")
	else:
		boot_infText = doc.createTextNode("Yes")
		status,zpool_output=commands.getstatusoutput('pfexec zpool status')
		zpool_envList = doc.createTextNode(zpool_output)
		zpool_env.appendChild(zpool_envList)
		status,zfs_output=commands.getstatusoutput('pfexec zfs list')
		zfs_envList = doc.createTextNode(zfs_output)
		zfs_env.appendChild(zfs_envList)

	boot_env.appendChild(boot_infText)

	status,dmiB_output=commands.getstatusoutput('%s/dmi_info -B' % bindir)
	dmiB_inpt=dmiB_output.splitlines()

	bios_inf = doc.createElement("bios")
	systemDetails.appendChild(bios_inf)

	vendor_inf = doc.createElement("vendor")
	bios_inf.appendChild(vendor_inf)
	vendor_infText = doc.createTextNode(dmiB_inpt[1].split(':')[1])
	vendor_inf.appendChild(vendor_infText)

	version_inf = doc.createElement("version")
	bios_inf.appendChild(version_inf)
	version_infText = doc.createTextNode(dmiB_inpt[2].split(':')[1])
	version_inf.appendChild(version_infText)

	releaseDate_inf = doc.createElement("releaseDate")
	bios_inf.appendChild(releaseDate_inf)
	releaseDate_infText = doc.createTextNode(dmiB_inpt[3].split(':')[1])
	releaseDate_inf.appendChild(releaseDate_infText)

	biosRevision_inf = doc.createElement("biosRevision")
	bios_inf.appendChild(biosRevision_inf)
	biosRevision_infText = doc.createTextNode(dmiB_inpt[4].split(':')[1])
	biosRevision_inf.appendChild(biosRevision_infText)

	firmwareRevision_inf = doc.createElement("firmwareRevision")
	bios_inf.appendChild(firmwareRevision_inf)
	firmwareRevision_infText = doc.createTextNode(dmiB_inpt[5].split(':')[1])
	firmwareRevision_inf.appendChild(firmwareRevision_infText)


	status,dmiM_output=commands.getstatusoutput('%s/dmi_info -M' % bindir)
	dmiM_inpt=dmiM_output.splitlines()

	motherboard_inf = doc.createElement("motherboard")
	systemDetails.appendChild(motherboard_inf)

	product_inf = doc.createElement("product")
	motherboard_inf.appendChild(product_inf)
	try:
		product_infText = doc.createTextNode(dmiM_inpt[1].split(':')[1])
		product_inf.appendChild(product_infText)
	except:
		pass


	manufacturer_inf = doc.createElement("manufacturer")
	motherboard_inf.appendChild(manufacturer_inf)

	try:	
		manufacturer_infText = doc.createTextNode(dmiM_inpt[2].split(':')[1])
		manufacturer_inf.appendChild(manufacturer_infText)
	except:
		pass

	version_inf = doc.createElement("version")
	motherboard_inf.appendChild(version_inf)
	
	try:
		version_infText = doc.createTextNode(dmiM_inpt[3].split(':')[1])
		version_inf.appendChild(version_infText)
	except:
		pass

	device_inf = doc.createElement("device")
	motherboard_inf.appendChild(device_inf)
	try:
		device_infText = doc.createTextNode(dmiM_inpt[4].split(':')[1])
		device_inf.appendChild(device_infText)
	except:
		pass


	Processor_inf = doc.createElement("Processor")
	systemDetails.appendChild(Processor_inf)

	status,dmiC_output=commands.getstatusoutput('%s/dmi_info -C' % bindir)	
	dmiC_inpt=dmiC_output.splitlines()

	cputype=doc.createElement("CpuType")
	Processor_inf.appendChild(cputype)
	cputypeText=doc.createTextNode(dmiC_inpt[0].split(':')[1])
	cputype.appendChild(cputypeText)

	cpunum=doc.createElement("CpuNumber")
	Processor_inf.appendChild(cpunum)
	cpunumText=doc.createTextNode(dmiC_inpt[1].split(':')[1])
	cpunum.appendChild(cpunumText)

	numberofCpP=doc.createElement("NumberOfCoresPerProcessor")
	Processor_inf.appendChild(numberofCpP)
	numberofCpPText=doc.createTextNode(dmiC_inpt[2].split(':')[1])
	numberofCpP.appendChild(numberofCpPText)

	numberofTpP=doc.createElement("NumberOfThreadsPerProcessor")
	Processor_inf.appendChild(numberofTpP)
	numberofTpPText=doc.createTextNode(dmiC_inpt[3].split(':')[1])
	numberofTpP.appendChild(numberofTpPText)


	try:
		for loop in range(int(dmiC_inpt[1].split(':')[1])):
			status,dmi_output=commands.getstatusoutput('%s/dmi_info' % bindir)	
			
			status,cpuN_inf=commands.getstatusoutput('%s/dmi_info | grep -n "Processor %s"' % (bindir,str(loop)))		
	
			dmiC_inpt=dmi_output.splitlines()		
			cpu_inf = doc.createElement("cpu")
			Processor_inf.appendChild(cpu_inf)
		
			socketType_inf = doc.createElement("socketType")
			cpu_inf.appendChild(socketType_inf)
			socketType_infText = doc.createTextNode(dmiC_inpt[int(cpuN_inf.split(':')[0])].split(':')[1])
			socketType_inf.appendChild(socketType_infText)

			manufacturer_inf = doc.createElement("manufacturer")
			cpu_inf.appendChild(manufacturer_inf)
			manufacturer_infText = doc.createTextNode(dmiC_inpt[int(cpuN_inf.split(':')[0])+1].split(':')[1])
			manufacturer_inf.appendChild(manufacturer_infText)

			voltage_inf = doc.createElement("voltage")
			cpu_inf.appendChild(voltage_inf)
			voltage_infText = doc.createTextNode(dmiC_inpt[int(cpuN_inf.split(':')[0])+2].split(':')[1])
			voltage_inf.appendChild(voltage_infText)

			externalClock_inf = doc.createElement("externalClock")
			cpu_inf.appendChild(externalClock_inf)
			externalClock_infText = doc.createTextNode(dmiC_inpt[int(cpuN_inf.split(':')[0])+3].split(':')[1])
			externalClock_inf.appendChild(externalClock_infText)

			maxSpeed_inf = doc.createElement("maxSpeed")
			cpu_inf.appendChild(maxSpeed_inf)
			maxSpeed_infText = doc.createTextNode(dmiC_inpt[int(cpuN_inf.split(':')[0])+4].split(':')[1])
			maxSpeed_inf.appendChild(maxSpeed_infText)

			currentSpeed_inf = doc.createElement("currentSpeed")
			cpu_inf.appendChild(currentSpeed_inf)
			currentSpeed_infText = doc.createTextNode(dmiC_inpt[int(cpuN_inf.split(':')[0])+5].split(':')[1])
			currentSpeed_inf.appendChild(currentSpeed_infText)

	except:
		pass

	status,dmiM_output=commands.getstatusoutput('%s/dmi_info -m' % bindir)	
	dmiM_inpt=dmiM_output.splitlines()

	status,dmiMS_output=commands.getstatusoutput('%s/dmi_info -m | grep -n "Memory Subsystem"' % bindir)	
	dmiMS_inpt=dmiMS_output.splitlines()

	try:
		for loop in range(len(dmiMS_inpt)):
			memory_inf = doc.createElement("memory")
			systemDetails.appendChild(memory_inf)	
		
			usedFunction_inf = doc.createElement("usedFunction")
			memory_inf.appendChild(usedFunction_inf)
			usedFunction_infText = doc.createTextNode(dmiM_inpt[int(dmiMS_inpt[int(loop)].split(':')[0])].split(':')[1])
			usedFunction_inf.appendChild(usedFunction_infText)
	
			eccSupport_inf = doc.createElement("eccSupport")
			memory_inf.appendChild(eccSupport_inf)
			eccSupport_infText = doc.createTextNode(dmiM_inpt[int(dmiMS_inpt[int(loop)].split(':')[0])+1].split(':')[1])
			eccSupport_inf.appendChild(eccSupport_infText)

			maxMemoryCapacity_inf = doc.createElement("maxMemoryCapacity")
			memory_inf.appendChild(maxMemoryCapacity_inf)
			maxMemoryCapacity_infText = doc.createTextNode(dmiM_inpt[int(dmiMS_inpt[int(loop)].split(':')[0])+2].split(':')[1])
			maxMemoryCapacity_inf.appendChild(maxMemoryCapacity_infText)

	
			for subloop in range(int(dmiM_inpt[int(dmiMS_inpt[int(loop)].split(':')[0])+3].split(':')[1])):
				device_inf = doc.createElement("device")
				memory_inf.appendChild(device_inf)
			
				index=4
				while dmiM_inpt[int(dmiMS_inpt[int(loop)].split(':')[0])+int(index)].find(str("Memory Device " + str(subloop))) == -1:
					index=index+1
			

				deviceLocator_inf = doc.createElement("deviceLocator")
				device_inf.appendChild(deviceLocator_inf)

				totalWidth_inf = doc.createElement("totalWidth")
				device_inf.appendChild(totalWidth_inf)

				dataWidth_inf = doc.createElement("dataWidth")
				device_inf.appendChild(dataWidth_inf)

				installedSize_inf = doc.createElement("installedSize")
				device_inf.appendChild(installedSize_inf)

				deviceType_inf = doc.createElement("deviceType")
				device_inf.appendChild(deviceType_inf)


				speed_inf = doc.createElement("speed")
				device_inf.appendChild(speed_inf)


				if dmiM_inpt[int(dmiMS_inpt[int(loop)].split(':')[0])+int(index)+1].find('Not Installed') == -1:
					deviceLocator_infText=doc.createTextNode(dmiM_inpt[int(dmiMS_inpt[int(loop)].split(':')[0])+int(index)+1])
					deviceLocator_inf.appendChild(deviceLocator_infText)

					totalWidth_infText=doc.createTextNode(dmiM_inpt[int(dmiMS_inpt[int(loop)].split(':')[0])+int(index)+2])
					totalWidth_inf.appendChild(totalWidth_infText)
	
					dataWidth_infText=doc.createTextNode(dmiM_inpt[int(dmiMS_inpt[int(loop)].split(':')[0])+int(index)+3])
					dataWidth_inf.appendChild(dataWidth_infText)
			
					installedSize_infText=doc.createTextNode(dmiM_inpt[int(dmiMS_inpt[int(loop)].split(':')[0])+int(index)+4])
					installedSize_inf.appendChild(installedSize_infText)

					deviceType_infText=doc.createTextNode(dmiM_inpt[int(dmiMS_inpt[int(loop)].split(':')[0])+int(index)+5])
					deviceType_inf.appendChild(deviceType_infText)

					speed_infText=doc.createTextNode(dmiM_inpt[int(dmiMS_inpt[int(loop)].split(':')[0])+int(index)+6])
					speed_inf.appendChild(speed_infText)


	except:
		pass

	pciDevices = doc.createElement("pciDevices")
	HCLSubmittal.appendChild(pciDevices)
	
	for category, controllers in dev_submit.iteritems():
		if len(controllers)>0:
			for pci_controller in controllers:
				devices = doc.createElement("devices")
				pciDevices.appendChild(devices)
				status,detail_output=commands.getstatusoutput('%s/det_info.sh %s CLASS=%s' % (scriptsdir,pci_controller[0],pci_controller[1]))
				if status == 0:
					file = open(detail_output,"r")

					vendor_id=""
					device_id=""
					class_code=""
					subvendor_id=""
					subdevice_id=""
					revision_id=""
					driver_name=""
					driver_status=""
					disk_status=""
					instance=""
					for line in file.readlines():
						p = re.compile('^vendor-id')					
						if p.search(line):
							vendor_id=str(line.split(':')[1]).strip()


						p = re.compile('^device-id')					
						if p.search(line):
							device_id=str(line.split(':')[1]).strip()
						
						class_code = str(pci_controller[1]).strip()

						p = re.compile('^subsystem-vendor-id')					
						if p.search(line):
							subvendor_id=str(line.split(':')[1]).strip()
						
						p = re.compile('^subsystem-id')					
						if p.search(line):
							subdevice_id=str(line.split(':')[1]).strip()

						p = re.compile('^revision-id')					
						if p.search(line):
							revision_id=str(line.split(':')[1]).strip()

						p = re.compile('^driver\ name')					
						if p.search(line):
							driver_name=str(line.split(':')[1]).strip()
						
						p = re.compile('^driver\ state')					
						if p.search(line):
							driver_status=str(line.split(':')[1]).strip()

						p = re.compile('^DISK')					
						if p.search(line):
							disk_status="Yes"
						
						p = re.compile('^instance')					
						if p.search(line):
							instance=str(line.split(':')[1]).strip()	
					file.close()
					os.remove(detail_output)

					comName=doc.createElement("comName")
					devices.appendChild(comName)

					comNametext=doc.createTextNode(str(pci_controller[2]).strip())
					comName.appendChild(comNametext)

					comPath=doc.createElement("comPath")
					devices.appendChild(comPath)

					comPathtext=doc.createTextNode(str(pci_controller[0]).strip())
					comPath.appendChild(comPathtext)

						
					vendorId=doc.createElement("vendorId")
					devices.appendChild(vendorId)

					vendorIDtext=doc.createTextNode(vendor_id)
					vendorId.appendChild(vendorIDtext)
				
					deviceId=doc.createElement("deviceId")
					devices.appendChild(deviceId)

					deviceIdtext=doc.createTextNode(device_id)
					deviceId.appendChild(deviceIdtext)

					classCode=doc.createElement("classCode")
					devices.appendChild(classCode)

					classCodetext=doc.createTextNode(class_code)
					classCode.appendChild(classCodetext)

					subvendorId=doc.createElement("subVendorId")
					devices.appendChild(subvendorId)

					subVendorIdtext=doc.createTextNode(subvendor_id)
					subvendorId.appendChild(subVendorIdtext)

					subdeviceId=doc.createElement("subDeviceId")
					devices.appendChild(subdeviceId)

					subdeviceIdtext=doc.createTextNode(subdevice_id)
					subdeviceId.appendChild(subdeviceIdtext)

					revisionId=doc.createElement("revisionId")
					devices.appendChild(revisionId)

					revisionIdtext=doc.createTextNode(revision_id)
					revisionId.appendChild(revisionIdtext)

					drivername=doc.createElement("driverName")
					devices.appendChild(drivername)

					drivernametext=doc.createTextNode(driver_name)
					drivername.appendChild(drivernametext)

					driverstatus=doc.createElement("driverStatus")
					devices.appendChild(driverstatus)
					
					driverstatustext=doc.createTextNode(driver_status)
					driverstatus.appendChild(driverstatustext)

					driverInstance=doc.createElement("driverInstance")
					devices.appendChild(driverInstance)
					
					driverinstancetext=doc.createTextNode(instance)
					driverInstance.appendChild(driverinstancetext)




					if disk_status == "Yes":
						disk_status,diskdetail_output=commands.getstatusoutput('%s/hd_detect -c %s' % (bindir,pci_controller[0]))
						if disk_status == 0:
							output_lines=diskdetail_output.splitlines()
							for line in output_lines:
								disks=doc.createElement("disk")
								disk_env.appendChild(disks)

								diskdetail=doc.createElement("diskIndex")
								disks.appendChild(diskdetail)
								diskditailText=doc.createTextNode(str(line.split(":")[0]).strip())		
								diskdetail.appendChild(diskditailText)

								diskphyPath=doc.createElement("phyPath")
								disks.appendChild(diskphyPath)
								diskphyPathText=doc.createTextNode(str(line.split(":")[1]).strip())	
								diskphyPath.appendChild(diskphyPathText)					

								diskdevPath=doc.createElement("devPath")
								disks.appendChild(diskdevPath)
								diskdevPathText=doc.createTextNode(str(line.split(":")[2]).strip())	
								diskdevPath.appendChild(diskdevPathText)
							
	return doc



def insert_conf(ent1,ent2,ent3,ent4):
	abspath="/usr/ddu"
	status,output=commands.getstatusoutput('/sbin/uname -p')
	bindir=abspath+'/bin/'+output
	status,output=commands.getstatusoutput('%s/dmi_info -S' % bindir)
	inpt=output.splitlines()
	ent1.set_text(str(inpt[1].split(':')[1].strip()))
	ent2.set_text(str(inpt[2].split(':')[1].strip()))

	status,output=commands.getstatusoutput('%s/dmi_info -C' % bindir)
	inpt=output.splitlines()
	ent3.set_text(str(inpt[0].split(':')[1].strip()))

	status,output=commands.getstatusoutput('%s/dmi_info -B' % bindir)
	inpt=output.splitlines()
	ent4.set_text(str(inpt[1].split(':')[1].strip())+" Version:"+str(inpt[2].split(':')[1].strip())+" Release Date:"+str(inpt[3].split(':')[1].strip()))
	return

class _IdleObject(gobject.GObject):
	def __init__(self):
		gobject.GObject.__init__(self)

	def emit(self, *args):
		gobject.idle_add(gobject.GObject.emit,self,*args)
	
class Device_tree( threading.Thread, _IdleObject ):
	__gsignals__ =  {
		"clear":(gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, []),
		"append":(gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE,[gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_BOOLEAN]),
		"remove":(gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE,[]),
		"insert_after":(gobject.SIGNAL_RUN_LAST,gobject.TYPE_NONE,[gobject.TYPE_PYOBJECT,gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING,gobject.TYPE_STRING]),
		"get_path":(gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE,[gobject.TYPE_PYOBJECT])
	}
	myiter=None
	tempiter=None
	parentiter=None
	dev_tree={}
	def __init__(self, action = None):
		threading.Thread.__init__(self)
		_IdleObject.__init__(self)
		self.action = action
		self.finish = False
	def run( self ):
		abspath="/usr/ddu"
		status,output=commands.getstatusoutput('%s/scripts/probe.sh init' % abspath)
		self.dev_tree,self.certdata,self.dev_submit = self.insert_row(self.action)
		self.finish = True
			
	def insert_row(self,action=None):
		"""This function handle the TreeStore in the Treeview of the main window.
		The two parameters are: model point to the TreeStore and action indicate whether its a rescan action for refreshing the Treeview.
		The probe action for each category is stored in hdd.xml file for easy maintenance.
		The files for probe output:
		For Controller:
		F0:ID;F1:Parent ID;F2:Controller Name;F3:DeviceID;F4:ClassCode;F5:DevPath;F6:Drvier;F7:Instance;F8:Attach status;F9:VendorID
		For Device:
		F0:ID;F1:Parent ID;F2:Device Name;F3:Binding name;F4:DevPath;F5:Driver;F6:Instance;F7:Attach status
		"""
		
		dev_submit={}
		
		self.emit("clear")
			
		abspath="/usr/ddu"

		systemxml = minidom.parse('%s/data/hdd.xml' % abspath)

		category = systemxml.getElementsByTagName('category')
		abnormal_path=''
        
		for catelist in category:
			catename=catelist.attributes["name"].value
		
	
			self.emit("append",catename,'category',None,'','',False)

			First_iter=True
			dev_submit[catename]=[]

			probehook=catelist.getElementsByTagName('probe')[0]
		
			for probedata in probehook.childNodes:
				"""Get The probe script for each category"""
				if probedata.nodeType == Node.TEXT_NODE:
					if action == 'rescan':
						probecmd=abspath+'/'+probedata.data+' %s' % action
					else:
						probecmd=abspath+'/'+probedata.data

					
					status,output=commands.getstatusoutput(probecmd)
					if len(output) > 0:
						output_lines=output.splitlines()
						for line in output_lines:
							component_disc=line.split(':')
							if(component_disc[1] == ''):
								if component_disc[6] == 'unknown' :
									if (len(component_disc) > 10) and (component_disc[10] == '0') and (component_disc[11] != ''):
										if First_iter == True:
											self.emit("remove")
											catename=catelist.attributes["name"].value
											self.emit("append",catename,component_disc[0],None,component_disc[2],'Missing:[driver available]',True)

										else:
											self.emit("insert_after",self.myiter,None,'',component_disc[0],None,component_disc[2],'Missing:[driver available]',True)
											time.sleep(1)
																				
									elif (len(component_disc) > 10) and (component_disc[10] == '0') and (component_disc[11] == ''):
										if First_iter == True:
											self.emit("remove")
											catename=catelist.attributes["name"].value

											self.emit("append",catename,component_disc[0],None,component_disc[2],'Missing:[driver unavailable]',True)
											

										else:
											self.emit("insert_after",self.myiter,None,'',component_disc[0],None,component_disc[2],'Missing:[driver unavailable]',True)
											time.sleep(1)
											

									elif (len(component_disc) > 10) and (component_disc[10] == '1'):
										if First_iter == True:
											self.emit("remove")
											catename=catelist.attributes["name"].value
											self.emit("append",catename,component_disc[0],None,component_disc[2],'Missing:[]',True)
										else:
											self.emit("insert_after",self.myiter,None,'',component_disc[0],None,component_disc[2],'Missing:[]',True)
											time.sleep(1)

									elif (len(component_disc) > 10) and (component_disc[10] == '3') and (component_disc[11] != ''):
										if First_iter == True:
											self.emit("remove")
											catename=catelist.attributes["name"].value
											self.emit("append",catename,component_disc[0],None,component_disc[2],'Missing:[third-party]',True)
										
										else:
											self.emit("insert_after",self.myiter,None,'',component_disc[0],None,component_disc[2],'Missing:[third-party]',True)
											time.sleep(1)
											
									else:	
										if First_iter == True:
											self.emit("remove")
											catename=catelist.attributes["name"].value
											self.emit("append",catename,component_disc[0],None,component_disc[2],'Missing:[]',True)

										else:
											self.emit("insert_after",self.myiter,None,'',component_disc[0],None,component_disc[2],'Missing:[]',True)
											time.sleep(1)

									if abnormal_path == '':
										if First_iter == True:
											self.emit("get_path",self.myiter)
											abnormal_path=self.myiter
										else:
											self.emit("get_path",self.tempiter)
											abnormal_path=self.tempiter

								elif (int(component_disc[7]) < 0) and (component_disc[8] == 'Detached' ):
									if First_iter == True:
										self.emit("remove")

										catename=catelist.attributes["name"].value
										self.emit("append",catename,component_disc[0],None,component_disc[2],str("Misconfigured:["+component_disc[6]+"]"),True)

									else:
										self.emit("insert_after",self.myiter,None,'',component_disc[0],None,component_disc[2],str("Misconfigured:["+component_disc[6]+"]"),True)
										time.sleep(1)

									if abnormal_path == '':
										if First_iter == True:
											self.emit("get_path",self.myiter)
											abnormal_path=self.myiter
											
										else:
											self.emit("get_path",self.tempiter)
											abnormal_path=self.tempiter
								else:
									if First_iter == True:
										self.emit("remove")
										catename=catelist.attributes["name"].value
										self.emit("append",catename,component_disc[0],None,component_disc[2],component_disc[6],False)
									else:
										self.emit("insert_after",self.myiter,None,'',component_disc[0],None,component_disc[2],component_disc[6],False)
										time.sleep(1)

								if First_iter == True:
									self.dev_tree[component_disc[0]]=[self.myiter,line,'c']
								else:
									self.dev_tree[component_disc[0]]=[self.tempiter,line,'c']				
								dev_submit[catename].append((component_disc[5],component_disc[4],component_disc[2]))
								First_iter = False	
							else:
								self.parentiter=self.dev_tree[component_disc[1]][0]								
								self.emit("insert_after",self.parentiter,None,'',component_disc[0],None,component_disc[2],component_disc[5],False)
								time.sleep(1)
								self.dev_tree[component_disc[0]]=[self.tempiter,line,'d']
								dev_submit[catename].append((component_disc[4],"",component_disc[2]))
					else:
						self.emit("remove")

		"""Get The driver handling script"""
		certhook=systemxml.getElementsByTagName('trydrv')[0]
		for certdata in certhook.childNodes:
			if certdata.nodeType == Node.TEXT_NODE:
				pass
		return self.dev_tree,certdata.data,dev_submit
  

class HDDgui:
    """
    HDDgui class represents all the device information
    main Variables:
    __dev_tree representens the tree information for treeview
    __disp_data represents the selected node in treevire
    __dev_tree_back used for the animation displaying of the statistics pie
    __certdata try driver action
    """	
    __dev_tree={}
    __disp_data=''
    __dev_tree_back={}
    __certdata=''
    __rescan=False
    __success=False
    detail_inf_run = None
    myiter=None
    tempiter=None
    abnormal_path=''
	
    def __init__(self):
	self.abspath="/usr/ddu"
	xmlpath=self.abspath+"/data/hdd.glade"
	xml = gtk.glade.XML(xmlpath,root='topbox_main',domain='ddu')
	self.window = xml.get_widget('topbox_main')
	self.window.connect("destroy",self.main_destroy)

	self.window.set_default_size(630,700)

	self.window.set_resizable(True)


	"""devtree_view is the area for displaying the device tree"""	
	self.devtreeview=xml.get_widget('devtree_view')

        self.devtreemodel=gtk.ListStore(gtk.gdk.Pixbuf,gobject.TYPE_STRING,gobject.TYPE_STRING,gtk.gdk.Pixbuf,gobject.TYPE_STRING,gobject.TYPE_STRING,'gboolean')


        self.devtreeview.set_model(self.devtreemodel)
        self.devtreeview.set_headers_visible(True)

	menuxml=gtk.glade.XML(xmlpath,'detail_menu')
	self.popup_menu=menuxml.get_widget('detail_menu')
	self.detail_information=menuxml.get_widget('detail_information')
	self.install_driver=menuxml.get_widget('install_driver')
	self.install_all_missing_driver=menuxml.get_widget('install_all_missing_driver')
	self.power_management=menuxml.get_widget('power_management')

	self.detail_information.connect('activate',self.on_detail_activate)

	self.install_all_missing_driver.connect('activate',self.on_install_missing_activate)

	self.devtreeview.connect('button-press-event',self.on_popup_menu)
	
	col0 = gtk.TreeViewColumn()
        col0.set_title(_('Types'))
	col0.set_property("alignment", 0.5)
        render_pixbuf0 = gtk.CellRendererPixbuf()
	render_pixbuf0.set_property('cell-background', 'pink')
        col0.pack_start(render_pixbuf0, expand=False)
        col0.add_attribute(render_pixbuf0, 'pixbuf', 0)
	col0.add_attribute(render_pixbuf0, 'cell_background_set', 6)


        render_text0 = gtk.CellRendererText()
	render_text0.set_property('cell-background', 'pink')
        col0.pack_start(render_text0, expand=True)
        col0.add_attribute(render_text0, 'text', 1)
	col0.add_attribute(render_text0, 'cell_background_set', 6)


	render_key1 = gtk.CellRendererText()
	render_key1.set_property('visible',False)
	col0.pack_start(render_key1, expand=True)
        col0.add_attribute(render_key1, 'text', 2)

	col0.set_resizable(True)


	col1 = gtk.TreeViewColumn()
        col1.set_title(_('Device'))
	col1.set_property("alignment", 0.5)
        render_pixbuf0 = gtk.CellRendererPixbuf()
	render_pixbuf0.set_property('cell-background', 'pink')
        col1.pack_start(render_pixbuf0, expand=False)

        col1.add_attribute(render_pixbuf0, 'pixbuf', 3)
	col1.add_attribute(render_pixbuf0, 'cell_background_set', 6)

        render_text1 = gtk.CellRendererText()
	render_text1.set_property('cell-background', 'pink')
        col1.pack_start(render_text1, expand=True)
	render_text1.set_property('xalign', 0)
        col1.add_attribute(render_text1, 'text', 4)
	col1.add_attribute(render_text1, 'cell_background_set', 6)

	col1.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
	col1.set_expand(True)
	col1.set_resizable(True)

	col2 = gtk.TreeViewColumn()
        col2.set_title(_('Driver'))
	col2.set_property("alignment", 0.5)

        render_text0 = gtk.CellRendererText()
	render_text0.set_property('cell-background', 'pink')
	render_text0.set_property('xalign', 0.5)
        col2.pack_start(render_text0, expand=True)
        col2.add_attribute(render_text0, 'text', 5)
	col2.add_attribute(render_text0, 'cell_background_set', 6)
	col2.set_resizable(True)

        self.devtreeview.append_column(col0)
        self.devtreeview.append_column(col1)
        self.devtreeview.append_column(col2)

	self.devtreeview.expand_all()

	self.scrolledwindow_dev=xml.get_widget('scrolledwindow_dev')	

	
	self.devtreeview.show()
	self.scrolledwindow_dev.show()

	selection=self.devtreeview.get_selection()
	selection.set_mode(gtk.SELECTION_SINGLE)
        selection.connect('changed',self.on_selection_changed)

	"""rescan_clicked handle the rescan action"""
	self.rescan_button = xml.get_widget('button_rescan')
	self.rescan_button.connect("clicked", self.rescan_clicked)


	close_button = xml.get_widget('button_close')
	close_button.connect("clicked", gtk.main_quit)	

	"""drv_clicked handle the drv installation action"""
	self.drv_button = xml.get_widget('button_drv_detect')
	self.drv_button.connect("clicked", self.drv_clicked)
	self.drv_button.set_sensitive(True)

	self.help_button = xml.get_widget('help_button')
	self.help_button.connect("clicked", self.help_clicked)

	self.submit_button = xml.get_widget('button_submit')
	self.submit_button.connect("clicked", self.submit_clicked)

	ag = gtk.AccelGroup()
	self.window.add_accel_group(ag)

	self.rescan_button.add_accelerator("clicked", ag, ord('r'), gtk.gdk.MOD1_MASK,gtk.ACCEL_VISIBLE)
	close_button.add_accelerator("clicked", ag, ord('c'), gtk.gdk.MOD1_MASK,gtk.ACCEL_VISIBLE)
	self.drv_button.add_accelerator("clicked", ag, ord('i'), gtk.gdk.MOD1_MASK,gtk.ACCEL_VISIBLE)
	self.submit_button.add_accelerator("clicked", ag, ord('s'), gtk.gdk.MOD1_MASK,gtk.ACCEL_VISIBLE)

	
	self.dev_view=xml.get_widget("dev_view")
	self.hbox_msg=xml.get_widget("hbox_msg")

	self.dev_viewport=xml.get_widget("dev_viewport")
	self.devstatview=xml.get_widget("dev_stat")
	self.devstatview.set_size_request(30,0)
	self.devstatview.connect('expose-event',self.drawstat)
	self.dev_text=xml.get_widget("dev_text")

	self.statusbar=xml.get_widget("statusbar1")
	context_id = self.statusbar.get_context_id("feedback alias")
	self.statusbar.push(context_id,_("Feedback alias:driver-utility-feedback@sun.com"))
	

        def size_allocate_cb(wid, allocation):
	    pass

	self.window.connect('size-allocate', size_allocate_cb)


	self.rescan_button.emit("clicked")

	self.window.show_all()
	return

    def model_clear(self, thread):
	self.devtreemodel.clear()

    def model_append(self, thread, catename, category, data1, data2, data3, condition):
	iconfile0 = gtk.gdk.pixbuf_new_from_file('%s/data/%s.png' %(self.abspath,catename))
	self.myiter=self.devtreemodel.append([iconfile0,_(catename),category,data1,data2,data3,condition=="True"])

	self.rescan_thread.myiter=self.devtreemodel.get_path(self.myiter)

    def model_remove(self, thread):
	self.devtreemodel.remove(self.devtreemodel.get_iter(self.rescan_thread.myiter))


    def model_insert_after(self, thread, insert_iter,data1, data2, data3, data4, data5, data6, condition):
	insert_iter=self.devtreemodel.get_iter(insert_iter)
	self.tempiter=self.devtreemodel.insert_after(insert_iter,[data1,data2,data3,data4,data5,data6,condition=="True"])
	self.rescan_thread.tempiter=self.devtreemodel.get_path(self.tempiter)

    def model_getpath(self, thread, myiter):
#	self.abnormal_path=self.devtreemodel.get_path(myiter)
	self.abnormal_path=myiter

    def main_destroy(self, widget, data = None):
	if self.rescan_thread != None:
		self.rescan_thread = None
	gtk.main_quit()
	

    def on_popup_menu(self, item_tree, event=None):
	model, iter1 = item_tree.get_selection().get_selected()

	if event:
		if event.button != 3:
			return
	        if iter1 != None:
                	data = model.get_value(iter1, 2)
	                if data == 'category':
				return
		button = event.button
		event_time = event.time
		info = item_tree.get_path_at_pos(int(event.x), int(event.y))
		if info != None:
			self.detail_information.set_sensitive(True)
			self.install_all_missing_driver.set_sensitive(True)
			path, col, cellx, celly = info
			item_tree.grab_focus()
			item_tree.set_cursor(path, col, 0)
		else:
			self.detail_information.set_sensitive(False)
			self.install_all_missing_driver.set_sensitive(False)			
	else:
		path = model.get_path(iter1)
		button = 0
		event_time = 0
		item_tree.grab_focus()
		item_tree.set_cursor(path, item_tree.get_columns()[0], 0)

	
	self.popup_menu.popup(None, None, None, button, event.time)	
        return True

    def on_detail_activate(self, menu):
	model,iter = self.devtreeview.get_selection().get_selected()

	data = model.get_value(iter, 2)

	if data != 'category':
		tobe_handle = self.__dev_tree[data]
		disp_collection=tobe_handle[1].split(':')

		if tobe_handle != '':
			if tobe_handle[2] == 'c':
				devpath=str(disp_collection[5])
				classcode=str(disp_collection[4])
				device=str(disp_collection[2])
				if len(disp_collection) > 10:
					driver_info=str(disp_collection[11])
				else:
					driver_info=''
			elif tobe_handle[2] == 'd':
				devpath=str(disp_collection[4])
				device=str(disp_collection[2])
				classcode=''
				driver_info=''
			abspath="/usr/ddu"
			scriptsdir=abspath+'/scripts'
			status,detail_output=commands.getstatusoutput('%s/det_info.sh %s CLASS=%s' % (scriptsdir,devpath,classcode))
			if status == 0:
				self.detail_inf_run=detail_inf(detail_output,driver_info,device,fg='reload')
	else:
		return
	return


    def on_install_missing_activate(self, menu):
	disp_collection=self.__disp_data[1].split(':')	
	if len(disp_collection) > 10:
		if disp_collection[1] == '' :
			if disp_collection[6] == 'unknown':		
				if (disp_collection[10] == '1'):
					Inst=Message_Box(self.window,_('Install Driver'),_('Driver not installed'),_('The repository is currently unavailable'))
					Inst.run()
				elif (disp_collection[10] == '0') and (disp_collection[11] == ''):
					Inst=Message_Box(self.window,_('Install Driver'),_('Driver not installed'),_('Driver not found in the repository'))
					Inst.run()
				elif (disp_collection[10] == '3') and (disp_collection[11] != ''):
					status,driver_url=commands.getstatusoutput('/usr/bin/head -1 /tmp/%s.tmp' % disp_collection[11])
					Inst=Message_Box(self.window,_('Install Driver'),_('Third-party driver not installed!'),_("Install third-party driver manually"))
					Inst.run()					
				else:	
					Inst=Inst_drv(self.__certdata,disp_collection[11])
					Inst.run()
					self.rescan_button.emit("clicked")
			else:
				Inst=Message_Box(self.window,_('Install Driver'),_('Cannot proceed with the installation'),_('Driver already installed'))
				Inst.run()
		else:
			Inst=Message_Box(self.window,_('Install Driver'),_('Cannot proceed with the installation'),_('Driver already installed'))
			Inst.run()
	elif disp_collection[1] != '' :
		Inst=Message_Box(self.window,_('Install Driver'),_('Cannot proceed with the installation'),_('Driver already installed'))
		Inst.run()
	elif disp_collection[6] == 'unknown':
		Inst=Message_Box(self.window,_('Install Driver'),_('Driver not installed'),_('Refresh the device list and install the driver again'))
		Inst.run()
	else:
		Inst=Message_Box(self.window,_('Install Driver'),_('Cannot proceed with the installation'),_('Driver already installed'))
		Inst.run()
        return


    def submit_clicked(self,widget):
	submit=submit_dlg(self.dev_submit)
        return

    def help_clicked(self,widget):
	abspath="/usr/ddu"
	props = { gnome.PARAM_APP_DATADIR : abspath+'/help' }

	prog = gnome.program_init('ddu', '1.0', properties=props)
	gnome.help_display('ddu')
	return

    def drv_clicked(self,widget):
	"""This Function handles the driver installation issue, it will be implemtated later"""
	if self.abnormal_path == '':
		Inst=Message_Box(self.window,_('Install Driver'),_('No missing driver'),_('Do not need to install driver!'))
		Inst.run()
		return
	else:
		treeiter = self.devtreemodel.get_iter(self.abnormal_path)
		data=self.devtreemodel.get_value(treeiter, 2)
		disp_collection=self.__dev_tree[data][1].split(':')

		if len(disp_collection) > 10:
			Inst=Inst_all_drv(self.__certdata,self.__dev_tree)
			Inst.run()
			self.rescan_button.emit("clicked")
		else:
			Inst=Message_Box(self.window,_('Install Driver'),_('Driver not installed'),_('Refresh the device list and install the driver again'))
			Inst.run()
			return
	return



    def rescan_clicked(self,widget):
	self.__disp_data = ''
	self.draw_devdisc()

	self.devtreeview.collapse_all()
	self.devtreeview.queue_draw()
        while gtk.events_pending():
	        gtk.main_iteration()

	self.devtreeview.set_sensitive(False)

	self.__rescan = True
	self.dev_view.remove(self.hbox_msg)

	self.align = gtk.Alignment(0.5, 0.5, 1, 0)
	self.dev_pbar = gtk.ProgressBar()
	self.align.add(self.dev_pbar)
	self.dev_pbar.show()
	self.align.show()	

	self.dev_view.add(self.align)

	gobject.timeout_add(300, self.Profunc)

	self.rescan_button.set_sensitive(False)
	model=self.devtreemodel

	self.rescan_thread = Device_tree("rescan")
	self.rescan_thread.connect("clear",self.model_clear)
	self.rescan_thread.connect("append",self.model_append)
	self.rescan_thread.connect("remove",self.model_remove)
	self.rescan_thread.connect("insert_after",self.model_insert_after)
	self.rescan_thread.connect("get_path",self.model_getpath)

	self.rescan_thread.start()

        return

    def Profunc(self):
	if self.rescan_thread.finish == False:
		new_val = self.dev_pbar.get_fraction() + 0.01
		if new_val > 1.0:
			new_val=1.0
		self.dev_pbar.set_fraction(new_val)
	else:
		self.__dev_tree = self.rescan_thread.dev_tree
		self.__certdata = self.rescan_thread.certdata
#		self.abnormal_path = self.rescan_thread.abnormal_path
		self.dev_submit = self.rescan_thread.dev_submit
		
		selection=self.devtreeview.get_selection()
		self.devtreeview.expand_all()
		self.devtreeview.set_sensitive(True)

		if self.abnormal_path != '':
			self.devtreeview.scroll_to_cell(self.abnormal_path,None,True,0.5,0)
		self.__rescan = False

		self.dev_view.remove(self.align)

		self.hbox_msg = gtk.HBox(False, 0)
		self.dev_view.add(self.hbox_msg)
		self.dev_viewport=gtk.Viewport()
		self.dev_viewport.set_shadow_type(gtk.SHADOW_NONE)
		self.hbox_msg.pack_start(self.dev_viewport, False, False, 0)
		self.devstatview = gtk.DrawingArea()
		self.devstatview.set_size_request(30,0)
		self.devstatview.connect('expose-event',self.drawstat)
		self.dev_viewport.add(self.devstatview)

		self.dev_text=gtk.Label("")
		self.hbox_msg.pack_start(self.dev_text, False, False, 0)

		self.dev_view.show_all()
		self.rescan_button.set_sensitive(True)
			
	return self.__rescan


    def drawstat(self, widget,event):
	self.wid_get=widget
	self.event_c=event
        self.draw_stat()
	return


    def draw_stat(self):
	width, height = self.wid_get.window.get_size()
	crd = self.wid_get.window.cairo_create()

	yes_driver=0
	no_driver=0
	all_driver=0
	for iternum,iterdata in self.__dev_tree.iteritems():
		disp_type=iterdata[2]
		disp_collection=iterdata[1].split(':')	
		if disp_type == 'c':
			if  disp_collection[6] == 'unkonwn' or ((int(disp_collection[7]) < 0) and (disp_collection[8] == 'Detached')):
					no_driver+=1
			else:
					yes_driver+=1
		all_driver+=1



	if self.__rescan == False:
		drawable = self.wid_get.window
		drawable.clear()		
		
		if no_driver > 0:
			iconfile = gtk.gdk.pixbuf_new_from_file('%s/data/Missing-1.png' % self.abspath)	
		else:
			iconfile = gtk.gdk.pixbuf_new_from_file('%s/data/info.png' % self.abspath)				
        	crd.set_source_pixbuf(iconfile,0,15)
		crd.paint()
		crd.stroke()

	status_str=str(_("<b>Driver Problems: %s</b>") % str(no_driver))

	self.dev_text.set_markup(status_str)

	if no_driver == 0:
		self.drv_button.set_sensitive(False)

	return



    def draw_devdisc(self):
	if self.__disp_data != '':
		if self.__disp_data[2] == 'c':
			disp_collection=self.__disp_data[1].split(':')				
			if len(disp_collection) > 10:
				if disp_collection[10] == '1':
					self.drv_button.set_sensitive(True)
				elif disp_collection[10] == '0':
					if disp_collection[11] != '':
						self.drv_button.set_sensitive(True)
					else:
						self.drv_button.set_sensitive(True)
				else:
					self.drv_button.set_sensitive(True)
			else:
				self.drv_button.set_sensitive(False)

		elif self.__disp_data[2] == 'd':
			disp_device=self.__disp_data[1].split(':')
			self.drv_button.set_sensitive(True)
	else:
		pass
	return


    def on_selection_changed(selection,*args):
	"""This function handle the selection action in the device treeview
	   It just set the __disp_data which will be used for drawdev/draw_devdisc
	"""
	abspath="/usr/ddu"
	scriptsdir=abspath+'/scripts'

	model,iter=args[0].get_selected ()

	if iter != None:
		data=model.get_value(iter, 2)
		if data != 'category':	
			selection.__disp_data=selection.__dev_tree[data]
			disp_collection=selection.__dev_tree[data][1].split(':')
			if selection.__dev_tree[data][2] == "c":
				devpath=str(disp_collection[5])
				classcode=str(disp_collection[4])
				device=str(disp_collection[2])
				if len(disp_collection) > 10:
					driver_info=str(disp_collection[11])
				else:
					driver_info=''
			elif selection.__dev_tree[data][2] == "d":
				devpath=str(disp_collection[4])
				device=str(disp_collection[2])
				classcode=''
				driver_info=''
			try:			
				if selection.detail_inf_run.spam():
					status,detail_output=commands.getstatusoutput('%s/det_info.sh %s CLASS=%s' % (scriptsdir,devpath,classcode))
					selection.detail_inf_run=detail_inf(detail_output,driver_info,device)
			except:
				pass
		else:
			selection.__disp_data=''
			pass
	return


class Inst_drv:
    """This Class is used to show install driver progress"""
    __finish = False
    __success = False
    def __init__(self,action='',drv=''):
	self.drv=drv
	self.action=action
	self.abspath="/usr/ddu"
	gladepath=self.abspath+'/data/hdd.glade'
	xml = gtk.glade.XML(gladepath,'Inst_dri_dlg')
	self.inst_dlg=xml.get_widget('Inst_dri_dlg')

	self.label_inst=xml.get_widget('label_inst')
	self.label_list=xml.get_widget('label_list')
	self.progressbar_inst=xml.get_widget('progressbar_inst')
	self.button_ok=xml.get_widget('button_ok')
	self.inst_dlg.set_resizable(False)
	self.inst_dlg.connect('map_event', self.on_map_event)

    def run(self):
	self.inst_dlg.run()
	self.inst_dlg.destroy()

    def on_map_event(self, event, param):
	while gtk.gdk.events_pending():
		gtk.main_iteration(False)
	self.button_ok.set_sensitive(False)
	gobject.timeout_add(100, self.pro)
	gobject.timeout_add(10000, self.destroy_actor)	
	thread = threading.Thread(target=self.install_run)
	thread.start()
	
    
    def pro(self):
	if self.__finish == False:
		self.progressbar_inst.pulse()
	else:
		if self.__success == False:
			errmg = _("Installation Failed!")
			msg = _("")
		else:
			errmg = _("Installation Successful!")
			msg=_('Reboot your system after installing the driver\n')
			msg += _('This window will be closed in a few seconds')
		self.label_list.set_markup("<span foreground=\"#FF0000\">%s</span>" % errmg)
		self.label_inst.set_markup("<span foreground=\"#FF0000\">%s</span>" % msg)
		self.button_ok.set_sensitive(True)
	return not self.__finish

    def destroy_actor(self):
    	if self.__success == True:
		self.submit_dlg.destroy()
	return not self.__success


    def install_run(self):
	certcmd=self.abspath+"/"+self.action + ' %s' % self.drv
	self.status,self.output=commands.getstatusoutput(certcmd)

	if self.status != 0:
		self.__success = False
	else:
		self.__success = True
		self.__finish=True		
	self.__finish=True
	
	return self.status,self.output


class Inst_all_drv:
    """This Class is used to show install driver progress"""
    __finish = False
    __success = False
    def __init__(self,action='',dev_tree=''):
	self.dev_tree=dev_tree
	self.action=action
	self.abspath="/usr/ddu"
	gladepath=self.abspath+'/data/hdd.glade'
	xml = gtk.glade.XML(gladepath,'Inst_dri_dlg')
	self.inst_dlg=xml.get_widget('Inst_dri_dlg')

	self.label_inst=xml.get_widget('label_inst')
	self.label_list=xml.get_widget('label_list')
	self.progressbar_inst=xml.get_widget('progressbar_inst')
	self.button_ok=xml.get_widget('button_ok')
	self.button_ok.set_sensitive(False)
	self.inst_dlg.set_resizable(False)
	self.inst_dlg.connect('map_event', self.on_map_event)

    def run(self):
	self.inst_dlg.run()
	self.inst_dlg.destroy()

    def on_map_event(self, event, param):
	while gtk.gdk.events_pending():
		gtk.main_iteration(False)
	gobject.timeout_add(100, self.pro)	
	gobject.timeout_add(20000, self.destroy_actor)	
	thread = threading.Thread(target=self.install_run)
	thread.start()
	
    
    def pro(self):
	self.label_list.set_markup("<span foreground=\"#FF0000\">%s</span>" % self.msgstr)
	if self.__finish == False:
		self.progressbar_inst.pulse()
	else:
		self.msg=_('Reboot your system after installing the driver\n')
		self.label_inst.set_markup("<span foreground=\"#FF0000\">%s</span>" % self.msg)
		self.button_ok.set_sensitive(True)
	return not self.__finish
	
    def destroy_actor(self):
    	if self.__success == True:
		pass
	return not self.__success

    def install_run(self):
    	self.msgstr=''
	for iternum,iterdata in self.dev_tree.iteritems():
		disp_type=iterdata[2]
		disp_collection=iterdata[1].split(':')	
		if disp_type == 'c':
			if disp_collection[6] == 'unknown':		
				if (disp_collection[10] == '1'):
					self.msgstr += disp_collection[2]
					self.msgstr += ':\n'
					self.msgstr += _('The repository is currently unavailable')
					self.msgstr += "\n\n"
				elif (disp_collection[10] == '0') and (disp_collection[11] == ''):
					self.msgstr += disp_collection[2]
					self.msgstr += ':\n'
					self.msgstr += _('Driver not found in the repository')
					self.msgstr += "\n\n"
				elif (disp_collection[10] == '3') and (disp_collection[11] != ''):
					self.msgstr += disp_collection[2]
					self.msgstr += ':\n'
					self.msgstr += _('Install third-party driver manually')
					self.msgstr += "\n\n"
				else:	
					certcmd=self.abspath+"/"+self.action + ' %s' % disp_collection[11]
					self.status,self.output=commands.getstatusoutput(certcmd)
					if self.status != 0:
						self.msgstr += disp_collection[11]
						self.msgstr += ':\n'
						self.msgstr += _("Installation Failed!")
						self.msgstr += "\n\n"
					else:
						self.msgstr += disp_collection[11]
						self.msgstr += ':\n'
						self.msgstr += _("Installation Successful!")
						self.msgstr += "\n\n"						
	self.__finish=True
	self.__success=True
		
	return			

class submit_dlg:
    __finish = False
    __success = False
    def __init__(self,dev_submit):
	abspath="/usr/ddu"
	gladepath=abspath+'/data/hdd.glade'
	xml = gtk.glade.XML(gladepath,'submit_dlg')
	self.submit_dlg = xml.get_widget('submit_dlg')

	self.submit_dlg.connect("response",self.on_response)

	conn=httplib.HTTPSConnection("www.sun.com")
	try:
		conn.request("GET","/cgi-bin/sun/bigadmin/parseHCLTool.cgi")
		resp=conn.getresponse()
		if resp.status != 200:
			Inst=Message_Box(self.submit_dlg,_('Submit'),_('Submission failed'),_('The server is currently unavailable'))
			Inst.run()
			return
	except:
		Inst=Message_Box(self.submit_dlg,_('Submit'),_('Submission failed'),_('The server is currently unavailable'))
		Inst.run()
		return
	conn.close()

	"""Necessary text value"""
	self.submit_notebook=xml.get_widget("submit_notebook")

	self.pro_sub = xml.get_widget('pro_sub')
	self.submit_button = xml.get_widget('submit_button')
	self.submit_button.connect("clicked", self.act_submit)

	self.close_button = xml.get_widget('close_button')
	self.close_button.connect("clicked", lambda w:self.submit_dlg.destroy())

	self.save_button = xml.get_widget('submit_save')
	self.save_button.connect("clicked", self.act_save)

	self.manu_text=xml.get_widget('Manuf_name')
	self.manu_modle=xml.get_widget('Manuf_modle')
	self.manu_modle.set_sensitive(False)

	self.cpu_type=xml.get_widget('CPU_type')
	self.firmware_maker=xml.get_widget('Firmware_maker')
	insert_conf(self.manu_text,self.manu_modle,self.cpu_type,self.firmware_maker)

	self.name_ent=xml.get_widget('Name_ent')
	self.email_ent=xml.get_widget('Email_ent')

	self.server_com=xml.get_widget('Server_com')
	self.server_com.set_active(0)	

	self.bios_set=xml.get_widget('Bios_set')

	self.general_ent=xml.get_widget('General_ent')
	self.inform_c=xml.get_widget('Information_c')
	self.label_warning=xml.get_widget('label_warning')


	textbuffer = self.inform_c.get_buffer()
	insert_one_tag_into_buffer(textbuffer, "bold", "weight", pango.WEIGHT_BOLD) 
	
	ag = gtk.AccelGroup()
	self.submit_dlg.add_accel_group(ag)

	self.submit_button.add_accelerator("clicked", ag, ord('s'), gtk.gdk.MOD1_MASK,gtk.ACCEL_VISIBLE)
	self.close_button.add_accelerator("clicked", ag, ord('c'), gtk.gdk.MOD1_MASK,gtk.ACCEL_VISIBLE)
	self.save_button.add_accelerator("clicked", ag, ord('a'), gtk.gdk.MOD1_MASK,gtk.ACCEL_VISIBLE)

	self.label17=xml.get_widget('label17')
	self.label17.set_mnemonic_widget(self.server_com)

	self.label15=xml.get_widget('label15')
	self.label15.set_mnemonic_widget(self.manu_text)

	self.label11=xml.get_widget('label11')
	self.label11.set_mnemonic_widget(self.firmware_maker)

	self.label9=xml.get_widget('label9')
	self.label9.set_mnemonic_widget(self.cpu_type)

	self.label7=xml.get_widget('label7')
	self.label7.set_mnemonic_widget(self.inform_c)

	self.label12=xml.get_widget('label12')
	self.label12.set_mnemonic_widget(self.name_ent)

	self.label16=xml.get_widget('label16')
	self.label16.set_mnemonic_widget(self.email_ent)

	self.label19=xml.get_widget('label19')
	self.label19.set_mnemonic_widget(self.general_ent)

	insert_col_info(self.name_ent,self.email_ent,self.server_com,self.manu_text,self.manu_modle,self.cpu_type,self.firmware_maker,self.bios_set,self.general_ent,self.inform_c)

	self.submit_dlg.set_resizable(False)
	self.status = 1
	self.dev_submit=dev_submit
	self.submit_dlg.run()
	return

    def on_response(self,widget,response):
	if response == gtk.RESPONSE_DELETE_EVENT:
		self.submit_dlg.destroy()
	pass


    def act_save(self,widget):
	dialog = gtk.FileChooserDialog(_("Save..."),
                               None,
                               gtk.FILE_CHOOSER_ACTION_SAVE,
                               (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                gtk.STOCK_SAVE, gtk.RESPONSE_OK))
	dialog.set_default_response(gtk.RESPONSE_OK)
	dialog.set_do_overwrite_confirmation(True)

	filter = gtk.FileFilter()
	filter.set_name("All files")
	filter.add_pattern("*")
	dialog.add_filter(filter)


	response = dialog.run()
	if response == gtk.RESPONSE_OK:
		self.doc = insert_col(self.name_ent,self.email_ent,self.server_com,self.manu_text,self.manu_modle,self.cpu_type,self.firmware_maker,self.bios_set,self.general_ent,self.inform_c,self.dev_submit)
		filesave=open(dialog.get_filename(),"w")
		filesave.write(self.doc.toprettyxml())
		filesave.close()
	     
	elif response == gtk.RESPONSE_CANCEL:
		pass
	dialog.destroy()

	return


    def act_submit(self,widget):
	conn=httplib.HTTPSConnection("www.sun.com")
	try:
		conn.request("GET","/cgi-bin/sun/bigadmin/parseHCLTool.cgi")
		resp=conn.getresponse()
		if resp.status != 200:
			Inst=Message_Box(self.submit_dlg,_('Submit'),_('Submission failed'),_('The server is currently unavailable'))
			Inst.run()
			return
	except:
		Inst=Message_Box(self.submit_dlg,_('Submit'),_('Submission failed'),_('The server is currently unavailable'))
		Inst.run()
		return
	conn.close()

	self.submit_notebook.set_current_page(1)
	self.submit_button.set_sensitive(False)
	
	while gtk.gdk.events_pending():
		gtk.main_iteration(False)
	gobject.timeout_add(100, self.pro)
	gobject.timeout_add(20000, self.destroy_actor)
	
	thread = threading.Thread(target=self.submit_run)
	thread.start()
	
	return


    def submit_run(self):
	self.doc = insert_col(self.name_ent,self.email_ent,self.server_com,self.manu_text,self.manu_modle,self.cpu_type,self.firmware_maker,self.bios_set,self.general_ent,self.inform_c,self.dev_submit)


        BOUNDARY = '------DdU_Post_To_Hcl_BoUnDary$$'
        CRLF = '\r\n'
        L = []


        L.append('--' + BOUNDARY)
        L.append('Content-Disposition: form-data; name="%s"; filename="%s"' % ("hclSubmittalXML", "uud.test"))
        L.append('')
        L.append(str(self.doc.toprettyxml(indent="")))
        L.append('--' + BOUNDARY + '--')
        L.append('')

        body = CRLF.join(L)
   
        content_type = 'multipart/form-data; boundary=%s' % BOUNDARY

	try:
	        h = httplib.HTTPS("www.sun.com")
	        h.putrequest('POST', "/cgi-bin/sun/bigadmin/parseHCLTool.cgi")
	        h.putheader('User-Agent','DDU 0.1')
	        h.putheader('content-length', str(len(body)))
	        h.putheader('content-type', content_type)
	        h.endheaders()
    
        	h.send(body)
 
        	errcode, errmsg, headers = h.getreply()
    
 		statuscode = errcode

		if statuscode != 200:
			self.__success = False
		else:
			self.__success = True
			self.__finish=True

	except:
		self.__success = False
	h.close()
	self.__finish=True
	return
    

    def pro(self):
	if self.__finish == False:
		self.pro_sub.pulse()
	else:
		if self.__success == True:
			msg=_('Submission Successful!\n')
			msg += _('Thank you for your submission.\n')
			msg += _('Your submission will now be reviewed before being posted to the OpenSolaris HCL.\n')
			msg += _('To get more OpenSolaris HCL information, See:\n')
			msg += _('http://www.sun.com/bigadmin/data/os/.\n')
			msg += _('This window will be closed in a few seconds')
		else:
			msg=_("Submission failed")
			
		self.label_warning.set_markup("<span foreground=\"#FF0000\">%s</span>" % msg)
	return not self.__finish


    def destroy_actor(self):
	if self.__success == True:
		self.submit_dlg.destroy()
	return not self.__success


class Message_Box:
    """This Class is used to show error message box"""
    def __init__(self,winID,title,message,sec_message=''):
	self.dialog=gtk.MessageDialog(
			parent			= winID,
			flags			= gtk.DIALOG_DESTROY_WITH_PARENT | gtk.DIALOG_MODAL,
			type			= gtk.MESSAGE_ERROR,
			buttons			= gtk.BUTTONS_CLOSE,
			message_format	= _(message))
	self.dialog.set_title(_(title))
	self.dialog.format_secondary_text(_(sec_message))

    def run(self):
	self.dialog.run()
	self.dialog.destroy()


class detail_inf:
    class __impl:
        """ Implementation of the singleton interface """
        def spam(self):
            return id(self)
		
    __instance = None

    def __init__(self,data='',driver='',device='',fg=''):
	if detail_inf.__instance is None:
		detail_inf.__instance = detail_inf.__impl()

		self.__setattr__("abspath","/usr/ddu")
		self.__setattr__("gladepath",self.__getattr__("abspath")+'/data/hdd.glade')
	
		self.__setattr__("detail_inf_inst",gtk.glade.XML(self.__getattr__("gladepath"),'detail_inf_dlg'))
		self.__setattr__("detail_infdlg",self.__getattr__("detail_inf_inst").get_widget('detail_inf_dlg'))
		self.__setattr__("det_label",self.__getattr__("detail_inf_inst").get_widget('det_label'))
		self.__getattr__("detail_infdlg").connect("response",self.on_response)
		self.__getattr__("detail_infdlg").connect("focus_out_event",self.focus_out_event)
		self.__setattr__("close_button",self.__getattr__("detail_inf_inst").get_widget('close_button2'))
		self.__getattr__("close_button").connect("clicked", self.on_close)
		self.__setattr__("detailtext_view",self.__getattr__("detail_inf_inst").get_widget('detailtext_view'))
		self.__getattr__("detailtext_view").modify_font(pango.FontDescription('DejaVu Sans mono'))
		self.__setattr__("textbuffer",self.__getattr__("detailtext_view").get_buffer())
		insert_one_tag_into_buffer(self.__getattr__("textbuffer"), "bold", "weight", pango.WEIGHT_BOLD)
		self.data=data

	self.__dict__['_Singleton__instance'] = detail_inf.__instance

	self.__getattr__("textbuffer").delete(self.__getattr__("textbuffer").get_start_iter(),self.__getattr__("textbuffer").get_end_iter())

	line_iter = self.__getattr__("textbuffer").get_iter_at_offset (0)
	
	line_iter = self.__getattr__("textbuffer").get_end_iter()
	
	self.__getattr__("det_label").set_markup("<span weight=\"bold\">%s</span>" % device)

	if os.path.exists("/tmp/%s.tmp" % driver):
		status,driverurl=commands.getstatusoutput('/usr/bin/cat /tmp/%s.tmp' % driver) 
		self.__getattr__("textbuffer").insert_with_tags_by_name (line_iter,_("Driver URL:"),"bold")
		self.__getattr__("textbuffer").insert(line_iter,str(driverurl.strip('\t\r\n')+'\n'))

	file = open(data,"r")
	for line in file.readlines():
		line_iter = self.__getattr__("textbuffer").get_end_iter()
		p = re.compile('[a-zA-Z0-9]')
		if p.search(line):
			line_disp = line.split(':')
			if line_disp[0] != '':
				if len(line_disp) > 1:
					self.__getattr__("textbuffer").insert_with_tags_by_name (line_iter,str(line_disp[0].strip('\t\n\r')+":"),"bold")
					space_need=35-len(line_disp[0])
					while space_need > 0:
						self.__getattr__("textbuffer").insert_with_tags_by_name (line_iter,str(' '),"bold")
						space_need = space_need - 1

				else:
					self.__getattr__("textbuffer").insert_with_tags_by_name (line_iter,str(line_disp[0].strip('\t\n\r')+"\n"),"bold")
					line_disp[0].strip('\t\n\r')+":"
			
				if len(line_disp) > 1:
					if len(line_disp) < 3:
						self.__getattr__("textbuffer").insert(line_iter,str(line_disp[1]).strip('\t\n\r\ ')+'\n')
					else:
						self.__getattr__("textbuffer").insert(line_iter,str(line_disp[1]).strip('\t\n\r\ ')+':')
			index=2
			while index < len(line_disp):
				if line_disp[index] != '':	
					self.__getattr__("textbuffer").insert(line_iter,str(line_disp[index]).strip('\t\n\r\ ')+'\n')
					index = index + 1
		else:
			pass
	file.close()
	os.remove(data)
	self.__getattr__("detail_infdlg").show()
	if fg == 'reload':
		self.__getattr__("detail_infdlg").hide()
		self.__getattr__("detail_infdlg").show()
	return

    def focus_out_event(self,widget,data=None):
	pass

    def __getattr__(self, attr):
        """ Delegate access to implementation """
        return getattr(self.__instance, attr)

    def __setattr__(self, attr, value):
        """ Delegate access to implementation """
        return setattr(self.__instance, attr, value)

    def on_close(self,widget):
	try:
		os.remove(self.data)
	except:
		pass
	self.__getattr__("detail_infdlg").destroy()
	detail_inf.__instance = None
	self.__dict__['_Singleton__instance'] = None
	return

    def on_response(self,widget,response):
	try:
		os.remove(self.data)
	except:
		pass
	if response == gtk.RESPONSE_DELETE_EVENT:
		self.__getattr__("detail_infdlg").destroy()
		detail_inf.__instance = None
		self.__dict__['_Singleton__instance'] = None
	return	


app=HDDgui()
gobject.threads_init()
gtk.gdk.threads_init()
gtk.gdk.threads_enter()
gtk.main()
gtk.gdk.threads_leave()
