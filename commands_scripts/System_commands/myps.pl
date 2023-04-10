#!/usr/bin/perl

# This script takes command-line arguments to execute different variations of the 'ps' command on a Unix/Linux system.
# ps is a command in Unix and Unix-like operating systems that is used to display information about running processes on the system.
# The information that ps provides includes the process ID (PID), the user who started the process,
# the amount of CPU and memory resources the process is using, and other details about the process's status, priority, and resource usage.

use strict; 
use warnings;

# Extract the first command-line argument from the @ARGV array, which is then stored in the $cmd variable.
my $cmd = shift @ARGV || "";

# Determine which variation of the 'ps' command to execute based on the value of $cmd.
# If $cmd is '-e', display information about all processes running on the system.
if ($cmd eq "-e" ) {  
  open my $ps, "ps $cmd |";  # Open a pipe to the 'ps' command with the '-e' option. 
  while (<$ps>) {  # Read each line of output from the 'ps' command.
    print;  # Print the line of output to the console.
  }
  
  close $ps;  # Close the pipe to the 'ps' command.
  
  # If $cmd is '-ef', display detailed information about all processes running on the system.
} elsif ($cmd eq "-ef") { 

  # Print a formatted table header to the console.
  print "UID\tPID\tPPID\tC\tSTIME\tTTY\tTIME\t\tCMD\n";
  open my $ps, "ps $cmd |";  # Open a pipe to the 'ps' command with the '-ef' option.
  
  # Read each line of output from the 'ps' command.
  while (<$ps>) {  
    if ($. == 1) {  # Skip the first line of output, which contains column headers.
      next;
    }
    my @fields = split;  # Split the line of output into an array of fields.
    
    # Print the relevant fields to the console in a formatted table row.
    print "$fields[0]\t$fields[1]\t$fields[2]\t$fields[3]\t$fields[4]\t$fields[5]\t$fields[6]\t$fields[7]\n";
  }
  close $ps;  # Close the pipe to the 'ps' command.
  
  # If $cmd is anything else (i.e. an empty string or any other value), display basic information about all processes running on the system.
} else {  

  # Print a formatted table header to the console.
  print "PID\tTTY\tTIME\tCMD\n";
  
  open my $ps, "ps |";  # Open a pipe to the 'ps' command with no options.
  
  # Read each line of output from the 'ps' command.
  while (<$ps>) {  
    if ($. == 1) {  # Skip the first line of output, which contains column headers.
      next;
    }
    my @fields = split;  # Split the line of output into an array of fields.
    
    # Print the relevant fields to the console in a formatted table row.
    print "$fields[0]\t$fields[1]\t$fields[2]\t$fields[3]\n";
  }
  close $ps;  # Close the pipe to the 'ps' command.
}

