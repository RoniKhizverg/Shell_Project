#!/usr/bin/perl

# The "chmod" command (short for "change mode") is a Unix/Linux command that is used to change the access permissions of files or directories.
# It allows you to modify the read, write, and execute permissions for the owner, group, and other users. 

use strict;
use warnings;

# Retrieve the mode and file arguments from command line
my $mode = shift;
my $file = shift;

# Check if both arguments have been provided
if (!defined $file || !defined $mode) {
    # Print a usage message and exit with non-zero status
    print "Usage: $0 file mode\n";
    exit 1;
}

# Check if the mode argument is in the expected format (e.g., u+rwx)
if ($mode !~ /^([ugo]*)([+-])([rwx]+)/) {
    # Print an error message and exit with non-zero status
    print "Invalid mode\n";
    exit 1;
}

# Extract the user, operation, and permissions parts from the mode
my ($users, $operation, $permissions) = ($1, $2, $3);

# Initialize the mode bits to zero
my $mode_bits = 0;

# Set the appropriate mode bits based on the requested permissions
if ($permissions =~ /r/) {
    $mode_bits |= 0b100;
}
if ($permissions =~ /w/) {
    $mode_bits |= 0b010;
}
if ($permissions =~ /x/) {
    $mode_bits |= 0b001;
}

# If no user is specified, set it to "ugo" (i.e., apply to all users)
$users = 'ugo' if !$users;

# Initialize an array of files to modify (in case the argument is a directory)
my @files = ();

# Check if the file argument is a directory
if (-d $file) {
    # Open the directory and read its contents
    opendir(my $dh, $file) || die "Can't open $file: $!";
    @files = readdir $dh;
    closedir $dh;
} else {
    # If the file argument is not a directory, add it to the list of files to modify
    push @files, $file;
}

# Loop through each file in the list
foreach my $file (@files) {
    # Retrieve the current permissions of the file
    my @stat = stat $file;
    my $cur_mode = $stat[2] & 07777;

    # Print the old permissions of the file
    printf("Before:\n");
    system("ls", "-l", $file);

    # Apply the requested changes to the appropriate bits of the mode
    if ($users =~ /u/) {
        if ($operation eq '+') {
            $cur_mode |= ($mode_bits << 6);
        } else {
            $cur_mode &= ~($mode_bits << 6);
        }
    }
    if ($users =~ /g/) {
        if ($operation eq '+') {
            $cur_mode |= ($mode_bits << 3);
        } else {
            $cur_mode &= ~($mode_bits << 3);
        }
    }
    if ($users =~ /o/) {
        if ($operation eq '+') {
            $cur_mode |= $mode_bits;
        } else {
            $cur_mode &= ~$mode_bits;
        }
    }

    # Set the new permissions of the file
    chmod $cur_mode, $file;

    # Print the new permissions of the file
    printf("After:\n");
    system("ls", "-l", $file);
}

