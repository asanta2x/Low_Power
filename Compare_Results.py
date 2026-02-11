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
    
    def main(self):
        self.Read_Input_Files()
        self.result_df = (self.df1 - self.df2).abs().round(3)
        self.result_df.insert(0,'Rail Names', self.interested_rails)
        self.result_df.to_csv('DF_Result.csv', index=False)

        return self.result_df
    
    def do_math(self):
        filename1 = self.file_path1.rsplit('Results')[1]
        filename2 = self.file_path2.rsplit('Results')[1]
        path = self.file_path1.rsplit('Results')[0]
        self.Read_Input_Files()
        acc = []
        dic = {}
        regs = []
        dfs = []
        partial = pd.DataFrame()
        partial['Rails'] = self.interested_rails
        for test in self.test_names:
            cola = self.df1[test].reset_index(drop=True).abs().round(3)
            colb = self.df2[test].reset_index(drop=True).abs().round(3)
            delta = cola.sub(colb).abs().round(3)

            partial[test+'-'+filename1] = cola
            partial[test+'-'+filename2] = colb
            partial[test+'-Delta'] = delta
            
        partial.to_excel(f'{path}{filename1}_vs{filename2}{self.time_stamp}.xlsx', index=False)
        print(f'File Created: {path}{filename1}_vs_{filename2}{self.time_stamp}.xlsx')

if __name__ == '__main__':
    print('Testing Comparison script')
    compare = CCompare_Files("C:\Borrar\WW06_28C\Results_Interested_Rails_Summary_26_01_2026_09_30_20_WW04_28C.csv",
                             "C:\Borrar\WW06_28C\Results_Interested_Rails_Summary_10_02_2026_09_49_19_.csv")
    compare.do_math()
