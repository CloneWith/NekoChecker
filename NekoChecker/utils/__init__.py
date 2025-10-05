"""Some utility functions for the NekoChecker package to use."""

import re


CLI = {
    "unavailable": "This feature is not available."
}

COLORS = {
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "reset": "\033[0m"
}

def tint(text: str, color: str) -> str:
    return f"{COLORS[color]}{text}{COLORS['reset']}"

def bold(s: str) -> str:
    """
    Returns the bold format version of a string.
    """

    # Stay the same: have been marked as bold 
    if s.find("\033[1;") != -1: return s
    
    # Add a reset mark if the string doesn't have one.
    if not s.endswith(COLORS['reset']):
        s += COLORS['reset']

    if not s.startswith("\033"):
        return f"\033[1;0m{s}"
    
    mark_pattern = re.compile(r"\033\[[0-9]m*")
    
    if re.match(mark_pattern, s):
        return f"\033[1;{s[2:]}"
    return "\033[1m" + s
