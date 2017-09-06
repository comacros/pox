# -*- coding: utf-8 -*-

import importlib

import pox.theme
import pox.plot



def rgb(red, green, blue):
	return (1 << 24) + ((red % 256) << 16) + ((green % 256) << 8) + (blue % 256)