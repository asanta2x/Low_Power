#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      asanta2x
#
# Created:     03/02/2026
# Copyright:   (c) asanta2x 2026
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import pandas as pd
from datetime import datetime

class CProcess_Data:

    def __init__(self, file_name):
        #file_path, input_file
        path_file_names = file_name.rsplit('\\')
        path = ''
        i = len(path_file_names)
        for t in range(i-1): path += path_file_names[t]+'\\'
        self.input_file_name = file_name.rsplit('\\')[-1]
        self.file_path = path
        self.time_stamp = ''#datetime.now().strftime('%d_%m_%Y_%H_%M_%S')
        self.reference_value = ["P_MCP_PCH_TOTAL"] # value to take as a reference
        self.power_rails = ["P_MCP_PCH_TOTAL",'P_PCH_TOTAL','P_MCP_TOTAL']
        self.interested_rails = ['V_PM_SLP_S0_N','V_PM_SLP_S3_N','V_PM_SLP_S4_N','V_PM_SLP_S5_N','V_CPU_C10_GATE_N','P_VCCGT','P_VCCSA','P_VNNAON','P_VCCIO','P_VCC1P8','P_VDD2','P_V3P3A_PCH',
                            'P_VCCPDSW_3P3','P_V1P8A_PCH','P_V1P25','P_V0P85A','P_VCCCORE','P_MCP_TOTAL','P_PCH_TOTAL','P_MCP_PCH_TOTAL']

        self.test_names = ['CMS-Mode-Short-Idle', 'CMS-Mode-MCS-State', 'CMS-Mode-S5-State', 'CMS-Mode-DeepSx-State', 'S3-Mode-Short-Idle','S3-Mode-Long-Idle','S3-State','S3-Mode-S5-State','S3-Mode-DeepSx-State']

    def read_csv(self, file):
##        print(file)
        df = pd.read_excel(r'{}{}'.format(self.file_path,file))
        return df

    def process_test_names(self, test_names):
        self.dic_test = {}
        for test_name in test_names:
            #print(test_name)
            temp_test_to_add = []
            mask = self.main_df['Unnamed: 0'].isin(self.reference_value)
            self.df_filtered = self.main_df[mask]

            for test in self.df_filtered.columns:
                if 'Unnamed' in test or 'Socwatch' in test: continue
                if test_name in test:
                    temp_test_to_add.append([test, 'iteration-{}'.format(test.split('iteration-')[-1].split('\\')[0])])

                self.dic_test[test_name] = temp_test_to_add

        return self.dic_test

    def process_dic_test(self, tests):
        self.column_names = []
        for test in self.dic_test:
            golden_index = 0
            if self.dic_test[test] == [] or 'Socwatch' in self.dic_test[test]: continue
            iteration_numbers = len(self.dic_test[test])
            if iteration_numbers == 1:
                self.column_names.append(self.df_filtered[self.dic_test[test][0][0]].name)

            else:
                if iteration_numbers%2==0: print(f'Be careful: 2 posible values as median on {test}, total iterations: {iteration_numbers} total iterations')
                temp_list = []
                vals = []
                for i in range(iteration_numbers):
##                    print(self.dic_test[test][i][-1])
##                    print(self.df_filtered[self.dic_test[test][i][0]].values)
                    temp_list.append([self.dic_test[test][i][-1], self.df_filtered[self.dic_test[test][i][0]].values])
                    vals.append(self.df_filtered[self.dic_test[test][i][0]].values)

                vals.sort()
                index_midle_value = len(vals)//2
                midle_value = vals[index_midle_value]

                for i in range(iteration_numbers):
##                    print(midle_value)
##                    print(self.df_filtered[self.dic_test[test][i][0]].values)
                    if midle_value == self.df_filtered[self.dic_test[test][i][0]].values:
                        column_name_midle_value = self.df_filtered[self.dic_test[test][i][0]].name
                        self.column_names.append(column_name_midle_value)
                        break
        return self.column_names

    def create_result_files(self):
        self.main_df.set_index('Unnamed: 0', inplace=True)
        df_full_rails = self.main_df[self.column_names]
        name=self.input_file_name.strip('.xlsx')
        """df_full_rails.to_csv(r'{}\Results_Full_Rails_{}_{}.csv'.format(self.file_path,name , self.time_stamp))
        print('File created: {}\Results_Full_Rails_{}_{}.csv'.format(self.file_path, name , self.time_stamp))"""

        df_row_filtered = self.main_df.loc[self.interested_rails]
        df_Copy = df_row_filtered.copy()
        self.df_result = df_Copy[self.column_names]
        self.df_result.to_csv(r'{}\Results_Interested_Rails_{}_{}.csv'.format(self.file_path,name , self.time_stamp))
        print('File created: {}\Results_Interested_Rails_{}_{}.csv'.format(self.file_path,name , self.time_stamp))

        """self.newdf = self.main_df.loc[self.power_rails]
        self.newdf = self.newdf[self.column_names]
        self.newdf.to_csv(r'{}\Results_Power_Rails_{}_{}.csv'.format(self.file_path,name , self.time_stamp))
        print('File created: {}\Results_Power_Rails_{}_{}.csv'.format(self.file_path,name , self.time_stamp))"""
        self.return_name = f'{self.file_path}\Results_Interested_Rails_{name}_{self.time_stamp}.csv'

    def main(self):
        self.main_df = self.read_csv(self.input_file_name)
        #print(self.test_names)
        self.process_test_names(self.test_names)
        #print(self.dic_test)
        self.process_dic_test(self.dic_test)
        self.create_result_files()
        return self.return_name

############################################################################################################################################
if __name__ == '__main__':
    #main()
    data = CProcess_Data("C:\Borrar\WW06_Rerun_Alonso\Summary_16_02_2026_22_29_03.xlsx")
    data.main()
