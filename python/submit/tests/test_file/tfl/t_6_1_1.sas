/*
Top-Level Comment
*/

proc datasets library = work memtype = data kill noprint;
quit;

dm ' log; clear; output; clear; odsresult; clear; ';

/*SUBMIT BEGIN*/
proc sql noprint;
    create table work.adsl as select * from rawdata.adsl;
quit;

proc sql noprint;
    create table work.t_6_1_1 as select * from adsl;
quit;
/*SUBMIT END*/

%LOG;
%ERROR;
