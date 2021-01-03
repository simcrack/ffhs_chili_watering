from datetime import time

from lib.adc.MCP3008 import MCP3008


mcpInterface = None


def getMCPInterface():
    global mcpInterface
    if mcpInterface:
        return mcpInterface
    mcpInterface = MCP3008()
    return mcpInterface
