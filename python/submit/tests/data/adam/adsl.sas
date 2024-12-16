/*
Top-Level Comment
*/

proc datasets library = work memtype = data kill noprint;
quit;

dm ' log; clear; output; clear; odsresult; clear; ';

/*SUBMIT BEGIN*/
proc sql noprint;
    create table work.fp as select * from rawdata.fp;
quit;

proc sql noprint;
    create table work.adsl as select * from fp;
quit;
/*SUBMIT END*/

%LOG;
%ERROR;