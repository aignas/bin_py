#!/usr/bin/env python3

import os, time, glob, sys
import argparse
from subprocess import call

# The queue dir
QUEUEDIR = os.getenv("HOME") + "/Mail/.sendqueue"
LOCKFILE = QUEUEDIR + "/.msmtp-lock"
MAXWAIT = 120
ADDRESS_REFRESH = [ "~/Mail/gmail/GM.Sent", "~/Mail/hermes/Sent" ]
ADDRESS_DEST = "~/.cache/mutt/mu-sent-index"

#{{{ fun: touch
def touch(path):
    basedir = os.path.dirname(path)
    if not os.path.exists(basedir):
        os.makedirs(basedir)

    with open(path, 'a'):
        os.utime(path, None)
#}}}
#{{{ fun: check_connection
# Found this on http://stackoverflow.com/a/3764660/1105870
def check_connection(url='http://74.125.113.99'):
    """
    By default this function checks whether google is up. It uses the IP address to speed things up.
    If google is not up, I don't know what is...
    """
    try:
        response=urllib2.urlopen(url, timeout=1)
        return True
    except urllib2.URLError as err: pass
    return False
#}}}

#{{{ fun: listqueue
def listqueue(qdir=QUEUEDIR):
    count = len(os.listdir(qdir))/2

    for files in glob.glob(qdir + "/*.mail"):
        message = ""
        with open(files) as f:
            for line in f:
                li=line.strip()
                if li.startswith("From:") or \
                        li.startswith("To:") or \
                        li.startswith("Subject:"):
                   message += li + "\n"
                
        print(message)

    if count == 0:
        print("No mail in queue")

    return count
#}}}
#{{{ fun: enqueue
def enqueue(params, email, qdir=QUEUEDIR):
    """
    This is a function to enqueue messages
    """
    # Make the directory to queue messages if doesn't exist
    if not os.path.exists(qdir):
        os.makedirs(qdir)

    # Construct the base of the file
    timestamp = time.strftime("%Y-%m-%d-%H.%M.%S", time.gmtime())
    base = qdir + "/" + timestamp
    i=0
    while (os.isfile(base + ".mail") or os.isfile(base + ".msmtp")):
        i += 1
        base = qdir + "/" + timestamp + "-" + i

    with os.open(base + ".mail", os.O_WRONLY, int("0600", 8)) as fem, os.open(base + ".msmtp", os.O_WRONLY, int("0600", 8)) as fms:
        # Print strings into files
        print(params, fms)
        print(message, fem)
#}}}
#{{{ fun: runqueue
def runqueue(qdir=QUEUEDIR, maxwait=120, lockfile=LOCKFILE):
    # Wait for a lock that another instance has set
    wait = 0
    for i in range(maxwait):
        if os.isfile(lockfile):
            time.sleep(1)
        else:
            break

    if os.isfile(lockfile):
        print("Cannot use the queuedir, because another instance is already using it")
        print("Remove the lockfile if that's not the case")

    # Check for empty queuedir
    if len(os.listdir(qdir)) == 0:
        print("No mails in the queuedir")

    # Lock the directory
    touch(lockfile)

    # Process all mails
    for mailfile in glob.glob(qdir + "/*.mail"):
        msmtpfile = os.path.splitext(mailfile)[0] + ".msmtp"
        print("Sending")

        with os.open(msmtpfile) as f:
            msmtp_opts = f.read()


        if 0 != Call(["msmtp", msmtp_opts, "<", mailfile]):
            os.remove(msmtpfile)
            os.remove(mailfile)
            print("Sent")
        else:
            print("msmtp could not process the message")
    

    # Unlock the directory
    os.rm(lockfile)

    return 0
#}}}

#{{{ fun: refresh_addresses
def refresh_addresses(dirs=ADDRESS_REFRESH, dest=ADDRESS_DEST):
    for directory in dirs:
        args = [ "mu", "index", "--nocleanup",
                "--maildir=" + directory,
                "--muhome=" + dest ]
        call(args)
#}}}

#{{{ fun: sendmail
def sendmail (params):
    message = sys.stdin.read().rstrip()
    enqueue(params, message)

    if check_connection:
        runqueue()
        print("Messages were successfully sent")

    return True
#}}}
#{{{ fun: syncmail
# FIXME Make the idle script working properly with imaplib2
def syncmail():
    args = ["mbsync", "gmail", "hermes"]
    return call(args)
#}}}

#{{{ fun: Our parameter parser
def main():
    parser = argparse.ArgumentParser(
            description="""
    Mutt helper functions, which make my mutt setup slightly more clever. This script facilitates
    sending mail (queueing and running the queue), checking the mail and refreshing the address book.
        """)
    group = parser.add_mutually_exclusive_group()
    parser.add_argument("--opt-queuedir",
            help="Set the queuedir")
    parser.add_argument("--opt-lockfile",
            help="The locking file path to use for msmtp queue running")
    parser.add_argument("--opt-maxwait",
            help="The maximum wait time for the runqueue")
    parser.add_argument("--opt-refresh-dir",
            help="The refresh directory list for the address book")
    parser.add_argument("--opt-adrresbook-dest",
            help="The destination for the address book index")
    group.add_argument("--sendmail", action="store_true",
            help="Send a message. This is sendmail compatible as we wrap arround msmtp. Pass the \
            parameters to msmtp after --sendmail.")
    group.add_argument("--runqueue", action="store_true",
            help="Send all the messages in the Outbox")
    group.add_argument("--refresh-addresses", action="store_true",
            help="Refresh the address book by indexing the sent-mail")
    group.add_argument("--syncmail", action="store_true",
            help="Synchronize with remote IMAP accounts")

    # Parse only the known parameters as we want to pipe all the other stuff to msmtp and otherwise
    # it doesn't work. Save the rest of parameters as a simple list
    args_k, args_u = parser.parse_known_args()

    if args_k.sendmail:
        print("Sending mail")
        sendmail(args_u)
    elif args_k.runqueue:
        print("Running the queue")
        runqueue()
    elif args_k.refresh_addresses:
        print("Refresh the address book")
        refresh_addresses()
    elif args_k.syncmail:
        print("Synchronise with remote IMAP mailboxes")
        syncmail
    else:
        print("Incorrect parammeters. Please see the help by using the [-h|--help] option.")

    return 0
#}}}

# Execute the function
main()

# vim: foldmethod=marker
