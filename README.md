noid-minter
===========

This is an [Archival Resource Key (ARK)](https://arks.org/about/) minter.
It is based on John A. Kunze's [Nice Opaque Identifiers (Noid)](https://legacy-n2t.n2t.net/e/noid.html)
software, but differs from Noid in at least the following respects.

First, the scope is greatly reduced. This software handles minting only, not
binding or resolving. Minting is fundamentally a simple mathematical operation,
and this reduction in scope allows this simplicity to surface. In contrast,
Noid performs minting, binding, and resolving, and successors such as 
[eggnog](https://github.com/CDLUC3/n2t-eggnog) split these services.

Similarly, while this software allows for serialization and deserialization
using JSON as a transport language, it takes no responsibility for the data
at rest. Hence this package is not suitable by itself for a minting service.
Noid uses [BerkeleyDB](https://www.oracle.com/database/technologies/related/berkeleydb.html)
for storage, and Noid's `dbcreate` method encodes metadata specific to the
version of BerkeleyDB used on creation that may complicate data migrations.
We believe that using JSON as a transport language for the small amount of
metadata required by a minter will help keep minter services mobile.

Finally, we are explicit about our choice of pseudo-random number generator (PRNG):
[rand48](https://pubs.opengroup.org/onlinepubs/9699919799/functions/drand48.html).
When Noid was originally written in Perl, the Perl language relied on the PRNG
provided by the system on which it was running. On many Unix systems, this was
rand48, and in [Perl 5.19.4](https://metacpan.org/release/SHAY/perl-5.19.4/view/pod/perldelta.pod#rand_now_uses_a_consistent_random_number_generator),
the language standardized on rand48. We have chosen to use this PRNG to allow minter
databases that were created with Noid on Unix systems to be migrated to
noid-minter and mint new identifiers in a compatible, replayable manner.
The rand48 PRNG has known defects for pseudo-random number generation. However,
we are using it not for pseudo-randomness but first for uniform mixing of the sequence
of identifiers generated, so that two identifiers minted together are likely to be
quite different, and second for replayability of minting sequences, so that minters
can be migrated easily.

Users may want to bring their own PRNG to use with a minter. While support for other
PRNGs is not a current priority, we are opening to providing support for pluggable
PRNGs for minter. We welcome suggestions and code.

This code is just a snapshot! It is still in development.

License
-------

Copyright (C) 2024 MLE Slone. Licensed under the [MIT license](LICENSE.md).
