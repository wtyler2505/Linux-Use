from typing import Set

# Control types that the agent can directly interact with
INTERACTIVE_CONTROL_TYPE_NAMES: Set[str] = {
    'ButtonControl', 'CheckBoxControl', 'ComboBoxControl', 'CustomControl', 
    'DataItemControl', 'EditControl', 'GroupControl', 'HyperlinkControl', 'ImageControl', 
    'ListItemControl', 'MenuControl', 'MenuBarControl', 'MenuItemControl', 
    'PaneControl', 'RadioButtonControl', 'ScrollBarControl', 'SliderControl', 
    'SpinnerControl', 'SplitButtonControl', 'TabItemControl', 'TableControl', 
    'ThumbControl', 'TitleBarControl', 'ToolBarControl', 'TreeItemControl', 
    'WindowControl'
}

# Control types that provide information but are not typically interactive
INFORMATIVE_CONTROL_TYPE_NAMES: Set[str] = {
    'HeaderControl', 'HeaderItemControl', 'IndicatorControl', 'ProgressBarControl',
    'SeparatorControl', 'StatusBarControl', 'TextControl', 'ToolTipControl'
}

# Default actions for legacy patterns that indicate interactiveness
DEFAULT_ACTIONS: Set[str] = {
    'Press', 'Click', 'Open', 'Expand', 'Collapse', 'Toggle'
}
