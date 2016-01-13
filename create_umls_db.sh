sudo apt-get install sqlite3
sudo apt-get install s3cmd
s3cmd --configure
# s3cmd get s3://umls-bucket/umls-data/umls.db umls.db
s3cmd get s3://umls-bucket/umls-data/2015AB/META/MRCONSO.RRF MRCONSO.RRF
s3cmd get s3://umls-bucket/umls-data/2015AB/META/MRSTY.RRF MRSTY.RRF
s3cmd get s3://umls-bucket/umls-data/2015AB/META/MRREL.RRF MRREL.RRF

# doesn't import correctly with doublequotes
sed 's/"/\<DOUBLEQUOTE\>/g' MRCONSO.RRF > MRCONSO_FORMATTED.RRF

sqlite3 umls.db

create table mrconso(CUI text, LAT text, TS text, LUI text, STT text, SUI text, ISPREF text, AUI text, SAUI text, SCUI text, SDUI text, SAB text, TTY text, CODE text, STR text, SRL text, SUPPRESS text, CVF text, PLACEHOLDER text);
.separator "|"
.import MRCONSO_FORMATTED.RRF mrconso

create table mrsty(CUI text, TUI text, STN text, STY text, ATUI text, CVF text, PLACEHOLDER text);
.separator "|"
.import MRSTY.RRF mrsty

create table mrrel(CUI1 text, AUI1 text, STYPE1 text, REL text, CUI2 text, AUI2 text, STYPE2 text, RELA text, RUI text, SRUI text, SAB text, SL text, RG text, DIR text, SUPPRESS text, CVF text, PLACEHOLDER text);
.separator "|"
.import MRREL.RRF mrrel

create index idx_mrconso_cui on mrconso(cui);
create index idx_mrrel_cui1 on mrrel(cui1);
create index idx_mrrel_cui2 on mrrel(cui2);
create index idx_mrsty_cui on mrsty(cui);

s3cmd put umls.db s3://umls-bucket/
