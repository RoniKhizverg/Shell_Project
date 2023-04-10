#!/usr/bin/perl

# Use strict and warnings to enable various safety checks and warnings
use strict;
use warnings;

# Import various Perl modules needed for this script
use File::stat;
use File::Basename;
use Getopt::Std;

# Define a hash to hold command-line options (-l, -r, -a)
my %opts;

# Parse command-line options and store them in the %opts hash
getopts('lra', \%opts);

# Get the directory path from the command-line arguments, or use the current directory if none is given
my $dir = $ARGV[0] || '.';

# Open the directory for reading and store the list of files in an array
opendir(my $dh, $dir) || die "can't opendir $dir: $!";
my @files = readdir($dh);
closedir($dh);

# If the -l option is given, sort the files alphabetically (ignoring case) and print them in long format
if ($opts{'l'}) {
    @files = sort { lc($a) cmp lc($b) } @files;
    foreach my $file (@files) {
        # If the -a option is given, include hidden files in the output
        if ($opts{'a'} || $file ne '.' && $file ne '..') {
            # Print the file in long format
            my $filename = "$dir/$file";
            print_with_longFormat($dir, $file);
        }
    }
}
# If the -a option is given, sort the files alphabetically (ignoring case) and print them all in a single line
elsif ($opts{'a'}) {
    @files = sort { lc($a) cmp lc($b) } @files;
    print join("\n", @files);
}
# If neither -l nor -a is given, sort the files alphabetically (ignoring case) and print them all in a single line
else {
    @files = sort { lc($a) cmp lc($b) } @files;
    # If -r is given, reverse the order of the files
    @files = reverse(@files) if $opts{'r'};
    # Filter out the "." and ".." entries and print the remaining files
    print join(" ", grep { $_ ne '.' && $_ ne '..' } @files), "\n";
}

# function to print a file's information in long format
sub print_with_longFormat {
    my ($dirPath, $file) = @_;
    my $filename = "$dirPath/$file";
    my $file_info = stat($filename);

    if (!defined $file_info) {
        # If stat fails, print an error message and return
        print "Could not get information for file $filename\n";
        return;
    }

    # Extract the file's mode (permissions), number of hard links, owner and group, size, and modification time from the stat object
    my $mode = $file_info->mode;
    my $permissions = sprintf("%04o", $mode & 07777);
    my $is_directory = (-d $filename);

    # Print the file's type (d for directories, - for regular files) and permissions
    if ($is_directory) {
        print "d";
    } else {
        print "-";
    }
    print (($mode & 0400) ? 'r' : '-');
    print (($mode & 0200) ? 'w' : '-');
    print (($mode & 0100) ? 'x' : '-');
    print (($mode & 0040) ? 'r' : '-');
    print (($mode & 0020) ? 'w' : '-');
    print (($mode & 0010) ? 'x' : '-');
    print (($mode & 0004) ? 'r' : '-');
    print (($mode & 0002) ? 'w' : '-');
    print (($mode & 0001) ? 'x' : '-');
    print " " . $file_info->nlink . " ";
    print getpwuid($file_info->uid) . " ";
    print getgrgid($file_info->gid) . " ";
    print $file_info->size . " ";
    print scalar localtime($file_info->mtime) . " ";
    print "$file\n";
}

