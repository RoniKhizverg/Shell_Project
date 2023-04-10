#!/usr/bin/perl

# The top command is a system monitor tool for Unix-based systems that displays real-time information about running processes and system resources.

use strict;
use warnings;

# use POSIX for system calls and other POSIX functions
use POSIX;

# define the interval (in seconds) between updates
my $interval = 5;

# define the maximum number of processes to display
my $max_processes = 40;

# function to retrieve process information
sub get_process_info {

    my @process_info;

    # open a pipe to the ps command and read its output
    open my $ps, "ps -eo pid,user,pcpu,pmem,etime,vsz,rss,comm,args --sort=-pcpu |" or die "Couldn't run ps command: $!";

    # iterate over each line of the ps output
    while (<$ps>) {
        # split the line into fields
        my ($pid, $user, $cpu, $mem, $etime, $vsz, $rss, $comm, $args) = split /\s+/;

        # remove the '%' sign from the user field
        $user =~ s/%//;

        # add a hash reference containing the process information to the @process_info array
        push @process_info, {
            pid => $pid,
            user => $user,
            cpu => $cpu,
            mem => $mem,
            etime => $etime,
            vsz => $vsz,
            rss => $rss,
            comm => $comm,
            args => $args,
        };
    }

    # close the pipe and return the array of process information
    close $ps;
    return @process_info;
}

# main loop
while (1) {

    # get the process information
    my @process_info = get_process_info();

    # clear the screen
    print "\033[2J";

    # move the cursor to the top-left corner
    print "\033[0;0H";

    # iterate over the first $max_processes processes and print their information
    for (my $i = 0; $i < $max_processes; $i++) {
        my $process = $process_info[$i];

        # print the process information in a formatted table
        printf "%5s\t %-8s %5s%% %5s%% %10s %10s %10s %-15s %s\n",
            $process->{pid},
            $process->{user},
            # if the CPU or memory usage is a number, format it with one decimal place
            # otherwise, print it as is
            ($process->{cpu} =~ /^\d+(\.\d+)?$/) ? sprintf("%.1f", $process->{cpu}) : $process->{cpu},
            ($process->{mem} =~ /^\d+(\.\d+)?$/) ? sprintf("%.1f", $process->{mem}) : $process->{mem},
            $process->{etime},
            $process->{vsz},
            $process->{rss},
            $process->{comm},
            $process->{args};
    }

    # sleep for $interval seconds before repeating the loop
    sleep $interval;
}

