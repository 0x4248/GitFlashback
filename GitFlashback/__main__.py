# SPDX-License-Identifier: GPL-3.0
# GitFlashback
# Export all Git commits as snapshots.
#
# __main__.py
# Main script for GitFlashback.
#
# COPYRIGHT NOTICE
# Copyright (C) 2024 0x4248 and contributors
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the license is not changed.
#
# This software is free and open source. Licensed under the GNU general
# public license version 3.0 as published by the Free Software Foundation.

import os
import subprocess
import shutil
import argparse

def error_exit(message):
    print(f"Error: {message}")
    exit(1)

def get_commit_details(repo_path):
    if not os.path.isdir(repo_path) or not os.path.isdir(os.path.join(repo_path, ".git")):
        error_exit("The provided path is not a valid Git repository.")
        return

    try:
        commit_details = subprocess.check_output(
            ["git", "log", "--pretty=format:%H:%cd:%an:%s", "--date=short"], cwd=repo_path, text=True
        ).splitlines()
    except subprocess.CalledProcessError as e:
        error_exit(f"Failed to get commit details - {e}")
        return

    return commit_details

def export_git_versions(repo_path, output_path):
    if not os.path.isdir(repo_path) or not os.path.isdir(os.path.join(repo_path, ".git")):
        error_exit("The provided path is not a valid Git repository.")
        return

    if output_path == ".":
        output_path = os.getcwd()
    elif not output_path:
        output_path = repo_path

    versions_folder = os.path.join(output_path, "versions")
    os.makedirs(versions_folder, exist_ok=True)

    commit_details = get_commit_details(repo_path)

    commits_file_path = os.path.join(versions_folder, "commits.txt")
    with open(commits_file_path, "w") as commits_file:
        for detail in commit_details:
            commit_hash, date, author, message = detail.split(":", 3)
            commits_file.write(f"{commit_hash}: {date} {author}\n{message}\n\n")

    for detail in commit_details:
        commit_hash, _, _, _ = detail.split(":", 3)
        commit_folder = os.path.join(versions_folder, commit_hash)
        os.makedirs(commit_folder, exist_ok=True)

        try:
            if args.quiet:
                subprocess.check_call(["git", "checkout", commit_hash], cwd=repo_path, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            else:
                subprocess.check_call(["git", "checkout", commit_hash], cwd=repo_path)
            for item in os.listdir(repo_path):
                item_path = os.path.join(repo_path, item)
                if item not in {".git", "versions"}:
                    dest_path = os.path.join(commit_folder, item)
                    if os.path.isdir(item_path):
                        shutil.copytree(item_path, dest_path)
                    else:
                        shutil.copy2(item_path, dest_path)
        except subprocess.CalledProcessError as e:
            error_exit(f"Failed to export commit {commit_hash} - {e}")
        finally:
            if args.quiet:
                subprocess.check_call(["git", "checkout", "main"], cwd=repo_path, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            else:
                subprocess.check_call(["git", "checkout", "main"], cwd=repo_path)

    print(f"Export completed. All commits saved in {versions_folder}.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Export all Git commits as snapshots.")
    parser.add_argument("repo", help="Path to the Git repository.")
    parser.add_argument(
        "output",
        nargs="?",
        default="",
        help="Path to the output directory for the versions folder (default: repo folder). Use '.' for the working directory.",
    )
    parser.add_argument("-q", "--quiet", action="store_true", help="Suppress output.")
    args = parser.parse_args()

    export_git_versions(args.repo, args.output)
