"""
pytest configuration file for jass-runner tests.

This file sets up the testing environment and provides fixtures
shared across all tests in the project.
"""

import sys
import os

# Add the src directory to Python's path so tests can import jass_runner
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))