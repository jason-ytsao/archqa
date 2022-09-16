#!python
# jasonx.tsao@intel.com - [09/14/2022]

import pandas as pd
import argparse as aps
import re
import numpy as np
from pathlib import Path


class XlsxDiff:
    """
    1. Customized for HW architecture features comparisons between 
        a).'CSME IE OCS Hardware Architecture Features Per Project.xlsm' and 
        b).xlsx from ArchGUI database
    2. Formatting HW architecture features config file from ArchGUI database
    3. Comparisons between two HW architecture features config files from ArchGUI database
    """

    def __init__(self, out_dir, flag):
        self.df_extract_projs_start = 0
        self.flag = flag
        self.database_projs = []
        self.database_df_extract_BF = []
        pd.set_option('display.max_rows', 500)
        
        # OUTPUT FILES:
        self.cwd = Path.cwd()
        self.output_dir = out_dir
        self.p = Path(self.output_dir)
        self.p.mkdir(parents=True, exist_ok=True)
        if flag == 'diff_gd':
            self.wr_database_extract_sorted = f"{self.output_dir}/output_extract_sorted_db.xlsx"
            self.wr_golden_extract_sorted = f"{self.output_dir}/output_extract_sorted_golden.xlsx"
            self.wr_discrepancy = f"{self.output_dir}/output_diffcfg.xlsx"
            self.wr_matched = f"{self.output_dir}/output_matched.xlsx"
            self.wr_diff_golden = f"{self.output_dir}/output_diffcfg_golden.xlsx"
            self.wr_diff_database = f"{self.output_dir}/output_diffcfg_db.xlsx"
            self.wr_diffBF_golden = f"{self.output_dir}/output_diffbf_extragolden.xlsx"
            self.wr_diffBF_database = f"{self.output_dir}/output_diffbf_exrtradb.xlsx"
            self.wr_diffBF_all = f"{self.output_dir}/output_diffbf.xlsx"
        elif flag == 'diff_dd':
            self.wr_database_extract_sorted = ''
            self.wr_discrepancy = f"{self.output_dir}/output_diffcfg.xlsx"
            self.wr_matched = f"{self.output_dir}/output_matched.xlsx"
            self.wr_diff_golden = ''
            self.wr_diff_database = ''
            self.wr_diffBF_golden = ''
            self.wr_diffBF_database = '' 
            self.wr_diffBF_all = f"{self.output_dir}/output_diffbf.xlsx"


    def process_database(self, db):
        """
        Process xlsx downloaded from ArchGUI
        """
        self.format(db)
        database_df = pd.read_excel(db)
        database_slice_start = list(database_df.columns).index('Type Name') + 1
        database_cols_projIPG = sorted(database_df.columns[database_slice_start:])
        database_projs = [ x.split('_')[0] for x in database_cols_projIPG if re.search('_', x)]
        name_db = db.split('/')[-1].split('.')[-2]
        
        # uniquify database_projs
        self.database_projs = list(dict.fromkeys(database_projs))

        # set extract columns
        database_cols = ['Functional Block', 'Feature Name', *database_cols_projIPG]
        
        # extract columns
        database_df_extract = database_df.loc[:, database_cols]

        # Rename column labels
        database_df_extract.rename(columns={'Functional Block': 'Block', 'Feature Name': 'Feature'}, inplace=True)

        # 'Block' & 'Feature' DataFrame
        database_df_extract_projs_start = list(database_df_extract.columns).index('Feature') + 1
        self.database_df_extract_BF = database_df_extract.columns[:database_df_extract_projs_start].tolist()

        self.df_extract_projs_start = database_df_extract_projs_start


        # clean up strings in cell values
        for col in self.database_df_extract_BF:
            database_df_extract[col] = (
                self.feature_names_mapping(
                self.cleanup(database_df_extract[col]))
                )
        
        for col in database_cols_projIPG:
            database_df_extract[col] = (
                self.feature_names_mapping(
                self.cleanup(database_df_extract[col]))
                )

        # debug
        # database_df_extract.to_excel(f'database_df_extract_{name_db}.xlsx')

        # No MultiIndex, sort by values
        database_df_extract_sorted = (database_df_extract.sort_values(
            by=list(database_df_extract.columns)[:database_df_extract_projs_start]))

        # remove index col
        database_df_extract_sorted_ri = self.index_1st_col(database_df_extract_sorted)

        if self.flag == 'diff_gd':
            database_df_extract_sorted_ri.to_excel(self.wr_database_extract_sorted)
            print(f"Dumping file {self.cwd}/{self.wr_database_extract_sorted}")
            return database_df_extract_sorted
        elif self.flag == 'diff_dd':
            self.wr_database_extract_sorted = f"{self.output_dir}/output_extract_sorted_{name_db}.xlsx"
            database_df_extract_sorted_ri.to_excel(self.wr_database_extract_sorted)
            print(f"Dumping file {self.cwd}/{self.wr_database_extract_sorted}")
            return [database_df_extract_sorted, name_db]


    def process_golden(self, golden):
        """
        Process `CSME IE OCS Hardware Architecture Features Per Project.xlsm`
        """
        golden_df = pd.read_excel(golden, sheet_name='CSE CSME IE OCS Features', skiprows=1, index_col=None)

        # remove `Unnamed: 0` column
        golden_df = golden_df.loc[:, ~golden_df.columns.str.contains('^Unnamed', na=False, regex=True)]
        
        # strip 'Feature' 
        golden_df.loc[1, 2] = golden_df.loc[1, 2].strip()

        # unmerge column 1: Block, CPU, MISA ....
        golden_df[1] = pd.Series(golden_df[1]).fillna(method='ffill')
        
        # unmerge column cells
        golden_df.iloc[0, 3:] = golden_df.iloc[0, 3:].fillna(method='ffill')

        # unmerge Feature cell
        golden_df.loc[0:1, 2] = golden_df.loc[0:1, 2].fillna(method='bfill')

        # Remove footer garbage rows
        golden_df[2] = golden_df[2].fillna(np.nan)
        golden_df = golden_df.dropna(subset=[2])

        # Change golden_df.columns, 1, 2, 3...74, with 'Feature', 'IP Version Number: ', 'OCS 2.0'...
        golden_df.columns = golden_df.iloc[0]

        # Extract columns from golden_df
        golden_df_extract = golden_df.loc[:, ['Block', 'Feature', *self.database_projs]]

        # Remove the duplicate row, column labels
        golden_df_extract = golden_df_extract.drop(index=0)

        # relabel the index
        golden_df_extract.reset_index(drop=True, inplace=True)

        # handle golden extract column labels
        self.golden_extract_projs_start = list(golden_df_extract.columns).index('Feature') + 1
        golden_extract_projs = golden_df_extract.columns[self.golden_extract_projs_start:]

        # Formatting, Replace 'GSC (GSC 3.3)' with 'GSC 3.3'
        ipGenerations = golden_df_extract.loc[0, :][self.golden_extract_projs_start:]
        ipGenerations.replace('(.*)\ \((.*)\)', r'\2', regex=True, inplace=True)

        # Combine proj + ipGeneration as new column labels
        colNames_proj_ipGeneration = ([ '_'.join([proj, ipGeneration]) 
        for proj, ipGeneration in zip(golden_extract_projs, ipGenerations)])

        # Replace columns with new labels
        golden_df_extract.columns = (list(golden_df_extract.columns)
        [:self.golden_extract_projs_start] + sorted(colNames_proj_ipGeneration))

        # Remove row 0
        golden_df_extract = golden_df_extract.drop(labels=[0], axis=0)

        # relabel the index
        golden_df_extract.reset_index(drop=True, inplace=True)

        # clean up column values and then feature names mapping 
        for col in golden_df_extract.columns[:self.golden_extract_projs_start]:
            golden_df_extract[col] = self.feature_names_mapping(self.cleanup(golden_df_extract[col]))

        for col in colNames_proj_ipGeneration:
            golden_df_extract[col] = self.feature_names_mapping(self.cleanup(golden_df_extract[col]))

        # No MultiIndex, sort by values
        golden_df_extract_sorted = (golden_df_extract.sort_values
        (by=list(golden_df_extract.columns)[:self.golden_extract_projs_start]))

        # remove index col
        golden_df_extract_sorted_ri = self.index_1st_col(golden_df_extract_sorted)

        golden_df_extract_sorted_ri.to_excel(self.wr_golden_extract_sorted)
        print(f"Dumping file {self.cwd}/{self.wr_golden_extract_sorted}")
        return golden_df_extract_sorted
    
    def diff(self, df1, df2):
        """
        Compare two spreadsheets and dumps out files
        """
        # diff 1:
        if self.flag == 'diff_gd':
            discrepancy = (
                df1
                .merge(df2, 
                indicator=True, how='outer')
                .loc[lambda v: v['_merge'] != 'both']
                )
            matched = (
                df1
                .merge(df2, 
                indicator=True, 
                how='outer')
                .loc[lambda v: v['_merge'] == 'both']
                )
            # Rename _merge column
            self.rename_merge_col(
                discrepancy, 
                'Match', 
                'golden_only', 
                'database_only'
                )
        elif self.flag == 'diff_dd':
            discrepancy = (
                df1[0]
                .merge(df2[0], 
                indicator=True, how='outer')
                .loc[lambda v: v['_merge'] != 'both']
                )
            matched = (
                df1[0]
                .merge(df2[0],
                indicator=True, 
                how='outer')
                .loc[lambda v: v['_merge'] == 'both']
                )            
            # Rename _merge column
            self.rename_merge_col(
                discrepancy, 
                'Match', 
                'database1_only', 
                'database2_only'
                )

        # Rename _merge column
        self.rename_merge_col(
            matched, 
            'Match', 
            'golden_only', 
            'database_only'
            )
        # sort by values
        discrepancy.sort_values(
            by=discrepancy.columns[self.df_extract_projs_start - 1], 
            inplace=True
        )
        matched.sort_values(
            by=matched.columns[self.df_extract_projs_start - 1],
            inplace=True
        )

        # remove index col
        discrepancy_ri = self.index_1st_col(discrepancy)
        matched_ri = self.index_1st_col(matched)

        discrepancy_ri.to_excel(self.wr_discrepancy)
        print(f"Dumping file {self.cwd}/{self.wr_discrepancy}")
        matched_ri.to_excel(self.wr_matched)
        print(f"Dumping file {self.cwd}/{self.wr_matched}")
        
        # diff 2:
        if self.flag == 'diff_gd':
            diff_golden = (
                pd.merge(
                    df1, 
                    df2, 
                    indicator=True, 
                    how='outer')
                    .loc[lambda v: v['_merge'] == 'left_only']
                )
            diff_database = (
                pd.merge(
                    df1, 
                    df2, 
                    indicator=True, 
                    how='outer')
                    .loc[lambda v: v['_merge'] == 'right_only']
                )            
            # Rename _merge column
            self.rename_merge_col(
                diff_golden, 
                'Match', 
                'golden_only', 
                'database_only'
                )
            self.rename_merge_col(
                diff_database, 
                'Match', 
                'golden_only', 
                'database_only'
                )
            # sort by values
            diff_golden.sort_values(
                by=diff_golden.columns[self.df_extract_projs_start - 1], 
                inplace=True
                )
            diff_database.sort_values(
                by=diff_database.columns[self.df_extract_projs_start - 1], 
                inplace=True
                )         
            # remove index col
            diff_golden_ri = self.index_1st_col(diff_golden)
            diff_database_ri = self.index_1st_col(diff_database)

            diff_golden_ri.to_excel(self.wr_diff_golden)
            print(f"Dumping file {self.cwd}/{self.wr_diff_golden}")
            
            diff_database_ri.to_excel(self.wr_diff_database)
            print(f"Dumping file {self.cwd}/{self.wr_diff_database}")

        elif self.flag == 'diff_dd':
            diff_golden = (
                pd.merge(
                    df1[0], 
                    df2[0], 
                    indicator=True, 
                    how='outer')
                    .loc[lambda v: v['_merge'] == 'left_only']
                )
            diff_database = (
                pd.merge(
                    df1[0], 
                    df2[0], 
                    indicator=True, 
                    how='outer')
                    .loc[lambda v: v['_merge'] == 'right_only']
                )                 
            # Rename _merge column
            self.rename_merge_col(
                diff_golden, 
                'Match', 
                'database1_only', 
                'database2_only'
                )
            self.rename_merge_col(
                diff_database, 
                'Match', 
                'database1_only', 
                'database2_only'
                )

            # sort by values
            diff_golden.sort_values(
                by=diff_golden.columns[self.df_extract_projs_start - 1], 
                inplace=True
                )
            diff_database.sort_values(
                by=diff_database.columns[self.df_extract_projs_start - 1], 
                inplace=True
                )                  
            # remove index col
            diff_golden_ri = self.index_1st_col(diff_golden)
            diff_database_ri = self.index_1st_col(diff_database)

            self.wr_diff_golden = f"{self.output_dir}/output_diffcfg_{df1[1]}.xlsx"
            diff_golden_ri.to_excel(self.wr_diff_golden)
            print(f"Dumping file {self.cwd}/{self.wr_diff_golden}")
            
            self.wr_diff_database = f"{self.output_dir}/output_diffcfg_{df2[1]}.xlsx"
            diff_database_ri.to_excel(self.wr_diff_database)
            print(f"Dumping file {self.cwd}/{self.wr_diff_database}")
        
        # diff 3: compare 'Block' & 'Feature' columns only
        if self.flag == 'diff_gd':
            diffBF_golden = (
                pd.merge(df1.loc[:, self.database_df_extract_BF ], 
                df2.loc[:, self.database_df_extract_BF], 
                indicator=True, 
                how='outer').loc[lambda v: v['_merge'] == 'left_only']
                )
            diffBF_database = (
                pd.merge(df1.loc[:, self.database_df_extract_BF], 
                df2.loc[:, self.database_df_extract_BF], 
                indicator=True, 
                how='outer').loc[lambda v: v['_merge'] == 'right_only']
                )
            diffBF_all = (
                pd.merge(df1.loc[:, self.database_df_extract_BF], 
                df2.loc[:, self.database_df_extract_BF], 
                indicator=True, 
                how='outer').loc[lambda v: v['_merge'] != 'both']
                )
            # Rename _merge column
            self.rename_merge_col(
                diffBF_golden, 
                'Match', 
                'golden_only', 
                'database_only'
                )
            self.rename_merge_col(
                diffBF_database, 
                'Match', 
                'golden_only', 
                'database_only'
                )
            self.rename_merge_col(
                diffBF_all, 
                'Match', 
                'golden_only', 
                'database_only'
                )

            # sort by values
            diffBF_golden.sort_values(
                by=diffBF_golden.columns[self.df_extract_projs_start - 1], 
                inplace=True
            )
            diffBF_database.sort_values(
                by=diffBF_database.columns[self.df_extract_projs_start - 1], 
                inplace=True
            )
            diffBF_all.sort_values(
                by=diffBF_all.columns[self.df_extract_projs_start - 1], 
                inplace=True
            )
            # remove index col
            diffBF_golden_ri = self.index_1st_col(diffBF_golden)
            diffBF_database_ri = self.index_1st_col(diffBF_database)
            diffBF_all_ri = self.index_1st_col(diffBF_all)
            
            diffBF_golden_ri.to_excel(self.wr_diffBF_golden)
            print(f"Dumping file {self.cwd}/{self.wr_diffBF_golden}")

            diffBF_database_ri.to_excel(self.wr_diffBF_database)
            print(f"Dumping file {self.cwd}/{self.wr_diffBF_database}")

            diffBF_all_ri.to_excel(self.wr_diffBF_all)
            print(f"Dumping file {self.cwd}/{self.wr_diffBF_all}")

            self.equal(df1, df2)

        elif self.flag == 'diff_dd':
            diffBF_golden = (
                pd.merge(df1[0].loc[:, self.database_df_extract_BF ], 
                df2[0].loc[:, self.database_df_extract_BF], 
                indicator=True, 
                how='outer').loc[lambda v: v['_merge'] == 'left_only']
                )
            diffBF_database = (
                pd.merge(df1[0].loc[:, self.database_df_extract_BF], 
                df2[0].loc[:, self.database_df_extract_BF], 
                indicator=True, 
                how='outer').loc[lambda v: v['_merge'] == 'right_only']
                )
            diffBF_all = (
                pd.merge(df1[0].loc[:, self.database_df_extract_BF], 
                df2[0].loc[:, self.database_df_extract_BF], 
                indicator=True, 
                how='outer').loc[lambda v: v['_merge'] != 'both']
                )
                
            # Rename _merge column
            self.rename_merge_col(
                diffBF_golden, 
                'Match', 
                'database1_only', 
                'database2_only'
                )
            self.rename_merge_col(
                diffBF_database, 
                'Match', 
                'database1_only', 
                'database2_only'
                )
            self.rename_merge_col(
                diffBF_all, 
                'Match', 
                'database1_only', 
                'database2_only'
                )

            # sort by values
            diffBF_golden.sort_values(
                by=diffBF_golden.columns[self.df_extract_projs_start - 1], 
                inplace=True
            )
            diffBF_database.sort_values(
                by=diffBF_database.columns[self.df_extract_projs_start - 1], 
                inplace=True
            )
            diffBF_all.sort_values(
                by=diffBF_all.columns[self.df_extract_projs_start - 1], 
                inplace=True
            )

            # remove index col
            diffBF_golden_ri = self.index_1st_col(diffBF_golden)
            diffBF_database_ri = self.index_1st_col(diffBF_database)
            diffBF_all_ri = self.index_1st_col(diffBF_all)

            self.wr_diffBF_golden = f"{self.output_dir}/output_diffbf_extra_{df1[1]}.xlsx"
            diffBF_golden_ri.to_excel(self.wr_diffBF_golden)
            print(f"Dumping file {self.cwd}/{self.wr_diffBF_golden}")

            self.wr_diffBF_database = f"{self.output_dir}/output_diffbf_exrtra_{df2[1]}.xlsx"
            diffBF_database_ri.to_excel(self.wr_diffBF_database)
            print(f"Dumping file {self.cwd}/{self.wr_diffBF_database}")

            diffBF_all_ri.to_excel(self.wr_diffBF_all)
            print(f"Dumping file {self.cwd}/{self.wr_diffBF_all}")

            self.equal(df1[0], df2[0])

    
    def equal(self, df1, df2):
        match = f"[Matched] - For details please check {self.cwd}/{self.output_dir}"
        mismatch = f"[Mismatch Found] - For details please check {self.cwd}/{self.output_dir}"
        if df1.equals(df2): print(match)
        else: print(mismatch)


    def format(self, xlsx):
        """
        Formatting xlsx downloaded from databse (archGUI)
        """
        df = pd.read_excel(xlsx)
        df.sort_values(
            by=['Functional Block', 'Feature Name'], 
            inplace=True
        )

        # remove index col
        df_ri = self.index_1st_col(df)
        
        dump_file = f"{self.output_dir}/output_formatted_{xlsx.split('/')[-1]}"
        df_ri.to_excel(dump_file)
        print(f"Dumping file {self.cwd}/{self.output_dir}/{dump_file}")

        return df

    def index_1st_col(self, df):
        """
        Remove the index col. Set the 1st col index.
        """
        df = df.set_index(df.columns[0], inplace=False)
        return df

    def feature_names_mapping(self, x):
        """
        G: 'PRTC NUM OF PRIVATE CHANNELS\nCHANNEL 0 - ESE\nCHANNEL1 - PRTC'         --> R: 'PRTC NUM OF PRIVATE CHANNELS'
        R: 'DOEMAILBOX'                                                             --> G: 'DOE MAILBOX'
        R: 'FTPM INTERFACE ACCESS TYPE (LT ADDRESS)'                                --> G: 'FTPM INTERFACE ACCESS TYPE'
        R: 'HECI (NUM_INSTANCES)'                                                   --> G: 'HECI'
        G: 'IPC * CHANNEL (DEFAULT *) (16 OR 48 BIT ADDRESSING, DEFAULT IS 16-BIT)' --> R: 'IPC * CHANNEL (DEFAULT *)'
        R: 'PTT (FTPM)'                                                             --> G: 'PTT'        
        R: 'ROOT OF ROOTSPACE'                                                      --> G: 'ROOT OF ROOT SPACE' 
        R: 'TBD (RESERVED GPIC (# WIRES'                                            --> G: 'TBD (RESERVED) GPIC (# WIRES)'         
        R: 'DMA-AES_P (INTEGRITY CHECK VALUE) SCHEME'                               --> G: 'DMA-AES_P ICV (INTEGRITY CHECK VALUE) SCHEME'         
        G: 'OCS  SAVE AND RESTORE'                                                  --> R: 'OCS SAVE AND RESTORE'
        G: '16 BIT IOSF SIDEBAND PORT ID SUPPORT\n(CM DEVICE LIST)'                 --> R: '16 BIT IOSF SIDEBAND PORT ID SUPPORT (CM DEVICE LIST)'
        R: 'GSC FLR(DEVICE RESET)'                                                  --> G: 'GSC FLR (DEVICE RESET)'
        R: 'AES BASIC MODES (ECB,CBC,CTR)'                                          --> G: 'AES BASIC MODES (ECB, CBC, CTR)'
        R: 'AES ADVANCED MODES (OFB,CFB)'                                           --> G: 'AES ADVANCED MODES (OFB, CFB)'
        G: 'L1$ PARITY SUPPORT (TAG )'                                              --> 'L1$ PARITY SUPPORT (TAG)'
        R: 'L1$ PARITY SUPPORT(TAG)'                                                --> 'L1$ PARITY SUPPORT (TAG)'
        R: 'L1$ PARITY SUPPORT(DATA)'                                               --> 'L1$ PARITY SUPPORT (DATA)'
        R: 'BUNIT CACHE SIZE (IN KB)'                                               --> G: 'BUNIT CACHE SIZE'
        R: 'DTF(DEBUG TRACE FABRIC)'                                                --> G: 'DTF (DEBUG TRACE FABRIC)
        R: 'ECC GEN1 P256(WITH SCA MITIGATION)'                                     --> G: 'ECC GEN1 P256 (WITH SCA MITIGATION)'
        R: 'ECC GEN1 P384(WITH SCA MITIGATION)'                                     --> G: 'ECC GEN1 P384 (WITH SCA MITIGATION)'
        R: 'ECDSA(FW ASSISTED/HW BUILD-IN)'                                         --> G: 'ECDSA (FW ASSISTED / HW BUILD-IN)'
        R: 'HW EXTEND REGISTER FOR FW MEASUREMENT(SHA-256)'                         --> G: 'HW EXTEND REGISTER FOR FW MEASUREMENT (SHA-256)'
        R: 'IOMMU DMA ACCESS CONTROL (# ENTRIES)'                                   --> G: 'IOMMU DMA ACCESS CONTROL'
        R: 'IOMMU TRANSLATION TABLE (# ENTRY)'                                      --> G: 'IOMMU TRANSLATION TABLE'
        R: 'IOSF-P INTERFACE WIDTH( # IN BITS)'                                     --> G: 'IOSF-P INTERFACE WIDTH'
        R: 'L1$ SIZE (CODE + DATA) (# IN KB)'                                       --> G: 'L1$ SIZE (CODE + DATA)'
        R: 'ROM SIZE (# IN KB)'                                                     --> G: 'ROM SIZE'
        R: 'SM4 BASIC MODES(ECB,CBC,CTR)'                                           --> G: 'SM4 BASIC MODES (ECB, CBC, CTR)'
        R: 'SRAM SIZE (EXCLUDING ECC BITS,  # IN KB)'                               --> G: 'SRAM SIZE (EXCLUDING ECC BITS)'
        """
        return (x.replace(to_replace='(PRTC NUM OF PRIVATE CHANNELS)\n(CHANNEL 0 - ESE)\n(CHANNEL1 - PRTC)',
                value=r'\1', regex=True)                                   
                .replace(to_replace='(DOE)(MAILBOX)',
                value=r'\1 \2', regex=True)
                .replace(to_replace='(FTPM INTERFACE ACCESS TYPE)[ ]*\(LT ADDRESS\)',
                value=r'\1', regex=True)
                .replace(to_replace='HECI[ ]*\(NUM_INSTANCES\)',
                value='HECI', regex=True)
                .replace(to_replace='(IPC \d CHANNEL \(DEFAULT FOR .+\))[ ]*\(16 OR 48 BIT ADDRESSING, DEFAULT IS .+BIT\)',                
                value=r'\1', regex=True)
                .replace(to_replace='(PTT)[ ]*\(FTPM\)',       
                value=r'\1', regex=True)
                .replace(to_replace='(ROOT)[ ]*(OF)[ ]*(ROOT)(SPACE)',
                value=r'\1 \2 \3 \4', regex=True)
                .replace(to_replace='(TBD)[ ]*\((RESERVED)[ ]*(GPIC)[ ]*\([ ]*\#[ ]*(WIRES)',     
                value=r'\1 (\2) \3 (# \4)', regex=True)
                .replace(to_replace='(DMA-AES_P)[ ]*\((INTEGRITY)[ ]*(CHECK)[ ]*(VALUE)[ ]*\)[ ]*(SCHEME)',       
                value=r'\1 ICV (\2 \3 \4) \5', regex=True)
                .replace(to_replace='(OCS)[ ]*(SAVE)[ ]*(AND)[ ]*(RESTORE)',
                value=r'\1 \2 \3 \4', regex=True)
                .replace(to_replace='([ ]*16 BIT IOSF SIDEBAND PORT ID SUPPORT[ ]*)\n\([ ]*(CM DEVICE LIST)[ ]*\)',
                value=r'\1 (\2)', regex=True)
                .replace('(GSC FLR)[ ]*\([ ]*(DEVICE RESET)[ ]*\)', 
                value=r'\1 (\2)', regex=True)
                .replace('(AES BASIC MODES)[ ]*\([ ]*(ECB)[ ]*,[ ]*(CBC)[ ]*,[ ]*(CTR)[ ]*\)',
                value=r'\1 (\2, \3, \4)', regex=True)
                .replace(to_replace='(AES ADVANCED MODES)[ ]*\([ ]*(OFB)[ ]*,[ ]*(CFB)[ ]*\)', 
                value=r'\1 (\2, \3)', regex=True)
                .replace(to_replace='(L1\$ PARITY SUPPORT)[ ]*\([ ]*(\w+)[ ]*\)', 
                value=r'\1 (\2)', regex=True)
                .replace(to_replace='(BUNIT CACHE SIZE)[ ]*\([ ]*IN[ ]*KB[ ]*\)',
                value=r'\1', regex=True)
                .replace(to_replace='(DTF)[ ]*\([ ]*(DEBUG TRACE FABRIC)[ ]*\)',
                value=r'\1 (\2)', regex=True)
                .replace(to_replace='(ECC GEN1 P\d+)[ ]*\([ ]*(WITH SCA MITIGATION)[ ]*\)',
                value=r'\1 (\2)', regex=True)
                .replace(to_replace='(ECDSA)[ ]*\([ ]*(FW)[ ]*(ASSISTED)[ ]*/[ ]*(HW)[ ]*(BUILD-IN)[ ]*\)',                     
                value=r'\1 (\2 \3 / \4 \5)', regex=True)
                .replace(to_replace='(HW EXTEND REGISTER FOR FW MEASUREMENT)[ ]*\([ ]*(SHA-\d+)[ ]*\)',
                value=r'\1 (\2)', regex=True)
                .replace(to_replace='(IOMMU DMA ACCESS CONTROL)[ ]*\([ ]*\#[ ]*ENTRIES[ ]*\)',
                value=r'\1', regex=True)
                .replace(to_replace='(IOMMU TRANSLATION TABLE)[ ]*\([ ]*\#[ ]*ENTRY[ ]*\)',
                value=r'\1', regex=True)
                .replace(to_replace='(IOSF-P INTERFACE WIDTH)[ ]*\([ ]*\#[ ]*IN[ ]*BITS[ ]*\)',
                value=r'\1', regex=True)
                .replace(to_replace='(L1\$ SIZE \(CODE \+ DATA\))[ ]*\([ ]*\#[ ]*IN[ ]*KB[ ]*\)',
                value=r'\1', regex=True)
                .replace(to_replace='(ROM SIZE)[ ]*\([ ]*\#[ ]*IN[ ]*KB[ ]*\)',
                value=r'\1', regex=True)
                .replace(to_replace='(SM4 BASIC MODES)[ ]*\([ ]*(ECB)[ ]*,[ ]*(CBC)[ ]*,[ ]*(CTR)[ ]*\)',
                value=r'\1 (\2, \3, \4)', regex=True)
                .replace(to_replace='(SRAM)[ ]*(SIZE)[ ]*\([ ]*(EXCLUDING)[ ]*(ECC)[ ]*(BITS)[ ]*,[ ]*\#[ ]*IN[ ]*KB[ ]*\)',
                value=r'\1 \2 (\3 \4 \5)', regex=True)
                )         

    def cleanup(self, x):
        """
        Capitalize and strip to clean up the formatting of strings that cause false discrepancy
        """
        return (x.replace(to_replace='(Yes)[ ]*[\n]*[ ]*\([ ]*(x3,100,12.8)[ ]*\)', value=r'\1 (\2)', regex=True)  # For 'Yes \n(x3,100,12.8)'
                .apply(lambda x: x.strip().upper() if isinstance(x, str) else x))
    
    def rename_merge_col(self, df, label, left, right):
        """
        rename _merge col label and values 
        """
        df.rename(
            columns={df.columns[len(df.columns) - 1]: label}, 
            inplace=True)
        df[df.columns[len(df.columns) - 1]] = (
            df[df.columns[len(df.columns) - 1]]
            .replace(to_replace='left_only', value=left)
            .replace(to_replace='right_only', value=right))


def setup_parser(script_name):
    """
    Set up the argument parser
    """
    descript = "Customized for processing 'CSME IE OCS Hardware Architecture Features Per Project.xlsm'"

    parser = aps.ArgumentParser(
        prog=f'./{script_name}.py',
        description=descript
    )
    subparsers = parser.add_subparsers(dest='command')
    subparsers.required = True

    # subparser for diff_gd
    parser_diff_gd = subparsers.add_parser(
        'diff_gd',
        help="Compare two HW arch features config files: 'CSME IE OCS Hardware Architecture Features Per Project.xlsm' VS. HW arch features config from ArchGUI database")
    # add required args
    parser_diff_gd.add_argument(
        '-g',
        '--golden',
        type=str,
        metavar='',
        default='CSME IE OCS Hardware Architecture Features Per Project.xlsm',
        help="'CSME IE OCS Hardware Architecture Features Per Project.xlsm'"
    )
    parser_diff_gd.add_argument(
        '-d',
        '--database',
        type=str,
        metavar='',
        required=True,
        help='HW arch features config file from ArchGUI database'         
    )
    parser_diff_gd.add_argument(
        '-o',
        '--out_dir',
        type=str,
        metavar='',
        default=f'{script_name}_outputs',
        help=f'Output directory, default "{script_name}_outputs"'
    )

    # subparser for diff_dd
    parser_diff_dd = subparsers.add_parser(
        'diff_dd',
        help="Compare two HW arch features config files, both from ArchGUI database")
    # add required args
    parser_diff_dd.add_argument(
        '-f1',
        '--file1',
        type=str,
        metavar='',
        required=True,
        help='HW arch features config file1 from ArchGUI database'
    )
    parser_diff_dd.add_argument(
        '-f2',
        '--file2',
        type=str,
        metavar='',
        required=True,
        help='HW arch features config file2 from ArchGUI database'
    )
    parser_diff_dd.add_argument(
        '-o',
        '--out_dir',
        type=str,
        metavar='',
        default=f'{script_name}_outputs',
        help=f'Output directory, default "{script_name}_outputs"'
    )

    # subparser for format
    parser_format = subparsers.add_parser(
        'format',
        help='Format HW arch features config file from ArchGUI database')
    # add a required arg
    parser_format.add_argument(
        '-f',
        '--file',
        type=str,
        metavar='',
        required=True,
        help='HW arch features config file from ArchGUI database'
    )
    parser_format.add_argument(
        '-o',
        '--out_dir',
        type=str,
        metavar='',
        default=f'{script_name}_outputs',
        help=f'Output directory, default "{script_name}_outputs"'
    )
    return parser


if __name__ == "__main__":
    parser = setup_parser(archqa)
    args = parser.parse_args()
    done = '----- DONE -----'

    def display():
        print()
        for k, v in vars(args).items():
            print(f"{str.upper(k)} : {v}")
        print()
    
    if args.command == 'diff_gd':
        display()
        d = XlsxDiff(args.out_dir, args.command)
        df_db = d.process_database(args.database)
        df_golden = d.process_golden(args.golden)
        d.diff(df_golden, df_db)
        print(done)
    elif args.command == 'diff_dd':
        display()
        d = XlsxDiff(args.out_dir, args.command)
        df_db1 = d.process_database(args.file1)
        df_db2 = d.process_database(args.file2)
        d.diff(df_db1, df_db2)
        print(done)
    elif args.command == 'format':
        display()
        d = XlsxDiff(args.out_dir, args.command)
        d.format(args.file)
        print(done)
        
