#!/usr/bin/env perl

use strict;
use warnings;

use Finance::Quote;
use JSON;
use POSIX qw(strftime);

my $module = $ARGV[0];
my $isin = $ARGV[1];

use Data::Dumper qw(Dumper);

my $q = Finance::Quote->new;
my %info = ();

if ($module eq "CURRENCY") {
    my $symbol_a = substr($isin, 0, 3);
    my $symbol_b = substr($isin, -3,3);
    %info = (
	"$isin-price"    => $q->currency($symbol_a, $symbol_b),
	"$isin-date"     => strftime("%m/%d/%Y", localtime),
        "$isin-currency" => $symbol_b,
	)
} else {
    %info = $q->fetch($module, $isin);
}
print encode_json \%info;
