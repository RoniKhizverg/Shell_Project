#!/usr/bin/perl
# This script copies the contents of one file to another.

use warnings;
use strict;

# Get the source and destination filenames from the command line arguments.
my ($src, $dst) = @ARGV;

# Open the source file for reading and the destination file for writing.
open(my $src_fh, "<", $src) or die "Cannot open source file: $src: $!";
open(my $dst_fh, ">", $dst) or die "Cannot open destination file: $dst: $!";

# Loop over each line of the source file, copying it to the destination file.
while (my $line = <$src_fh>) {
   print $dst_fh $line;
}

# Print a message indicating that the copy operation was successful.
print "Copy created from $src to $dst.\n";

# Close the filehandles.
close($src_fh);
close($dst_fh);

