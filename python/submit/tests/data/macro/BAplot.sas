%macro BAplot(indata, var, outdata);
    data _tmp1;
        set &indata;
    run;

    proc sql noprint;
        create table _tmp2 as select * from _tmp1;
    quit;

    data &outdata;
        set _tmp2;
    run;

    /*NOT SUBMIT BEGIN*/
    proc template;
        define statgraph BAplot;
            begingraph;
                entrytitle "BA Plot";
                layout overlay;
                    scatterplot x=Period y=BA / group=Subject;
                endlayout;
            endgraph;
        end;
    run;

    proc sgrender data=&outdata template=BAplot;
    run;
    /*NOT SUBMIT END*/
%mend BAplot;