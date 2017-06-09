
"""
Moonshine Maya xgen WIP version control Tool
"""

def start():
	import xgenHub_ui; reload(xgenHub_ui)
	xgenHub = xgenHub_ui.MsXGenHubUI()
	xgenHub.showUI()