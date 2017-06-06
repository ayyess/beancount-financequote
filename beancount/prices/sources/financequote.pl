#!/usr/bin/env perl

use Finance::Quote;

my $module = $ARGV[0];
my $isin = $ARGV[1];

my $q = Finance::Quote->new;

my %info = $q->fetch($module, $isin);

print $info{$isin,"currency"}.','.$info{$isin,"date"}.','.$info{$isin,"price"};
