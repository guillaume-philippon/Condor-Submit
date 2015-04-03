#!/usr/bin/python
# pylint: disable=no-member
"""
condor.py is a python script to improve user experience with HTCondor batch scheduler
"""
import argparse
import getpass
import grp
import time
import os
import htcondor
import classad


__author__ = 'Guillaume Philippon <guillaume.philippon@lal.in2p3.fr>'
__version__ = 1.0


class UserNotInGroup(Exception):
    """
    Raise this exception if the current user is not on Unix group
    """
    pass


def command_parser():
    """
    Function that parse the CLI arguments and return a Namespace (see argparse module)
    :return: Namespace
    """
    parser = argparse.ArgumentParser(description='Condor submit wrapper to improve user experience')
    parser.add_argument('script', help='/path/to/script you want run')
    parser.add_argument('--args', dest='arguments', help='Arguments for your script')
    parser.add_argument('--group', dest='group',
                        help='Condor group you want to use (based on Unix group)')
    parser.add_argument('--machine', dest='machine',
                        help='Define a specific machine you want use (should be'
                             ' the full hostname of the machine)')
    parser.add_argument('--cpus', dest='cpus', help='Number of CPUs you need')
    return parser.parse_args()


def classad_creator(arguments, directory):
    """
    Function that return a classad based on arguments provide by CLI
    (see classad module from htcondor)
    :param arguments: Namespace
    :return: ClassAd
    """
    job_classad = classad.ClassAd()
    job_classad["CMD"] = arguments.script
    job_classad["UserLog"] = "{0}/{1}.log".format(directory, arguments.script)
    job_classad["Out"] = "{0}/{1}.out".format(directory, arguments.script)
    if arguments.arguments is not None:
        job_classad["Arguments"] = arguments.arguments
    if arguments.group is not None:
        if check_group(arguments.group):
            job_classad["AcctGroup"] = "group_{0}".format(arguments.group)
            job_classad["AccountingGroup"] = "group_{0}.{1}".format(arguments.group, get_username())
        else:
            raise UserNotInGroup()
    if arguments.cpus is not None:
        job_classad["RequestCpus"] = int(arguments.cpus)
        job_classad["RequestMemory"] = 2048 * int(arguments.cpus)
    if arguments.machine is not None:
        job_classad["Requirements"] = classad.ExprTree("(Machine =="
                                                       " \"{0}\")".format(arguments.machine))
    return job_classad


def get_username():
    """
    Return the username of current user
    :return: string
    """
    return getpass.getuser()


def check_group(group):
    """
    check if user is in group requested. If group not exist, return False
    :return: boolean
    """
    username = get_username()
    try:
        group_information = grp.getgrnam(group)
        if username in group_information.gr_mem:
            return True
        else:
            return False
    except KeyError:
        return False


def prepare_job_execution(job_name):
    """
    Create a directory to store log file and return the name for directory
    :return: string
    """
    directory_suffix = time.time()
    directory_name = "{0}.{1}".format(os.path.basename(job_name), directory_suffix)
    os.mkdir(directory_name)
    return directory_name


def main():
    """
    Main function
    """
    arguments = command_parser()
    try:
        directory = prepare_job_execution(arguments.script)
        job_classad = classad_creator(arguments, directory)
        scheduler = htcondor.Schedd()
        job_id = scheduler.submit(job_classad)
        print "Job {0} as been started output and log will be stored under" \
              " {1}/ directory".format(job_id, directory)
    except UserNotInGroup:
        print "You ({0}) are not in group: {1}".format(get_username(), arguments.group)

if __name__ == '__main__':
    main()
