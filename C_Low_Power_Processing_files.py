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

class Process_Data:

    def __init__(self, input_file, file_path):
        self.input_file_name = input_file
        self.file_path = file_path
        self.time_stamp = datetime.now().strftime('%d_%m_%Y_%H_%M_%S')
        self.reference_value = ["P_MCP_PCH_TOTAL"] # value to take as a reference
        self.power_rails = ["P_MCP_PCH_TOTAL",'P_PCH_TOTAL','P_MCP_TOTAL']
        self.interested_rails = ['P_VCCORE','P_VCCGT','P_VCCSA','P_VNNAON','P_VCCIO','P_VCC1P8','P_VDD2','P_V3P3A_PCH',
                            'P_VCCPDSW_3P3','P_V1P8A_PCH','P_V1P25','P_V0P85A','P_MCP_TOTAL','P_PCH_POWER','P_MCP_PCH_TOTAL']

        self.test_names = ['CMS-Mode-Short-Idle', 'CMS-Mode-MCS-State', 'CMS-Mode-S5-State', 'CMS-Mode-DeepSx-State', 'S3-Mode-Short-Idle','S3-Mode-Long-Idle','S3-State','S3-Mode-S5-State','S3-Mode-DeepSx-State']
        self.path = 'C:\Borrar'

    def read_csv(self, file):
        print(file)
        df = pd.read_excel(r'{}\{}.xlsx'.format(self.path,file))
        return df

    def process_test_names(self, test_names):
        self.dic_test = {}
        for test_name in test_names:
            #print(test_name)
            temp_test_to_add = []
            mask = self.main_df['Unnamed: 0'].isin(self.reference_value)
            self.df_filtered = self.main_df[mask]

            for test in self.df_filtered.columns:
                if 'Unnamed' in test: pass
                if test_name in test:
                    temp_test_to_add.append([test, 'iteration-{}'.format(test.split('iteration-')[-1].split('\\')[0])])

                self.dic_test[test_name] = temp_test_to_add

        return self.dic_test

    def process_dic_test(self, tests):
        self.column_names = []
        for test in self.dic_test:
            golden_index = 0
            if self.dic_test[test] == []: continue
            iteration_numbers = len(self.dic_test[test])
            if iteration_numbers == 1:
                self.column_names.append(self.df_filtered[self.dic_test[test][0][0]].name)

            else:
                if iteration_numbers%2==0: print(f'Be careful: 2 posible values as median on {test}, total iterations: {iteration_numbers} total iterations')
                temp_list = []
                vals = []
                for i in range(iteration_numbers):
                    temp_list.append([self.dic_test[test][i][-1], float(self.df_filtered[self.dic_test[test][i][0]].values)])
                    vals.append(float(self.df_filtered[self.dic_test[test][i][0]].values))

                vals.sort()
                index_midle_value = len(vals)//2
                midle_value = vals[index_midle_value]

                for i in range(iteration_numbers):
                    if midle_value == float(self.df_filtered[self.dic_test[test][i][0]].values):
                        column_name_midle_value = self.df_filtered[self.dic_test[test][i][0]].name
                        self.column_names.append(column_name_midle_value)
                        break
        return self.column_names

    def create_result_files(self):
        self.main_df.set_index('Unnamed: 0', inplace=True)
        df_full_rails = self.main_df[self.column_names]
        df_full_rails.to_csv(r'{}\\Results_Full_Rails_{}_{}.csv'.format(self.file_path,self.input_file_name, self.time_stamp))
        print('File created: {}\\Results_Full_Rails_{}_{}.csv'.format(self.file_path, self.input_file_name, self.time_stamp))

        df_row_filtered = self.main_df.loc[self.interested_rails]
        df_Copy = df_row_filtered.copy()
        df_result = df_Copy[self.column_names]
        ##df_result.loc['Test'] = test_names
        df_result.to_csv(r'c:\\Borrar\\Results_Interested_Rails_{}_{}.csv'.format(self.input_file_name, self.time_stamp))
        print('File created: c:\\Borrar\\Results_Interested_Rails_{}_{}.csv'.format(self.input_file_name, self.time_stamp))

        newdf = self.main_df.loc[self.power_rails]
        newdf = newdf[self.column_names]
        ##newdf.loc['Test'] = test_names
        newdf.to_csv(r'c:\\Borrar\\Results_Power_Rails_{}_{}.csv'.format(self.input_file_name, self.time_stamp))
        print('File created: c:\\Borrar\\Results_Power_Rails_{}_{}.csv'.format(self.input_file_name, self.time_stamp))

    def main(self):
        print('Main method')
        self.main_df = self.read_csv(self.input_file_name)
        self.process_test_names(self.test_names)
        self.process_dic_test(self.dic_test)
        self.create_result_files()

############################################################################################################################################
if __name__ == '__main__':
    #main()
    data = Process_Data('Summary', 'c:\_hopper_results')
    data.main()
