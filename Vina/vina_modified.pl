#!/usr/bin/perl

print "Ligand_file:\t";
$ligfile = <STDIN>;
chomp $ligfile;
open(FH, $ligfile) || die "Cannot open file\n";
@arr_file = <FH>;
close FH;

open(MASTER_LOG, '>', 'master_log.log') || die "Cannot open master log file\n";

foreach $file (@arr_file) {
    chomp $file;
    print "$file\n";
    my $command = "vina --config conf.txt --ligand $file";
    my $output = `$command 2>&1`;  # Capture both stdout and stderr
    print MASTER_LOG "\n\n\n";   # Leave three empty lines
    print MASTER_LOG "============= $file Log =============\n";
    print MASTER_LOG $output;
    open(LOG, '>', "${file}_log.log") || die "Cannot open log file ${file}_log.log\n";
    print LOG $output;
    close LOG;
}

close MASTER_LOG;
