"""
Strategy module initialization.
"""
from .basic_strategy import Action, BasicStrategy
from .index_plays import IndexPlay, IndexPlays
from .advisor import Advisor

__all__ = [
    'Action', 'BasicStrategy',
    'IndexPlay', 'IndexPlays',
    'Advisor'
]