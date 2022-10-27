<!-- ### Customized script for CSME IE OCS Hardware Architecture Features Config -->
# User Guide for archqa.py
## Functions - 
1. Customized for HW architecture features and config comparison between this two -
   - `'CSME IE OCS Hardware Architecture Features Per Project.xlsm'`
   -  HW arch features config sheet from ArchGUI database
2. Comparison between two HW arch features config sheets from ArchGUI database
3. Comparison between two sheets (*.xlsx)
4. Formatting `HW arch features config sheet` `(ProjectConfig_<yyyy-mm-dd_xx_xx_xx>.xlsx)` from ArchGUI database

#### [Note] :
The comparison checks only **"Block"**, **"Feature"**, and **"config"** for each IP.

## Usage - 
There are four functions that can be triggered by four different arguments respectively - *difffgd*, *diffdd*, *diffxlsx*, *format*
```
$ ./archqa.py -h
usage: archqa.py [-h] {diffgd,diffdd,diffxlsx,format} ...

Customized for processing 'CSME IE OCS Hardware Architecture Features Per
Project.xlsm'

positional arguments:
  {diffgd,diffdd,diffxlsx,format}
    diffgd              To compare two HW arch features config sheets: 'CSME
                        IE OCS Hardware Architecture Features Per
                        Project.xlsm' VS. HW arch features config sheet from ArchGUI database
    diffdd              To compare two HW arch features config sheets, both
                        from ArchGUI database
    diffxlsx            A quick checker to test whether two xlsx files have
                        the same shape and the same elements, Only dump out a
                        comparison report when two objects are in the same
                        shape but NOT Equivalent
    format              To format HW arch features config sheet from ArchGUI
                        database

optional arguments:
  -h, --help            show this help message and exit
```

## __diffgd__ -  <br>
To compare `'CSME IE OCS Hardware Architecture Features Per Project.xlsm'` and `HW arch features config sheet` `(ProjectConfig_<yyyy-mm-dd_xx_xx_xx>.xlsx)` from ArchGUI database.
```
$ ./archqa.py diffgd -h
usage: archqa.py diffgd [-h] [-g] -d  [-o]

optional arguments:
  -h, --help        show this help message and exit
  -g , --golden     'CSME IE OCS Hardware Architecture Features Per
                    Project.xlsm'
  -d , --database   HW arch features config file from ArchGUI database
  -o , --out_dir    Output directory, default "archqa_outputs"
```
#### Example :
```
$ ./archqa.py diffgd \
-g 'CSME IE OCS Hardware Architecture Features Per Project.xlsm' \
-d ProjectConfig_2022-09-02_17_37_49.xlsx \
-o out_dir
```
If -g is not provided, the script will pick up 'CSME IE OCS Hardware Architecture Features Per Project.xlsm' in the current directory if it exists.
```
$ ./archqa.py diffgd \
-d ProjectConfig_2022-09-02_17_37_49.xlsx \
-o out_dir
```
If '-o' is not provided, the output dir will be set to default, "archqa_outputs" dir under the current directory.
```
$ ./archqa.py diffgd \
-d ProjectConfig_2022-09-02_17_37_49.xlsx 
```
Output Files | Description
-------| ------------
output_diffbf.xlsx | The sheet that shows the discrepancies in respect to column `Block` and `Feature`
output_diffbf_exrtradb.xlsx | The sheet that lists `Block` and `Feature` that are found in ArchGUI database but are NOT found in `'CSME IE OCS Hardware Architecture Features Per Project.xlsm'`
output_diffbf_extragolden.xlsx | The sheet that lists `Block` and `Feature` that are found in `'CSME IE OCS Hardware Architecture Features Per Project.xlsm'` but are NOT found in ArchGUI database
output_diffcfg.xlsx | The sheet that shows all the discrepancies of `Block`, `Feature` and `Config` from comparison
output_diffcfg_db.xlsx | The sheet that lists `Block`, `Feature` and `Config` that are found in ArchGUI database but are NOT found in `'CSME IE OCS Hardware Architecture Features Per Project.xlsm'`
output_diffcfg_golden.xlsx | The sheet that lists `Block`, `Feature` and `Config` that are found in `'CSME IE OCS Hardware Architecture Features Per Project.xlsm'` but are NOT found in ArchGUI database
output_matched.xlsx | The sheet that lists all the matched `Block`, `Feature` and `Config` from comparison
output_extract_sorted_db.xlsx | Sorted HW arch features config sheet extracted from ArchGUI database that contains only column `Block`, `Feature` and `Config`
output_extract_sorted_golden.xlsx | Sorted sheet extracted from `'CSME IE OCS Hardware Architecture Features Per Project.xlsm'` that contains only column `Block`, `Feature` and `Config`
output_feature_names_mapping_db.xlsx | The sheet that lists `Feature` names from ArchGUI database that have been modified or changed for mapping to the ones in `'CSME IE OCS Hardware Architecture Features Per Project.xlsm'`
output_feature_names_mapping_golden.xlsx | The sheet that lists `Feature` names from `'CSME IE OCS Hardware Architecture Features Per Project.xlsm'` that have been modified or changed for mapping to the ones in ArchGUI database 
output_formatted_ProjectConfig_<yyyy-mm-dd_xx_xx_xx>.xlsx | The formatted version of `HW arch features config sheet` `(ProjectConfig_<yyyy-mm-dd_xx_xx_xx>.xlsx)` from ArchGUI database
output_waived_golden.xlsx | The sheet that lists waived `Block`, `Feature` and `Config` from `'CSME IE OCS Hardware Architecture Features Per Project.xlsm'`, that are not included for comparison 
output_diffss.xlsx | The sheet shows the highlight on the cells that contain discrepancies. This file is only available when both sheets have the same shape and matched `Block` and `Feature` pairs.

## **diffdd** -  <br>
To compare two `HW arch features config sheets` `(ProjectConfig_<yyyy-mm-dd_xx_xx_xx>.xlsx)` from ArchGUI database.
```
$ ./archqa.py diffdd -h
usage: archqa.py diffdd [-h] -f1  -f2  [-o]

optional arguments:
  -h, --help       show this help message and exit
  -f1 , --file1    HW arch features config file1 from ArchGUI database
  -f2 , --file2    HW arch features config file2 from ArchGUI database
  -o , --out_dir   Output directory, default "archqa_outputs"
```
#### Example :
If '-o' is not provided, the output directory will be set to default, "archqa_outputs" dir under the current directory.
```
$ ./archqa.py diffdd \
-f1 /c/Users/jtsaox/mybin/ProjectConfig_2022-09-02_17_37_49.xlsx \
-f2 /c/Users/jtsaox/mybin/ProjectConfig_2022-09-13_16_10_30.xlsx \
-o out_dir
```
| Output Files | Description |
| -------| ------------|
| output_diffbf.xlsx | The sheet that shows the discrepancies in respect to column `Block` and `Feature` |
| output_diffbf_extra_ProjectConfig_<yyyy-mm-dd_xx_xx_xx>.xlsx | The sheet that lists `Block` and `Feature` that are found in `ProjectConfig_<yyyy-mm-dd_xx_xx_xx>.xlsx` but are NOT found in the other sheet |
| output_diffcfg.xlsx | The sheet that shows all the discrepancies of `Block`, `Feature` and `Config` from comparison |
| output_diffcfg_ProjectConfig_<yyyy-mm-dd_xx_xx_xx>.xlsx | The sheet that lists `Block`, `Feature` and `Config` that are found in `ProjectConfig_<yyyy-mm-dd_xx_xx_xx>.xlsx` but are NOT found in the other sheet |
| output_matched.xlsx | The sheet that lists all the matched `Block`, `Feature` and `Config` from comparison |
| output_extract_sorted_ProjectConfig_<yyyy-mm-dd_xx_xx_xx>.xlsx | Sorted sheet extracted from `ProjectConfig_<yyyy-mm-dd_xx_xx_xx>.xlsx` that contains only column `Block`, `Feature` and `Config` |
| output_formatted_ProjectConfig_<yyyy-mm-dd_xx_xx_xx>.xlsx | The formatted version of `HW arch features config sheet` `(ProjectConfig_<yyyy-mm-dd_xx_xx_xx>.xlsx)` from ArchGUI database |
| output_waived_golden.xlsx | The sheet that lists `Block`, `Feature` and `Config` from `'CSME IE OCS Hardware Architecture Features Per Project.xlsm'`, that are waived from comparison |
| output_diffss.xlsx | The sheet shows the highlight on the cells that contain discrepancies. This file is only available when both sheets have the same shape and matched `Block` and `Feature` pairs.

## **diffxlsx** - 
A quick answer to check if two sheets are equivalent. It only dumps out a report of discrepancy `'output_diffxlsx.xlsx'` when two sheets have exactly the same columns and the same shape.
```
$ ./archqa.py diffxlsx -h
usage: archqa.py diffxlsx [-h] -f   [-o]

optional arguments:
  -h, --help       show this help message and exit
  -f  , --files    Two xlsx files for comparison
  -o , --out_dir   Output directory, default "archqa_outputs". Only dump out a comparison report when two objects are in the same shape but have discrepancy
```
#### Example :
If -o is not provided, the output directory will be set to default, "archqa_outputs" dir under the current directory.
```
$ ./archqa.py diffxlsx \
-f sheet1.xlsx sheet2.xlsx \
-o out_dir
```
| Output Files | Description |
| -------| ------------|
| output_diffxlsx.xlsx | The sheet shows the highlight on the cells that contain discrepancies. This file is only available when both sheets have the same shape and matched columns. |

## **format** - 
To format `HW arch features config sheet` `(ProjectConfig_<yyyy-mm-dd_xx_xx_xx>.xlsx)` from ArchGUI database for a better view.
```
$ ./archqa.py format -h
usage: archqa.py format [-h] -f  [-o]

optional arguments:
  -h, --help       show this help message and exit
  -f , --file      HW arch features config file from ArchGUI database
  -o , --out_dir   Output directory, default "archqa_outputs"
```
#### Example :
If '-o' is not provided, the output directory will be set to default, "archqa_outputs" dir under the current directory.
  ```
  $ ./archqa.py format \
  -f ProjectConfig_2022-09-13_16_10_30.xlsx \
  -o out_dir
  ```
| Output Files | Description |
| -------| ------------|
| output_formatted_ProjectConfig_<yyyy-mm-dd_xx_xx_xx>.xlsx | The formatted version of `HW arch features config sheet` `(ProjectConfig_<yyyy-mm-dd_xx_xx_xx>.xlsx)` from ArchGUI database |
