#!/usr/bin/perl

use strict;
use warnings;


# These lines retrieve the first and second command-line arguments provided
# to the script and store them in $src_file and $dest_file, respectively.

my $src_file = $ARGV[0];
my $dest_file = $ARGV[1];


# This block of code checks if either $src_file or $dest_file are undefined.
# If either of them is undefined, it prints an error message and exits the script.

if (!defined $src_file or !defined $dest_file) {
    die "Usage: $0 <source_file> <destination_file>\n";
}

# This block of code checks if the destination file already exists.
# If it does, it prints an error message and exits the script.

if (-e $dest_file) {
    die "File $dest_file already exists.\n";
}

# This line uses the built-in Perl function link() to create a hard link
# between $src_file and $dest_file. If the link() function fails, it
# prints an error message and exits the script.

link($src_file, $dest_file) or die "Can't create link: $!\n";


print "Hard link created from $src_file to $dest_file.\n";


