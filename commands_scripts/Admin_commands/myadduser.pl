#!/usr/bin/perl

use strict;
use warnings;

use User::pwent;       # This module provides a way to access system password and group files.
use Crypt::PasswdMD5;  # This module provides the "apache_md5_crypt" function for password encryption.

# This line reads the first command-line argument and assigns it to the $username variable.
my $username = shift @ARGV;
my $file = "/etc/passwd";

# This block checks if the $username variable is defined. If not, it prints an error message and exits.
if (!defined $username) {
  print "Invalid arguments\n";
  exit 1;
}

# This line tries to retrieve the user information from the system using the "getpwnam" function.
my $pw = getpwnam($username);

# This block checks if the $pw variable is defined. If it is, it means that the user already exists,
# so the script prints an error message and exits.
if (defined $pw) {
  print "User $username already exists\n";
  exit 1;
}

# These lines set some default values for the user's password, home directory, and shell.
my $password = "1234";
my $home_dir = "home/$username";
my $shell = "/bin/bash";

# This line generates a random UID in the range 1000-9999.
my $uid = int(rand(9000)) + 1000;

my $gid = 1000;

# This line encrypts the user's password using the "apache_md5_crypt" function.
my $enc_password = apache_md5_crypt($password);

# This line constructs a string with the user information in the format expected by the "/etc/passwd" file.
my $pw_info = "$username:$enc_password:$uid:$gid:$username:/$home_dir:$shell\n";

# This line opens the "/etc/passwd" file in append mode, or dies with an error message if it can't open the file.
open my $fh, '>>', $file or die "Cannot open $file: $!";

# This line writes the user information to the file.
print $fh $pw_info;

close $fh; # This line closes the file.

print "User $username has been added with UID $uid and GID $gid\nTo see it, write in terminal the following command: cat /etc/passwd\n";

exit 0;

