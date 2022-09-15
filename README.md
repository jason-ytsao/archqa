### Customized script for processing 'CSME IE OCS Hardware Architecture Features Per Project.xlsm'

<br />

### Functions - 

1. Customized for HW architecture features comparison between 
- 'CSME IE OCS Hardware Architecture Features Per Project.xlsm' and 
- HW arch features config file from ArchGUI database
2. Formatting HW architecture features config file from ArchGUI database
3. Comparisons between two HW architecture features config files from ArchGUI database

<br />

### --help (-h)
```
$ ./archqa.py -h
usage: ./archqa.py [-h] {diff_gd,diff_dd,format} ...

Customized for processing 'CSME IE OCS Hardware Architecture Features Per
Project.xlsm'

positional arguments:
  {diff_gd,diff_dd,format}
    diff_gd             Compare two HW arch features config files: 'CSME IE
                        OCS Hardware Architecture Features Per Project.xlsm'
                        VS. HW arch features config from ArchGUI database
    diff_dd             Compare two HW arch features config files, both from
                        ArchGUI database
    format              Format HW arch features config file from ArchGUI
                        database

optional arguments:
  -h, --help            show this help message and exit

```
```
$ ./archqa.py diff_gd -h
usage: ./archqa.py diff_gd [-h] [-g] -d  [-o]

optional arguments:
  -h, --help        show this help message and exit
  -g , --golden     'CSME IE OCS Hardware Architecture Features Per
                    Project.xlsm'
  -d , --database   HW arch features config file from ArchGUI database
  -o , --out_dir    Output directory, default "archqa_outputs"

```
```
$ ./archqa.py diff_dd -h
usage: ./archqa.py diff_dd [-h] -f1  -f2  [-o]

optional arguments:
  -h, --help       show this help message and exit
  -f1 , --file1    HW arch features config file1 from ArchGUI database
  -f2 , --file2    HW arch features config file2 from ArchGUI database
  -o , --out_dir   Output directory, default "archqa_outputs"

```
```
$ ./archqa.py format -h
usage: ./archqa.py format [-h] -f  [-o]

optional arguments:
  -h, --help       show this help message and exit
  -f , --file      HW arch features config file from ArchGUI database
  -o , --out_dir   Output directory, default "archqa_outputs"

```
<br />


### Example 1:
To compare 'CSME IE OCS Hardware Architecture Features Per Project.xlsm' and 'ProjectConfig_2022-09-02_17_37_49.xlsx' from ArchGUI. If -g is not provided, it will be set to default, 'CSME IE OCS Hardware Architecture Features Per Project.xlsm' in the current directory. If -o is not provided, it will be set to default, "archqa_outputs" dir under the current directory.
  ```
  $ ./archqa.py diff_gd \
  -g 'CSME IE OCS Hardware Architecture Features Per Project.xlsm' \
  -d ProjectConfig_2022-09-02_17_37_49.xlsx \
  -o out_dir
  ```
### Example 2:
To format ProjectConfig_2022-09-13_16_10_30.xlsx from ArchGUI. If -o is not provided, it will be set to default, "archqa_outputs" dir under the current directory.
  ```
  $ ./archqa.py format \
  -f ProjectConfig_2022-09-13_16_10_30.xlsx \
  -o out_dir
  ```
### Example 3:
To compare two HW arch features config files from ArchGUI database. If -o is not provided, it will be set to default, "archqa_outputs" dir under the current directory.
  ```
  $ ./archqa.py diff_dd \
  -f1 /c/Users/jtsaox/mybin/ProjectConfig_2022-09-02_17_37_49.xlsx \
  -f2 /c/Users/jtsaox/mybin/ProjectConfig_2022-09-13_16_10_30.xlsx \
  -o out_dir
  ```