"""This package is used for accessing the MCP3008.

It provides a singleton which can be accessed by getMCPInterface().
"""
from datetime import time
from lib.adc.MCP3008 import MCP3008

mcpInterface = None


def getMCPInterface():
	"""Getter for singleton mcpInterface.
	
	Returns:
		An instance to a MCP3008 object.
	"""
	global mcpInterface
	if mcpInterface:
		return mcpInterface
	mcpInterface = MCP3008()
	return mcpInterface