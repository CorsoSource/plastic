"""
    Slightly easier to import stuff.
    
    This is Ignition, so let's shortcut some of that boilerplate.
"""


__all__ = [
    'PlasticIgnition',
    'connect_table',
    'commit',
]

from plastic.connectors.ignition import PlasticIgnition, connect_table
from plastic.core import commit


