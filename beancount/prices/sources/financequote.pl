#!/usr/bin/env perl

use Finance::Quote;
use JSON;

my $module = $ARGV[0];
my $isin = $ARGV[1];

my $q = Finance::Quote->new;

my %info = $q->fetch($module, $isin);

print encode_json \%info;
