#!/usr/bin/perl

use strict;
use warnings;

# Get the command-line arguments
my $user = $ARGV[0];
my $file = $ARGV[1];

# Get the UID for the specified user
my $uid = getpwnam($user);

# Check that the user exists
if (!defined($uid)) {
    die "User $user does not exist\n";
}

# Get the current permissions of the file
my $mode = (stat($file))[2];

# Set the new owner for the file
if (!chown($uid, -1, $file)) {
    die "Unable to change ownership of $file: $!\n";
}

# Set the permissions of the file
if (!chmod($mode & 07777, $file)) {
    die "Unable to change permissions of $file: $!\n";
}

# Print a message indicating that the ownership has been changed
print "Ownership of $file has been changed to $user\n";

