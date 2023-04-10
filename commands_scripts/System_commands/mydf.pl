#!/usr/bin/perl

use strict;
use warnings;

# The df command in Linux and Unix-like operating systems is used to display information about the file system usage on a computer.
# It shows the total size, used space, available space, and percentage of space used for each file system. 

# Initialize a variable to track whether to display sizes in human-readable format
my $human_readable = 0;

# Check if the -h option was passed
if (@ARGV && $ARGV[0] eq "-h") {
    $human_readable = 1;
}

# Run the `df` command and store the output in `@df_output`
my @df_output = `df -h` if $human_readable;
@df_output = `df` if !$human_readable;

# Remove the first line, which contains the headers
shift @df_output;

# Print a header line with the topics of each column, depending on whether the `-h` option was passed
if ($human_readable) {
    print "Filesystem\tSize\tUsed\tAvailable\tused%\tMounted on\n";
} else {
    print "Filesystem\t1K-blocks\tUsed\tAvailable\tused%\tMounted on\n";
}

# Loop through each line of `@df_output`
foreach my $line (@df_output) {

    # Split the line into columns using whitespace as the delimiter
    my @columns = split /\s+/, $line;

    # Extract the values for each column
    my $filesystem = $columns[0];
    my $size = $columns[1];
    my $used = $columns[2];
    my $available = $columns[3];
    my $percent_used = $columns[4];
    my $mount_point = $columns[5];

    # Print the values, separated by tabs
    print "$filesystem\t$size\t$used\t$available\t$percent_used\t$mount_point\n";
}

