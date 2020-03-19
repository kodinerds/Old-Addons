#!/usr/bin/env python

# source: https://github.com/sanderjo/fast.com

import fast_com
import xbmcgui
import sys

result = fast_com.fast_com()

okDialog = xbmcgui.Dialog()
ok = okDialog.ok("FAST.com", "Result: %s Mbps" % result)

sys.modules.clear()

