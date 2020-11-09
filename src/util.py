#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: marinheiro
# @Date:   2014-09-23 14:38:37
# @Last Modified by:   marinheiro
# @Last Modified time: 2014-09-23 17:30:08

import os
import re

def read_header_file(header_file):
	ret = {}
	images = []
	mask = ""

	base = os.path.abspath(os.path.dirname(header_file))

	with open(header_file) as hfile:
		first = True
		tot = 0
		for line in hfile:
			if first:
				tot = float(line)
				first = False
			else:
				if tot > 0:
					path = os.path.join(base, line[:-1])
					images.append(path)
				elif tot == 0:
					path = os.path.join(base, line[:-1])
					mask = path
				
				tot = tot-1

	ret['images'] = images
	ret['mask'] = mask

	return ret

def find_files_path(path):
	ret = {}
	images = []
	mask = ""
	objmask = ''
	validextensions = {".png"}
	os.chdir(path)
	path = os.path.normpath(os.getcwd())
	print ('path: ', path)
	for root, dirs, files in os.walk(path):
		for file in files:
			if file.endswith(tuple(validextensions)):
				maskmatch = re.match(r"probe.mask.png", file, re.I)
				objmatch = re.match(r"object.mask.png", file, re.I)
				imagematch = re.match(r"[a-z]*.[0-9]*.png", file, re.I)
				if maskmatch:
					mask = os.path.join(root, file)
				if objmatch:
					objmask = os.path.join(root, file)
				if imagematch:
					images.append(os.path.join(root, file))
	ret['images'] = images
	ret['mask'] = mask
	ret['object'] = objmask
	return (ret)

def read_lights_file(lights_file):
	lights = []
	with open(lights_file) as lfile:
		l = 0
		tot = 0
		for line in lfile:
			if l == 1:
				tot = float(line)
			elif l > 1:
				if tot > 0:
					w = line.split()
					lights.append((float(w[0]), float(w[1]), float(w[2])))

				tot = tot-1
			l = l+1

	return lights

def to_world_coordinate_system(point):
	return (-point[1], point[0])