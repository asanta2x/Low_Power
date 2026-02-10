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
        self.Read_Input_Files()
        acc = []
        dic = {}
        regs = []
        dfs = []
        for test in self.test_names:
            #print(test)
        #######for i, test in enumerate(self.test_names, start=1):
        #    print(test)
            #resta = pd.DataFrame([self.df1[test], self.df2[test], (self.df1[test]-self.df2[test]).abs().round(3)])
            cola = self.df1[test].reset_index(drop=True).abs().round(3)
            colb = self.df2[test].reset_index(drop=True).abs().round(3)
            delta = cola.sub(colb).abs().round(3)
            partial = pd.DataFrame({'Test:': test,
                                    'Rail': self.interested_rails,
                                    f'{self.file_path1}': cola,
                                    f'{self.file_path2}': colb,
                                    'Delta': delta,
                                    'Wrong %': round(100*(cola-colb)/cola,1).abs()})
            regs.append(partial)
           
        new_df = pd.concat(regs, ignore_index = True)
        new_df.to_csv(f'Comparison_{self.time_stamp}.csv')
        print(f'File Created: Comparison_{self.time_stamp}.csv')

if __name__ == '__main__':
    print('Testing Comparison script')
    compare = CCompare_Files("C:\Borrar\WW04_Rerun_PCH_B0\Results_Interested_Rails_Summary_52C_PCH_B0_27_01_2026_11_01_58.csv",
                             "C:\Borrar\WW06_Rerun_PCH_B0\Results_Interested_Rails_Summary_06_02_2026_14_49_20_.csv")
    compare.do_math()
