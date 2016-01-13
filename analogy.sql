create table mrrel_vocab_excise(cui1 text, cui2 text, word1 text, word2 text, rela text);
insert into mrrel_vocab_excise
select distinct
	r.cui1
	,r.cui2
	,lower(r.term1) as word1
	,lower(r.term2) as word2
	,r.rela
from
	mrrel_vocab r
where
	r.rela = 'procedure_has_excised_anatomy';

.mode csv
.headers on
.out mrrel_vocab_excise.csv
select * from mrrel_vocab_excise;
