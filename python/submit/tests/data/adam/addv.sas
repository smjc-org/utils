/*
Top-Level Comment
*/

proc datasets library = work memtype = data kill noprint;
quit;

dm ' log; clear; output; clear; odsresult; clear; ';

/*SUBMIT BEGIN*/
proc sql noprint;
    create table work.dv as select * from rawdata.dv;
quit;

proc sql noprint;
    create table work.addv as select * from ae;
quit;
/*SUBMIT END*/

%LOG;
%ERROR;