### Customized script for processing 'CSME IE OCS Hardware Architecture Features Per Project.xlsm'

<br />

### Functions - 

1. Customized for HW architecture features comparison between 
   - 'CSME IE OCS Hardware Architecture Features Per Project.xlsm' and 
   -  HW arch features config file from ArchGUI database
2. Formatting HW architecture features config file from ArchGUI database
3. Comparison between two HW architecture features config files from ArchGUI database

#### [Note] :
The comparison checks only column **"Block"**, **"Feature"**, and **"config column for each 'platform plus project'"**.

<br />

### Usage - 
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

### Output Files -
- diff_gd
  - output_extract_sorted_db.xlsx 
    - Sorted file that contains only column **"Block"**, **"Feature"**, and **"config column for each 'platform plus project'"** from ArchGUI database
  - output_extract_sorted_golden.xlsx
    - Sorted file that contains only column **"Block"**, **"Feature"**, and **"config column for each 'platform plus project'"** from 'CSME IE OCS Hardware Architecture Features Per Project.xlsm'
  - output_diffcfg.xlsx
    - File that shows all the discrepancies from comparison
  - output_matched.xlsx
    - File that shows all the matches from comparison
  - output_diffcfg_golden.xlsx
    - File that shows items only found to exist in 'CSME IE OCS Hardware Architecture Features Per Project.xlsm' but could not find exactly the same ones in ArchGUI database
  - output_diffcfg_db.xlsx
    - File that shows items only found to exist in ArchGUI database but could not find exactly the same ones in 'CSME IE OCS Hardware Architecture Features Per Project.xlsm'
  - output_diffbf_extragolden.xlsx
    - File that shows the discrepancies in respect to column **"Block"** and **"Feature"**, only found to exist in 'CSME IE OCS Hardware Architecture Features Per Project.xlsm' but could not find exactly the same ones in ArchGUI database 
  - output_diffbf_exrtradb.xlsx
    - File that shows the discrepancies in respect to column **"Block"** and **"Feature"**, only found to exist in ArchGUI database but could not find exactly the same ones in 'CSME IE OCS Hardware Architecture Features Per Project.xlsm' 
  - output_formatted_ProjectConfig_2022-09-13_16_10_30.xlsx
    - The formatted file that preserves all the content from original spreadsheet downloaded from ArchGUI database

- diff_dd
  - output_formatted_ProjectConfig_2022-09-13_16_10_30.xlsx
    - The formatted file that preserves all the content from ProjectConfig_2022-09-13_16_10_30.xlsx
  - output_formatted_ProjectConfig_2022-09-13_16_10_30_2B.xlsx
      - The formatted file that preserves all the content from ProjectConfig_2022-09-13_16_10_30_2B.xlsx
  - output_extract_sorted_ProjectConfig_2022-09-13_16_10_30.xlsx
    - Sorted file that contains only column **"Block"**, **"Feature"**, and **"config column for each 'platform plus project'"** from ProjectConfig_2022-09-13_16_10_30.xlsx
  - output_extract_sorted_ProjectConfig_2022-09-13_16_10_30_2B.xlsx
    - Sorted file that contains only column **"Block"**, **"Feature"**, and **"config column for each 'platform plus project'"** from ProjectConfig_2022-09-13_16_10_30_2B.xlsx
  - output_diffcfg.xlsx
    - File that shows all the discrepancies from comparison
  - output_matched.xlsx
    - File that shows all the matches from comparison
  - output_diffcfg_ProjectConfig_2022-09-13_16_10_30.xlsx
    - File that shows items only found to exist in 'ProjectConfig_2022-09-13_16_10_30.xlsx' but could not find exactly the same ones in 'ProjectConfig_2022-09-13_16_10_30_2B.xlsx'
  - output_diffcfg_ProjectConfig_2022-09-13_16_10_30_2B.xlsx
    - File that shows items only found to exist in 'ProjectConfig_2022-09-13_16_10_30_2B.xlsx' but could not find exactly the same ones in 'ProjectConfig_2022-09-13_16_10_30.xlsx'
  - output_diffbf_extra_ProjectConfig_2022-09-13_16_10_30.xlsx
    - File that shows the discrepancies in respect to column **"Block"** and **"Feature"**, only found to exist in 'ProjectConfig_2022-09-13_16_10_30.xlsx' but could not find exactly the same ones in 'ProjectConfig_2022-09-13_16_10_30_2B.xlsx'
  - output_diffbf_exrtra_ProjectConfig_2022-09-13_16_10_30_2B.xlsx
    - File that shows the discrepancies in respect to column **"Block"** and **"Feature"**, only found to exist in 'ProjectConfig_2022-09-13_16_10_30_2B.xlsx' but could not find exactly the same ones in 'ProjectConfig_2022-09-13_16_10_30.xlsx'

- format
  - output_formatted_ProjectConfig_2022-09-13_16_10_30.xlsx
    - The formatted version of 'ProjectConfig_2022-09-13_16_10_30.xlsx'