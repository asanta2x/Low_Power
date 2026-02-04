result_hopper_path = 'c:\\_hopper_results\\20260203T193430_CMS-Mode-MCS-State\\'
from Low_Power.PowerRoll_All_SKUs_vAlonso import PowerRoll
from Low_Power.C_Low_Power_Processing_files import Process_Data
power_roll = PowerRoll(result_hopper_path)
power_roll_file_result = power_roll.main()
print(power_roll_file_result)
post_processing = Process_Data(power_roll_file_result[0], power_roll_file_result[1])
post_processing.main()
