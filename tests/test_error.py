#import argparse
from pathlib import Path

import pytest

from pharmpy import Model
from pharmpy.plugins.utils import PluginError
from pharmpy.modeling import additive_error, combined_error, proportional_error, remove_error


def test_remove(model):
    print(model.source.path)
    remove_error(model)
    model.update_source()

def test_additive(model):
    print(model.source.path)
    additive_error(model)
    model.update_source()

def test_proportional(model):
    print(model.source.path)
    proportional_error(model)
    model.update_source()
   
def test_combined(model):
    print(model.source.path)
    combined_error(model)
    model.update_source()

