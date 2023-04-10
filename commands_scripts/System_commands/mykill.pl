#!/usr/bin/perl

use strict;
use warnings;
use POSIX qw(:signal_h);

# Check that we were given a process ID
if (@ARGV != 1) {
    print "Usage: $0 PID\n";
    exit 1;
}

# The process ID to send the signal to
my $pid = $ARGV[0];

# Send the SIGTERM signal
if (kill(SIGTERM, $pid) == 0) {
    print "Failed to send signal to process $pid: $!\n";
    exit 1;
} else {
    print "Signal sent to process $pid\n";
}