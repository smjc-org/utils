/*
Top-Level Comment
*/

proc datasets library = work memtype = data kill noprint;
quit;

dm ' log; clear; output; clear; odsresult; clear; ';

/*SUBMIT BEGIN*/
proc sql noprint;
    create table work.ae as select * from rawdata.ae;
quit;

proc sql noprint;
    create table work.adae as select * from ae;
quit;
/*SUBMIT END*/

/*NOT SUBMIT BEGIN*/
proc report;
quit;
/*NOT SUBMIT END*/

%LOG;
%ERROR;