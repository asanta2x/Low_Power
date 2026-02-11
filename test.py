result_hopper_path = 'C:\\Borrar\\WW06_Rerun_PCH_B0\\'
from Low_Power.PowerRoll_All_SKUs_vAlonso import CPowerRoll
from Low_Power.C_Low_Power_Processing_files import CProcess_Data
from Low_Power.Compare_Results import CCompare_Files

import pandas as pd

PowerRoll = True
PostProcessing = True
Compare = True

""" Power Roll Data from Pooja Script - Summary.xls """
if PowerRoll:
    power_roll = CPowerRoll(result_hopper_path)
    power_roll_file_result = power_roll.main()
    df_power_roll = pd.read_excel(power_roll_file_result)
    #TO DO: return should be only one string

""" Doing post processing data for interested rails """
if PostProcessing:
    post_processing = CProcess_Data(power_roll_file_result)
    post_procesing_name = post_processing.main()
    df_post_p = pd.read_csv(post_procesing_name)

""" Comparison betwen two interested rails files """
if Compare:
    compare = CCompare_Files(post_procesing_name, "C:\Borrar\WW06_28C\Results_Interested_Rails_Summary_26_01_2026_09_30_20_WW04_28C.csv")
    df_comparison = compare.do_math()

""" Creating a single file witj all data """
with pd.ExcelWriter(f"{result_hopper_path}Full_Summary.xlsx", engine="openpyxl") as writer:
    df_power_roll.to_excel(writer, sheet_name="Power_Roll", index=False)
    df_post_p.to_excel(writer, sheet_name="Post_Prosesing", index=False)
    df_comparison.to_excel(writer, sheet_name="WW_Comparison", index=False)

## TO DO: add Q4'25 meas comparison at last script 'compare results' to obtain ratio