result_hopper_path = 'C:\\Borrar\\WW06_Rerun_PCH_B0\\'
from Low_Power.PowerRoll_All_SKUs_vAlonso import CPowerRoll
from Low_Power.C_Low_Power_Processing_files import CProcess_Data
from Low_Power.Compare_Results import CCompare_Files

PowerRoll = True
PostProcessing = True
Compare = True

""" Power Roll Data from Pooja Script - Summary.xls """
if PowerRoll:
    power_roll = CPowerRoll(result_hopper_path)
    power_roll_file_result = power_roll.main()

""" Doing post processing data for interested rails """
if PostProcessing:
    post_processing = CProcess_Data(power_roll_file_result[0], power_roll_file_result[1])
    post_name = post_processing.main()
    print(post_name)

""" Comparison betwen twp interested rails files """
if Compare:
    compare = CCompare_Files("C:\Borrar\WW04_Rerun_PCH_B0\Results_Interested_Rails_Summary_52C_PCH_B0_27_01_2026_11_01_58.csv", post_name)
    compare.do_math()