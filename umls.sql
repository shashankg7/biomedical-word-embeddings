-- vocab

create table vocab (term text);
.separator ","
.import vocab.csv vocab

-- mrconso_vocab

create table mrconso_vocab (cui text, term text);
insert into mrconso_vocab
select distinct
	c.cui
	,replace(c.str, ' ', '-') as term
from
	mrconso c
where
	term in (select v.term from vocab v);

create index idx_mrconso_vocab_cui on mrconso_vocab(cui);

-- mrsty_vocab

create table mrsty_vocab(cui text, term text, sty text);
insert into mrsty_vocab
select
	c.cui
	,c.term
	,s.sty
from
	mrsty s
	join mrconso_vocab c on c.cui = s.cui; 

-- mrrel_vocab

create table mrrel_vocab (cui1 text, cui2 text, term1 text, term2 text, rela text);
insert into mrrel_vocab
select
	r.cui1
	,r.cui2
	,c1.term as term1
	,c2.term as term2
	,r.rela
from
	mrrel r
	join mrconso_vocab c1 on c1.cui = r.cui1
	join mrconso_vocab c2 on c2.cui = r.cui2;

create index idx_mrrel_vocab_term1 on mrrel_vocab(term1);

-- export

.mode csv
.headers on
.out mrsty_vocab.csv
select * from mrsty_vocab;
