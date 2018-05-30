#!/usr/bin/env python
import yaml
import json
import sys
"""
simple YAML to JSON converter

usage:
  python json_to_yaml.py < my-json-file.json
"""
yaml.dump(json.load(sys.stdin), sys.stdout)
