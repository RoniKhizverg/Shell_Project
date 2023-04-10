#!/usr/bin/perl

# This script renames a file by copying its contents to a new file and then deleting the old file.

use warnings;
use strict;


# Get the names of the old and new files from the command line arguments
my $old_file = shift @ARGV;
my $new_file = shift @ARGV;

# Check that both file names were provided
if (!defined $old_file || !defined $new_file) {
  print "Usage: mv.pl old_file new_file\n";
  exit;
}

# Check if the old file exists
if (! -e $old_file) {
  print "Error: $old_file does not exist\n";
  exit;
}

# Check if the new file already exists
if (-e $new_file) {
  print "Error: $new_file already exists\n";
  exit;
}

# Open the old and new files
open(my $old_fh, '<', $old_file) or die "Could not open $old_file: $!";
open(my $new_fh, '>', $new_file) or die "Could not open $new_file: $!";

# Read from the old file and write to the new file until the end of the old file is reached
while (my $line = <$old_fh>) {
  print $new_fh $line;
}

# Close the old and new files
close $old_fh or die "Could not close $old_file: $!";
close $new_fh or die "Could not close $new_file: $!";

# Delete the old file
unlink $old_file or die "Could not remove $old_file: $!";

# Print a message indicating that the file has been moved
print "Moved $old_file to $new_file\n";
