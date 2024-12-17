# submit.py

本程序用于从 `.sas` 文件中提取需要递交至监管机构的代码，并另存为 `.txt` 格式的文件。

## 安装

在终端中执行以下命令：

```bash
pip install git+https://github.com/smjc-macro/utils.git@main&subdirectory=python/submit
```

该命令将会在系统中注册 `submit` 命令，以便后续使用。

## 如何使用

`submit` 命令会识别 `.sas` 文件中的特殊注释，根据这些注释，删除多余的代码片段，保留需要递交的代码片段。

`submit` 命令可以识别的特殊注释如下：

- `/* SUBMIT BEGIN */`: 指定**需要**提交的代码的**起始**位置
- `/* SUBMIT END */`: 指定**需要**提交的代码的**终止**位置
- `/* NOT SUBMIT BEGIN*/`: 指定**无需**提交的代码的**起始**位置
- `/* NOT SUBMIT END */`: 指定**无需**提交的代码的**终止**位置

举例：

```sas
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
```

经 `submit` 命令处理之后将会变成：

```sas
proc sql noprint;
    create table work.adsl as select * from rawdata.adsl;
quit;

proc sql noprint;
    create table work.t_6_1_1 as select * from adsl;
quit;
```

### 处理单个 SAS 文件

子命令 `copyfile` 用于处理单个 `.sas` 文件。

```bash
submit copyfile "adae.sas" "adae.txt"
submit cpf "adae.sas" "adae.txt"
```

> [!TIP]
>
> `cpf` 是 `copyfile` 的别名（_alias_），大多数选项都具有别名，可通过 `--help` 命令查看。

#### --convert-mode

`--convert-mode` 选项用于指定处理模式，可选值为：`positive`, `negative`, `both`，默认为 `both`。

- `positive`: 仅处理 `/* SUBMIT BEGIN */`, `/* SUBMIT END */`
- `negative`: 仅处理 `/* NOT SUBMIT BEGIN*/`, `/* NOT SUBMIT END */`
- `both`: 同时处理所有四个特殊注释

> [!IMPORTANT]
>
> `/* NOT SUBMIT BEGIN*/`, `/* NOT SUBMIT END */` 的处理优先级高于 `/* SUBMIT BEGIN */`, `/* SUBMIT END */`。

```bash
submit copyfile --convert-mode negative
```

上述命令将会把：

```sas
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
```

处理为：

```sas
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


%mend BAplot;
```

#### --encoding

`--encoding` 选项指定 `.sas` 文件的编码格式。若未指定该选项，将尝试猜测最有可能的编码格式，并用于后续处理。

```bash
submit copyfile --convert-mode negative --encoding gbk
```

### 处理多个 SAS 文件

子命令 `copydir` 用于处理包含 `.sas` 文件的目录，该命令将以递归的方式自动查找扩展名为 `.sas` 的文件并进行处理，非 `.sas` 文件将被忽略。

```bash
submit copydir "/source" "/dest"
```

`copydir` 也支持 [`--convert-mode`](#--convert-mode) 和 [`--encoding`](#--encoding) 选项，用法相同。

#### --exclude-dirs

`--exclude-dirs` 选项指定排除的目录列表，这些目录中的文件将会被跳过处理。

```bash
submit copydir "/source" "/dest" --exclude-dirs macro
```

可同时指定多个目录：

```bash
submit copydir "/source" "/dest" --exclude-dirs macro qc initial
```

上述命令将在目录名称匹配 `macro`, `qc` 或 `initial` 时跳过处理其中的文件。

#### --exclude-files

`--exclude-files` 选项指定排除的文件列表，这些文件将会被跳过处理。

```bash
submit copydir "/source" "/dest" --exclude-dirs macro --exclude-files fcmp.sas format.sas
```

上述命令将在目录名称匹配 `macro` 时跳过处理其中的文件，并在文件名称匹配 `fcmp.sas` 或 `format.sas` （无论是否在 `macro` 目录中）时跳过处理。

## 命令行选项参考

### submit copyfile

```bash
usage: submit [options] copyfile [-h] [-c {positive,negative,both}] [--encoding ENCODING] sas_file txt_file

positional arguments:
  sas_file              SAS 文件路径
  txt_file              TXT 文件路径

options:
  -h, --help            show this help message and exit
  -c, --convert-mode {positive,negative,both}
                        转换模式（默认 both）
  --encoding ENCODING   编码格式（默认自动检测）
```

### submit copydir

```bash
usage: submit [options] copydir [-h] [-c {positive,negative,both}] [--encoding ENCODING] [-exf [EXCLUDE_FILES ...]] [-exd [EXCLUDE_DIRS ...]] sas_dir txt_dir

positional arguments:
  sas_dir               SAS 文件目录
  txt_dir               TXT 文件目录

options:
  -h, --help            show this help message and exit
  -c, --convert-mode {positive,negative,both}
                        转换模式（默认 both）
  --encoding ENCODING   编码格式（默认自动检测）
  -exf, --exclude-files [EXCLUDE_FILES ...]
                        排除文件列表（默认无）
  -exd, --exclude-dirs [EXCLUDE_DIRS ...]
                        排除目录列表（默认无）
```

## bat 脚本编写指南

`.bat` 文件是一种[批处理文件](https://en.wikipedia.org/wiki/Batch_file)，你可以将多条 `submit` 命令保存在单个 `.bat` 文件中，这样只需单击这个文件即可批量处理 `.sas` 文件。

例如：

```bash
submit copydir "D:/project/code/adam" "D:/project/submit/adam"
submit copydir "D:/project/code/tfl" "D:/project/submit/tfl" --exclude-files merge.sas
submit copydir "D:/project/code/macro" "D:/project/submit/macro" --convert-mode negative
```
