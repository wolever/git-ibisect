#!/usr/bin/env python

from __future__ import print_function

import os
import sys
import shlex
import codecs
import subprocess as sp

import pexpect

try:
    str = basestring
except NameError:
    pass

testdir = os.path.abspath(os.path.dirname(__file__))
path = lambda *a: os.path.join(testdir, *a)

def print_output(output):
    if not output:
        return
    print("> " + "\n> ".join(x for x in output.splitlines()))


def _xcall(cmd, show_output=False, show_command=False):
    """ Returns the output of calling ``cmd``, or raises an exception if ``cmd`` fails. """
    if isinstance(cmd, str):
        cmd = cmd.split()
    if show_output or show_command:
        print(" ".join(cmd))
    res = sp.check_output(cmd, stderr=sp.STDOUT, stdin=None).decode("utf-8").strip()
    if show_output:
        print_output(res)
    return res

def xcall(cmd, **kwargs):
    try:
        return _xcall(cmd, **kwargs)
    except sp.CalledProcessError as e:
        print_output(e.output.strip())

def call(cmd, **kwargs):
    """ Returns a tuple of (exit status, output) from calling ``cmd``. """
    try:
        return (0, _xcall(cmd, **kwargs))
    except sp.CalledProcessError as e:
        if kwargs.get("show_output"):
            print_output(e.output)
        return (e.returncode, e.output.strip())

def run_test(fname):
    if not os.path.exists(path("./test-repo/")):
        xcall(path("./mk-test-repo"))

    def error(msg):
        print("ERROR: %s" %(msg, ))
        print("In: %s" %(fname, ))
        print("  %s: %s" %(lineno + 1, line, ))
        return False

    os.chdir(path("./test-repo/"))

    cur_proc = None

    xcall("git bisect reset")
    xcall("git checkout master")

    print("Running tests: %s" %(fname, ))
    for lineno, line in enumerate(codecs.open(path(fname), "r", "utf-8")):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        cmd, _, args_str = line.partition(":")
        args_str = args_str.lstrip()
        args = list(filter(None, shlex.split(args_str)))

        if cmd == "checkout":
            xcall("git checkout " + " ".join(args))

        elif cmd == "run":
            if args[0] == "ibisect":
                args[:1] = [sys.executable, path("../git-ibisect")]
            if cur_proc:
                return error("Cannot run; process is already running.")
            cur_proc = pexpect.spawnu(" ".join(args))

        elif cmd == "expect":
            if not cur_proc:
                return error("No process has been run yet.")
            cur_proc.expect_exact(args_str, timeout=1.0)

        elif cmd == "send":
            if not cur_proc:
                return error("No process has been run yet.")
            cur_proc.sendline(args_str)

        elif cmd == "debug":
            print()
            print("debug: entering interactive mode...")
            print()
            if cur_proc:
                cur_proc.interact()
            else:
                os.system("/bin/bash")

        else:
            return error("invalid command: %s" %(cmd, ))

        print("  %s: OK!" %(line, ))

files = sys.argv[1:]
if not files:
    print("Usage: %s test-foo.txt [test-bar.txt ...]" %(sys.argv[1], ))
    sys.exit(1)

for f in files:
    run_test(f)
