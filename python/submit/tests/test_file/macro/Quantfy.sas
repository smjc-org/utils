%macro Quantify(indata, var, outdata);
    data _tmp1;
        set &indata;
    run;

    proc sql noprint;
        create table _tmp2 as select * from _tmp1;
    quit;

    data &outdata;
        set _tmp2;
    run;
%mend Quantify;