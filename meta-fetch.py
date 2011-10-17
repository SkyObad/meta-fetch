#!/usr/bin/python
# encoding: utf-8

from __future__ import print_function

import sys
import os
import subprocess
import time

children = []
root = os.path.expanduser("~")
for dirpath, dirnames, filenames in os.walk(root, topdown = True):
	if dirpath.endswith("Trash"):
		dirnames[0:] = [] #prevent recursion
	if any(map(lambda a: a == ".svn", dirnames)):
		dirnames[0:] = [] #prevent recursion
		child = subprocess.Popen(['svn', 'update', '--quiet', '--non-interactive'], cwd=dirpath, bufsize=-1, stderr=subprocess.PIPE)
		children.append(tuple([child, dirpath]))
	if any(map(lambda a: a == ".git", dirnames)):
		dirnames[0:] = [] #prevent recursion
		child = subprocess.Popen(['git', 'fetch', '--all', '--prune', '--quiet'], cwd=dirpath, bufsize=-1, stderr=subprocess.PIPE)
		children.append(tuple([child, dirpath]))

remaining = children
while remaining:
	children = remaining
	remaining = []
	
	for process, path in children:
		process.poll()
		if process.returncode == None:
			child = (process, path)
			remaining.append(child)
			time.sleep(0.01)
			continue
		if process.returncode != 0:
			print("[ERROR] %s:" % (path.lstrip(root)))
			for line in process.stderr:
				print(line.strip())
		else:
			print("[OK] %s" % (path.lstrip(root)))
	children = remaining
