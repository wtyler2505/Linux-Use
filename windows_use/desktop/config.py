from typing import Set

BROWSER_NAMES=set(['msedge.exe','chrome.exe','firefox.exe'])

AVOIDED_APPS:Set[str]=set([
    'Recording toolbar'
])

EXCLUDED_APPS:Set[str]=set([
    'Program Manager','Taskbar'
]).union(AVOIDED_APPS)