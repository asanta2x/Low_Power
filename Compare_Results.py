import pandas as pd

from datetime import datetime

class CCompare_Files:

    def __init__(self, file_path1, file_path2):
        self.file_path1 = file_path1
        self.file_path2 = file_path2
        self.time_stamp = datetime.now().strftime('%d_%m_%Y_%H_%M_%S')
        self.interested_rails = ['V_PM_SLP_S0_N','V_PM_SLP_S3_N','V_PM_SLP_S4_N','V_PM_SLP_S5_N','V_CPU_C10_GATE_N','P_VCCGT','P_VCCSA','P_VNNAON','P_VCCIO','P_VCC1P8','P_VDD2','P_V3P3A_PCH',
                            'P_VCCPDSW_3P3','P_V1P8A_PCH','P_V1P25','P_V0P85A','P_VCCCORE','P_MCP_TOTAL','P_PCH_TOTAL','P_MCP_PCH_TOTAL']
        self.test_names = ['CMS-Mode-Short-Idle', 'CMS-Mode-MCS-State', 'CMS-Mode-S5-State', 'CMS-Mode-DeepSx-State', 'S3-Mode-Short-Idle','S3-Mode-Long-Idle','S3-State','S3-Mode-S5-State','S3-Mode-DeepSx-State']

    def read_csv(self, file):
        df = pd.read_csv(r'{}'.format(file), header=None, skiprows=1)
        df = df.iloc[:,1:]        #delete column 0
        df.columns = self.test_names
        return df
    
    def Read_Input_Files(self):
        self.df1 = self.read_csv(self.file_path1)
        self.df2 = self.read_csv(self.file_path2)
     
    def do_math(self):
        filename1 = self.file_path1.rsplit('Results')[1].rsplit('_Interested_Rails_Summary_')[-1]
        filename2 = self.file_path2.rsplit('Results')[1].rsplit('_Interested_Rails_Summary_')[-1]
        path = self.file_path1.rsplit('Results')[0]
        
        self.Read_Input_Files()

        Result_df = pd.DataFrame()
        Result_df['Rails'] = self.interested_rails
        for test in self.test_names:
            col_a = self.df1[test].reset_index(drop=True).abs().round(3)
            col_b = self.df2[test].reset_index(drop=True).abs().round(3)
            delta = col_a.sub(col_b).abs().round(3)

            Result_df[test+'-'+filename1] = col_a
            Result_df[test+'-'+filename2] = col_b
            Result_df[test+'-Delta'] = delta

        result_file_name = f'{path}_Comparison_{filename1}_vs{filename2}.xlsx'

        Result_df.to_excel(result_file_name, sheet_name = 'Comparison',index=False)
        print(f'File Created: {result_file_name}')
        
        return Result_df

if __name__ == '__main__':
    print('Testing Comparison script')
    compare = CCompare_Files("C:\Borrar\WW06_28C\Results_Interested_Rails_Summary_26_01_2026_09_30_20_WW04_28C.csv",
                             "C:\Borrar\WW06_28C\Results_Interested_Rails_Summary_10_02_2026_09_49_19_.csv")
    compare.do_math()
