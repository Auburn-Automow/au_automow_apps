#!/usr/bin/env python

NAME='rosapp'

import cStringIO
import os
import sys
import socket
import struct
import threading
import time

import roslib
roslib.load_manifest('automow_apps')
import roslib.message
import roslib.names
import roslib.network
import roslib.scriptutil
import rospy
import rosmsg

import rosservice
from app_manager.srv import ListApps, StartApp, StopApp

from optparse import OptionParser

class ROSAppException(Exception):
    """Base class for rosapp-related exceptions"""
    pass

class ROSAppIOException(ROSAppException):
    """rosapp related to network I/O failure"""
    pass

def _rosapp_list(running=True, available=True, verbose=False, robot=None):
    try:
        matches = rosservice.rosservice_find('app_manager/ListApps')
    except:
        pass
    for match in matches:
        (req, resp) = rosservice.call_service(match, None, ListApps)
        if running:
            for app in resp.running_apps:
                print str(app.name)
        if available:
            for app in resp.available_apps:
                print str(app.name)

def _rosapp_start(args, robot=None):
    matches = []
    if robot is None:
        try:
            matches.extend(rosservice.rosservice_find('app_manager/StartApp'))
        except:
            pass
    else:
        matches.append('/' + str(robot) + '/start_app')
    for match in matches:
        (req, resp) = rosservice.call_service(match, args, StartApp)
        print resp

def _rosapp_stop(args, robot=None):
    matches = []
    if robot is None:
        matches.extend(rosservice.rosservice_find('app_manager/StopApp'))
    else:
        matches.append('/' + str(robot) + '/stop_app')
    for match in matches:
        (req, resp) = rosservice.call_service(match, args, StopApp)
        print resp

def _fullusage():
    print "This is a usage"
    pass

def _rosapp_cmd_list(argv):
    args = argv[2:]
    parser = OptionParser(usage="usage: %prog list", prog=NAME)
    parser.add_option("-a", "--available",
            dest="available_apps", default=False, action="store_true",
            help="Print available apps")
    parser.add_option("-r", "--running",
            dest="running_apps", default=False, action="store_true",
            help="Print running apps")
    (options, args) = parser.parse_args(args)
    if not options.running_apps and not options.available_apps:
        _rosapp_list()
    else:
        _rosapp_list(running=options.running_apps, available=options.available_apps)

def _rosapp_cmd_start(argv):
    args = argv[2:]
    parser = OptionParser(usage="usage: %prog start app_name", prog=NAME)
    (options, args) = parser.parse_args(args)
    _rosapp_start(args)

def _rosapp_cmd_stop(argv):
    args = argv[2:]
    parser = OptionParser(usage="usage: %prog stop app_name", prog=NAME)
    (options, args) = parser.parse_args(args)
    _rosapp_stop(args)

def _rosapp_cmd_info(argv):
    pass

def rosappmain(argv=sys.argv):
    if len(argv) == 1:
        _fullusage()
    try:
        command = argv[1]
        if command in 'list':
            _rosapp_cmd_list(argv)
        elif command == 'info':
            _rosapp_cmd_info(argv)
        elif command == 'start':
            _rosapp_cmd_start(argv)
        elif command == 'stop':
            _rosapp_cmd_stop(argv)
        else:
            _fullusage()
    except socket.error:
        print >> sys.stderr, "Network communication failed with the master or a node."
        sys.exit(1)
    except ROSAppException, e:
        print >> sys.stderr, "ERROR: " + str(e)
        sys.exit(2)
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    rosappmain()
