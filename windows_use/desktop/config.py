from typing import Set

BROWSER_NAMES=set(['msedge.exe','chrome.exe','firefox.exe'])

AVOIDED_APPS:Set[str]=set([
    'Recording toolbar','meet.google.com is sharing your screen.'
])

EXCLUDED_APPS:Set[str]=set([
    'Progman','Shell_TrayWnd',
    'Microsoft.UI.Content.PopupWindowSiteBridge',
    'Windows.UI.Core.CoreWindow',
]).union(AVOIDED_APPS)

PROCESS_PER_MONITOR_DPI_AWARE = 2