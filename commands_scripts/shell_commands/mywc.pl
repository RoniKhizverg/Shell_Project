#!/usr/bin/perl

use warnings;
use strict;

# Get the filename from the command-line argument
my $file = $ARGV[0];

# Initialize counters for words, bytes, and lines
my ($word_count, $byte_count, $line_count) = (0, 0, 0);

# Attempt to open the file for reading
open(my $fh, "<", $file) or die "Cannot open file: $file: $!";

# Loop over each line in the file
while (my $line = <$fh>) {

   # Increment the line counter
   $line_count++;

   # Add the length of the line to the byte counter
   $byte_count += length($line);

   # Split the line into words and add the number of words to the word counter
   $word_count += scalar(split(/\s+/, $line));
}

# Print the counts to standard output
print "$line_count ";
print "$word_count ";
print "$byte_count\n";

# Close the file
close($fh);

