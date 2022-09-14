### Customized script for processing 'CSME IE OCS Hardware Architecture Features Per Project.xlsm'

<br />

### Functions - 

1. Customized for HW architecture features comparison between 
- 'CSME IE OCS Hardware Architecture Features Per Project.xlsm' and 
- HW arch features config file from ArchGUI database
2. Formatting HW architecture features config file from ArchGUI database
3. Comparisons between two HW architecture features config files from ArchGUI database

<br />
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
<br />


### Example 1:
  ```
  $ ./archqa.py diff_gd \
  -g 'CSME IE OCS Hardware Architecture Features Per Project.xlsm' \
  -d ProjectConfig_2022-09-02_17_37_49.xlsx \
  -o out_dir
  ```
### Example 2:
  ```
  $ ./archqa.py format -f ProjectConfig_2022-09-13_16_10_30.xlsx -o out_dir
  ```
### Example 3:
  ```
  $ ./archqa.py diff_dd \
  -f1 /c/Users/jtsaox/mybin/ProjectConfig_2022-09-02_17_37_49.xlsx \
  -f2 /c/Users/jtsaox/mybin/ProjectConfig_2022-09-13_16_10_30.xlsx \
  -o out_dir
  ```