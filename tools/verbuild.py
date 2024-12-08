# SPDX-License-Identifier: GPL-3.0
# GitFlashback
# Export all Git commits as snapshots.
#
# tools/verbuild.py
# Run a command on each version.
#
# For example:
# python tools/verbuild.py versions/ "make"
#
# or to build and copy the binaries:
# python tools/verbuild.py versions/ "make && mkdir ../../out/%REF%/ && cp bin/ ../../out/%REF%/"
#
# COPYRIGHT NOTICE
# Copyright (C) 2024 0x4248 and contributors
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the license is not changed.
#
# This software is free and open source. Licensed under the GNU general
# public license version 3.0 as published by the Free Software Foundation.

import os
import argparse

def main():
	parser = argparse.ArgumentParser(description="Run a command on each version.")
	parser.add_argument("versions", help="Path to the versions folder.")
	parser.add_argument("command", help="Command to run on each version.")

	args = parser.parse_args()

	if not os.path.isdir(args.versions):
		print("The provided path is not a valid versions folder.")
		return

	for version in os.listdir(args.versions):
		version_path = os.path.join(args.versions, version)
		if not os.path.isdir(version_path):
			continue

		print(f"Running command on {version}...")
		command = args.command.replace("%REF%", version)
		os.system(f"cd {version_path} && {command}")

if __name__ == "__main__":
	main()