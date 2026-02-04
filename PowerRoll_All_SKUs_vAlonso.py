import os
import pandas as pd
import csv
import argparse
import json
import re
import warnings
from datetime import datetime

class PowerRoll:
    def __init__(self, rootdir):
        self.rootdir = rootdir
        self.time_stamp = datetime.now().strftime('%d_%m_%Y_%H_%M_%S')

    def main(self):
        msg         = "Script description"
        ##rootdir     = os.getcwd()
        data        = pd.DataFrame()
        max_index   = 135+253
        delim1      = ""
        delim2      = ","

        #These values may change based on product please update it accordingly
        #There would be one switch case, which can be used to update these before consumption
        pcListMaxLineNum = 9
        maxPCHLine = 255
        pcListRowMatch = ['C-State,', 'CPU/Package_0', 'Residency', '(%),', 'CPU/Package_0', 'Residency', '(msec)']
        s0ixRowMatch = ["SoC", "S0ix", "Substate"]
        dcRowMatch = ["Compute", "Die", "(CDie)", "C-State", "Residency", "Summary:", "Residency", "(Percentage", "and", "Time)"]
        rcMatch = ["Integrated", "Graphics", "C-State", "", "Summary:", "Residency", "(Percentage", "and", "Time)"]
        rcMaxLine = 4
        sagMatch = ["Memory", "Subsystem", "(MEMSS)", "P-State", "Summary", "-", "Sampled:", "Approximated", "Residency", "(Percentage)"]
        pchMatch = ['PCH', 'Active', 'State', 'Summary:', 'Residency', '(Percentage)']
        getIOEPCHData = False
        warnings.filterwarnings("ignore", category=pd.errors.PerformanceWarning)
        removeLatCommaFromColumnName = False
        usePTLDCNames = False
        useNVLSRCNames = False
        dcMaxLine = 8


        mtl_p = ["VLOAD_CORE0",
                 "VLOAD_CORE1",
                 "VLOAD_CORE2",
                 "VLOAD_CORE3",
                 "VLOAD_CORE4",
                 "VLOAD_CORE5",
                 "V_VCCLOAD_ATOM_0",
                 "V_VCCLOAD_ATOM_1",
                 "V_VCCLOAD_LLC",
                 "V_VCC_VCCCORE_SENSE",
                 "V_VCC_GT_SENSE",
                 "V_VCC_VCCSA_SENSE",
                 "V_PM_SLP_S0",
                 "V_CPU_C10_GATE",
                 "P_VCCCORE_SENSE",
                 "P_VCCGT_SENSE",
                 "P_VCCIO",
                 "P_VCCSA",
                 "P_VDD2_CPU",
                 "P_VCC_3P3",
                 "P_VCC_1P5_RTC",
                 "P_VNNAON_QUIET_1",
                 "P_VNNAON_QUIET_2",
                 "P_VNNAON",
                 "P_VCC1P8_QUIET_1",
                 "P_VCC1P8_QUIET_2",
                 "P_VCC1P8",
                 "P_MCP_TOTAL"]

        mtl_m = ["V_VCCLOAD_CORE_0",
                 "V_VCCLOAD_CORE_1",
                 "V_VCCLOAD_ATOM_0",
                 "V_VCCLOAD_ATOM_1",
                 "V_VCCLOAD_LLC_VAL",
                 "V_VCC_VCCCORE_SENSE",
                 "V_VCC_GT_SENSE",
                 "V_VCC_SA_SENSE",
                 "V_PM_SLP_S0",
                 "V_CPU_C10_GATE",
                 "P_VCCCORE_SENSE",
                 "P_VCCGT_SENSE",
                 "P_VCCIO",
                 "P_VCCSA",
                 "P_VDD2_CPU",
                 "P_VCC_3P3",
                 "P_VCC_1P5_RTC",
                 "P_VNNAON_QUIET_1",
                 "P_VNNAON_QUIET_2",
                 "P_VNNAON",
                 "P_VCC1P8_QUIET_1",
                 "P_VCC1P8_QUIET_2",
                 "P_VCC1P8",
                 "P_MCP_TOTAL"]

        arl_h = ["V_VLOAD_CORE0",
                 "V_VLOAD_CORE1",
                 "V_VLOAD_CORE2",
                 "V_VLOAD_CORE3",
                 "V_VLOAD_CORE4",
                 "V_VLOAD_CORE5",
                 "V_VCCLOAD_ATOM_0",
                 "V_VCCLOAD_ATOM_1",
                 "V_VCCLOAD_LLC",
                 "V_VCC_VCCCORE_SENSE",
                 "V_VCC_VCCSA_SENSE",
                 "V_VCC_GT_SENSE",
                 "V_PM_SLP_S0",
                 "V_CPU_C10_GATE",
                 "P_VCCCORE_SENSE",
                 "P_VCCGT_SENSE",
                 "P_VCCIO",
                 "P_VCCSA",
                 "P_VDD2_CPU",
                 "P_VCC_3P3",
                 "P_VCC_1P5_RTC",
                 "P_VNNAON_QUIET_1",
                 "P_VNNAON_QUIET_2",
                 "P_VNNAON",
                 "P_VCC1P8_QUIET_1",
                 "P_VCC1P8_QUIET_2",
                 "P_VCC1P8",
                 "P_MCP_TOTAL"]

        arl_u = ["VLOAD_CORE0",
                 "VLOAD_CORE1",
                 "V_VCCLOAD_ATOM_0",
                 "V_VCCLOAD_ATOM_1",
                 "V_VCCLOAD_LLC",
                 "V_VCC_VCCCORE_SENSE",
                 "V_VCC_VCCSA_SENSE",
                 "V_VCC_GT_SENSE",
                 "V_PM_SLP_S0",
                 "V_CPU_C10_GATE",
                 "P_VCCCORE_SENSE",
                 "P_VCCGT_SENSE",
                 "P_VCCIO",
                 "P_VCCSA",
                 "P_VDD2_CPU",
                 "P_VCC_3P3",
                 "P_VCC_1P5_RTC",
                 "P_VNNAON_QUIET_1",
                 "P_VNNAON_QUIET_2",
                 "P_VNNAON",
                 "P_VCC1P8_QUIET_1",
                 "P_VCC1P8_QUIET_2",
                 "P_VCC1P8",
                 "P_MCP_TOTAL"]

        arl_s = ["P_MCP_PCH_POWER",
                 "P_MCP_POWER",
                 "P_PCH_POWER",
                 "P_VAL_V0P82A",
                 "P_VAL_V1P8A",
                 "P_VAL_V1P8A_PCH",
                 "P_VAL_V3P3_DUAL",
                 "P_VAL_V3P3A_PCH",
                 "P_VAL_VCCA_CNV_0P82",
                 "P_VAL_VCCA_CNVI_PLL_1P8",
                 "P_VAL_VCCA_MPHYPLL_1P8",
                 "P_VAL_VCCA_REF_CLKPLL_1P8",
                 "P_VAL_VCCA_REFPLL_0P82",
                 "P_VAL_VCCA_SRC_GEN_DIG_XTAL_0P82",
                 "P_VAL_VCCA_XTAL_1P8",
                 "P_VAL_VCCDUSB_0P82",
                 "P_VAL_VCCFUSE_0P82",
                 "P_VAL_VCCMPHY_0P82",
                 "P_VAL_VCCPDSW_3P3",
                 "P_VAL_VCCPFUSE_1P8",
                 "P_VAL_VCCPGPPA_1P8",
                 "P_VAL_VCCPGPPBC_3P3_1P8",
                 "P_VAL_VCCPGPPDR_3P3_1P8",
                 "P_VAL_VCCPGPPEFHK_3P3_1P8",
                 "P_VAL_VCCPGPPI_3P3_1P8",
                 "P_VAL_VCCPRIM_1P8",
                 "P_VAL_VCCPRIM_1P25",
                 "P_VAL_VCCPRIM_DSW_0P82",
                 "P_VAL_VCCPRIMCORE_0P82",
                 "P_VAL_VCCPSPI_3P3_1P8",
                 "P_VAL_VCCPUSB_1P8",
                 "P_VAL_VCCPUSB_3P3",
                 "P_VCC1P8",
                 "P_VCCCORE_PHASE_TOTAL",
                 "P_VCCCORE_POWER",
                 "P_VCCGT",
                 "P_VCCIO",
                 "P_VCCPRTC_3P3",
                 "P_VCCSA",
                 "P_VDD2",
                 "P_VNNAON",
                 "V_PM_SLP_S0_N",
                 "V_PM_SLP_S3_N",
                 "V_PM_SLP_S4_N",
                 "V_PM_SLP_S5_N",]

        lnl_m = ["P_Total_LNL_Power",
                 "P_COMPUTE_SOC_TOTAL",
                 "P_PCD_M_TOTAL",
                 "P_V1P8_MEM",
                 "P_V1P8A_ROP",
                 "P_VCC1P5_RTC",
                 "P_VCC_3P3",
                 "P_VCCAtom",
                 "P_VCCDDRIO",
                 "P_VCCGT",
                 "P_VCCIA",
                 "P_VCCIO",
                 "P_VCCIO_ONLY",
                 "P_VCCIO_TERM_V1P25",
                 "P_VCCL2",
                 "P_VCCPRIM_1P8",
                 "P_VCCPRIM_1P8_FILTRA_IN",
                 "P_VCCPRIM_1P8_FILTRB_IN",
                 "P_VCCPRIM_1P8_ONLY",
                 "P_VCCPRIM_VNNAON",
                 "P_VCCPRIM_VNNAON_FLTR_R",
                 "P_VCCSA",
                 "P_VCCST",
                 "P_VDD2H",
                 "P_VDD2L",
                 "P_VDDQ",
                 "P_VNNAON_ONLY",
                 "P_VNNAONLV",
                 "V_PM_SLP_S0_N",
                 "V_VCC_ECORE_SENSE",
                 "V_VCCIO_SENSE",
                 "V_VNNAON_SENSE",
                 "V_VNNAONLV_SENSE"]

        ptl_p = ["P_PTL_Total_Power",
                 "P_COMPUTE_SOC_TOTAL",
                 "P_PCD_P_TOTAL",
                 "P_VCC_1P8",
                 "P_VCC_LP_ECORE",
                 "P_VCC_RTC",
                 "P_VCCIO_ONLY",
                 "P_VCCIO_TERM_V1P25",
                 "P_VCCPRIM_1P8",
                 "P_VCCPRIM_1P8_FLTRA",
                 "P_VCCPRIM_1P8_FLTRB",
                 "P_VCCPRIM_1P8_ONLY",
                 "P_VCCPRIM_3P3",
                 "P_VCCPRIM_IO",
                 "P_VCCPRIM_IO_FLTR",
                 "P_VCCPRIM_IO_ONLY",
                 "P_VCCPRIM_VNNAON",
                 "P_VCCPRIM_VNNAON_FLTR",
                 "P_VCCSA",
                 "P_VCCST",
                 "P_VDD2_CPU",
                 "P_VDDQ_CPU",
                 "P_VNNAON_noVCCST",
                 "P_VNNAON_ONLY",
                 "V_SLP_S0",
                 "V_VCC_LP_ECORE_SENSE",
                 "V_VCCCORE_SENSE",
                 "V_VCCGT_SENSE",
                 "V_VCCSA_SENSE"]


        nvl_s = ['P_VCCGT',
                'P_VCC1P8',
                'P_VDD2',
                'P_VCCIO',
                'P_VNNAON',
                'P_VCCCORE_PH1',
                'P_VCCCORE_PH2',
                'P_VCCCORE_PH3',
                'P_VCCCORE_PH4',
                'P_VCCCORE_PH5',
                'P_VCCCORE_PH6',
                'P_VCCCORE_PH7',
                'P_VCCCORE_PH8',
                'P_VCCCORE_PH9',
                'P_VCCSA_PH1',
                'P_VCCSA_PH2',
                'P_V5DUAL_DDR5',
                'P_V3P3A_PCH',
                'P_VCCPDSW_3P3',
                'P_VCCDUSB_3P3',
                'P_VCCPRTC_3P3',
                'P_V1P25',
                'P_VCCA_PLL_1P25',
                'P_VCCPRIM_1P05_1P25',
                'P_V1P8A_PCH',
                'P_VCCPRIM_1P8',
                'P_VCCPUSB_1P8',
                'P_VCCPFUSE_1P8',
                'P_VCCA_MPHYPLL_1P8',
                'P_VCCA_REF_PLL_1P8',
                'P_VCCA_XTAL_1P8',
                'P_VCCA_CNVI_PLL_1P8',
                'P_V0P85A',
                'P_V3P3S_PEG_SLOT_1',
                'P_VCCA_XTAL_0P85',
                'P_VCCPRIM_1P25',
                'P_V3P3S_PCIE_SLOT2',
                'P_V3P3S_PCIE_SLOT3',
                'P_V3P3A_PCIEAUX',
                'P_VCCPSPI_3P3_1P8',
                'P_VCCPGPPA_1P8',
                'P_VCCPGPPBC_3P3_1P8',
                'P_VCCPGPPDR_3P3_1P8',
                'P_VCCPGPPEFHK_3P3_1P8',
                'P_VCCPGPPI_3P3_1P8',
                'P_VCCMPHY_0P85',
                'P_VCCPRIMCORE_0P85',
                'P_VCCCORE',
                'P_VCCSA',
                'P_MCP_TOTAL',
                'P_PCH_TOTAL',
                'P_MCP_PCH_TOTAL',]

        soc_index = ["PC0",
                     "PC2",
                     "PC3",
                     "PC6",
                     "PC7",
                     "PC8",
                     "PC9",
                     "PC10",
                     "S0i2.0",
                     "S0i2.1",
                     "S0i2.2",
                     "Overall Platform Activity",
                     "Process1",
                     "Process2",
                     "Process3",
                     "Process4",
                     "Process5",
                     "SAGV0",
                     "SAGV1",
                     "SAGV2",
                     "SAGV3",
                     "DC0",
                     "DC2.1",
                     "DC2.2",
                     "DC3.1",
                     "DC3.2",
                     "DC6",
                     "ACPI C0",
                     "ACPI C1",
                     "ACPI C2",
                     "ACPI C3",
                     "RC0",
                     "RC6"]

        browser_efficiency_index = ["amazonscroll",
                                    "facebooknewsfeedscroll",
                                    "googleimages",
                                    "googlesearch",
                                    "bbcnews",
                                    "cnnhomepage",
                                    "espnhomepage",
                                    "reddithome",
                                    "wikipediaunitedstates",
                                    "twitterpublic",
                                    "outlookoffice_catapult_v2",
                                    "amazonsearch_catapult_v2",
                                    "googleimages_catapult_v2",
                                    "instagram_catapult_v2",
                                    "linkedinjobs",
                                    "linkedinfeedscroll",
                                    "nytimes",
                                    "giphy",
                                    "twitchtv"
                                    ]


        data_list = ["PC0",
                     "PC2",
                     "PC3",
                     "PC6",
                     "PC7",
                     "PC8",
                     "PC9",
                     "PC10",
                     "s0i2.0,",
                     "s0i2.1,",
                     "s0i2.2,",
                     "Overall",
                     "1",
                     "2",
                     "3",
                     "4",
                     "5",
                     "SAGV0",
                     "SAGV1",
                     "SAGV2",
                     "SAGV3",
                     "DC0",
                     "DC2.1,",
                     "DC2.2,",
                     "DC3.1,",
                     "DC3.2,",
                     "DC6",
                     "C0,",
                     "C1,",
                     "C2,",
                     "C3,",
                     "RC0",
                     "RC6",
                     "amazonscroll",
                     "facebooknewsfeedscroll",
                     "googleimages",
                     "googlesearch",
                     "bbcnews",
                     "cnnhomepage",
                     "espnhomepage",
                     "reddithome",
                     "wikipediaunitedstates",
                     "twitterpublic",
                     "outlookoffice_catapult_v2",
                     "amazonsearch_catapult_v2",
                     "googleimages_catapult_v2",
                     "instagram_catapult_v2",
                     "linkedinjobs",
                     "linkedinfeedscroll",
                     "nytimes",
                     "giphy",
                     "twitchtv"]
        #would be appened to soc_index on runtime
        #would be read from the file
        pch_index = []
        appendPCH = True
        ioe_pch_index = []
        appendIOEPCH = True
        # Initialize parser
        parser= argparse.ArgumentParser(description = msg)

        # Adding optional arguments
        parser.add_argument("-s",
                            "--sku",
                            help = "Si SKU the data was collected on.",
                            type = str,
                            default = 'nvl-s',
                            choices = ["mtl-p",
                                       "mtl-m",
                                       "arl-h",
                                       "arl-u",
                                       "arl-s",
                                       "lnl-m",
                                       "ptl-p",
                                       "nvl-s"])

        parser.add_argument("-c",
                            "--console",
                            help = "Prints summary Focus Rails to the console.",
                            default = False,
                            action = "store_true")

        # Read arguments from command line
        args = parser.parse_args()
        if args.sku == "lnl-m" or "ptl-p" or "nvl-s":
            pcListMaxLineNum = 8
            pcListRowMatch = ['C-State,', 'Package', 'Residency', '(%),', 'Package', 'Residency', '(msec)']
            s0ixRowMatch = ['S0ix', 'Substate']
            soc_index = ["PC0",
                     "PC2",
                     "PC6.1",
                     "PC6.2",
                     "PC10.1",
                     "PC10.2",
                     "PC10.3",
                     "S0i2.0",
                     "S0i2.1",
                     "S0i2.2",
                     "Overall Platform Activity",
                     "Process1",
                     "Process2",
                     "Process3",
                     "Process4",
                     "Process5",
                     "SAGV0",
                     "SAGV1",
                     "SAGV2",
                     "SAGV3",
                     "DC0",
                     "DC2.1",
                     "DC2.2",
                     "DC3.1",
                     "DC3.2",
                     "DC6",
                     "ACPI C0",
                     "ACPI C1",
                     "ACPI C2",
                     "ACPI C3",
                     "RC0",
                     "RC6"]

            data_list = ["PC0",
                     "PC2",
                     "PC6.1",
                     "PC6.2",
                     "PC10.1",
                     "PC10.2",
                     "PC10.3",
                     "s0i2.0",
                     "s0i2.1",
                     "s0i2.2",
                     "Overall",
                     "1",
                     "2",
                     "3",
                     "4",
                     "5",
                     "SAGV0",
                     "SAGV1",
                     "SAGV2",
                     "SAGV3",
                     "DC0",
                     "DC2.1,",
                     "DC2.2,",
                     "DC3.1,",
                     "DC3.2,",
                     "DC6",
                     "C0",
                     "C1",
                     "C2",
                     "C3",
                     "RC0",
                     "RC6",
                     "amazonscroll",
                     "facebooknewsfeedscroll",
                     "googleimages",
                     "googlesearch",
                     "bbcnews",
                     "cnnhomepage",
                     "espnhomepage",
                     "reddithome",
                     "wikipediaunitedstates",
                     "twitterpublic",
                     "outlookoffice_catapult_v2",
                     "amazonsearch_catapult_v2",
                     "googleimages_catapult_v2",
                     "instagram_catapult_v2",
                     "linkedinjobs",
                     "linkedinfeedscroll",
                     "nytimes",
                     "giphy",
                     "twitchtv"]

            removeLatCommaFromColumnName = True
            if args.sku == "ptl-p":
                pchMatch = ['PCD', 'Active', 'State', 'Summary:', 'Residency', '(Percentage)']
                maxPCHLine = 309
                dcMaxLine = 7
            elif args.sku == "nvl-s":
                dcMaxLine = 7
                rcMatch = ["Platform", "Monitoring", "Technology", "Integrated", "Graphics", "C-State", "Residency", "Summary:", "Residency", "(Percentage", "and", "Time)"]
                rcMaxLine = 3
                usePTLDCNames = True
                useNVLSRCNames = True

                soc_index = ["PC0",
                     "PC2",
                     "PC6.1",
                     "PC6.2",
                     "PC10.1",
                     "PC10.2",
                     "PC10.3",
                     "S0i2.0",
                     "S0i2.1",
                     "S0i2.2",
                     "Overall Platform Activity",
                     "Process1",
                     "Process2",
                     "Process3",
                     "Process4",
                     "Process5",
                     "SAGV0",
                     "SAGV1",
                     "SAGV2",
                     "SAGV3",
                     "DC0",
                     "DC1",
                     "DC2",
                     "DC3",
                     "DC6",
                     "ACPI C0",
                     "ACPI C1",
                     "ACPI C2",
                     "ACPI C3",
                     "RC6"]

                data_list = ["PC0",
                     "PC2",
                     "PC6.1",
                     "PC6.2",
                     "PC10.1",
                     "PC10.2",
                     "PC10.3",
                     "s0i2.0",
                     "s0i2.1",
                     "s0i2.2",
                     "Overall",
                     "1",
                     "2",
                     "3",
                     "4",
                     "5",
                     "SAGV0",
                     "SAGV1",
                     "SAGV2",
                     "SAGV3",
                     "DC0",
                     "DC1",
                     "DC2",
                     "DC3",
                     "DC6",
                     "C0",
                     "C1",
                     "C2",
                     "C3",
                     "RC6",
                     "amazonscroll",
                     "facebooknewsfeedscroll",
                     "googleimages",
                     "googlesearch",
                     "bbcnews",
                     "cnnhomepage",
                     "espnhomepage",
                     "reddithome",
                     "wikipediaunitedstates",
                     "twitterpublic",
                     "outlookoffice_catapult_v2",
                     "amazonsearch_catapult_v2",
                     "googleimages_catapult_v2",
                     "instagram_catapult_v2",
                     "linkedinjobs",
                     "linkedinfeedscroll",
                     "nytimes",
                     "giphy",
                     "twitchtv"]

                pchMatch = ['SoC', 'PCH', 'Active', 'State', 'Summary:', 'Residency', '(Percentage)']
        elif args.sku == "arl-h":
            pchMatch = ['SoC', 'PCH', 'Active', 'State', 'Summary:', 'Residency', '(Percentage)']
            maxPCHLine = 223
        elif args.sku == "arl-s":
            pchMatch = ['SoC', 'PCH', 'Active', 'State', 'Summary:', 'Residency', '(Percentage)']
            maxPCHLine = 153
            ioepchMatch = ['IOE', 'PCH', 'Active', 'State', 'Summary:', 'Residency', '(Percentage)']
            maxIOEPCHLine = 144
            getIOEPCHData = True

        # Initializes a data frame for everything but Flex logger data
        def data_frame():

            data_frame = pd.DataFrame([0] * len(data_list))
            data_frame.index = data_list
            data_frame = data_frame.T
            return data_frame

        # Package C-State Summary Data Frame
        def pc_df(soc_row_list):

            pc_frame    = pd.DataFrame()
            line_num    = 0
            pc_list     = [["PC0",  "0"],
                           ["PC2",  "0"],
                           ["PC3",  "0"],
                           ["PC6",  "0"],
                           ["PC7",  "0"],
                           ["PC8",  "0"],
                           ["PC9",  "0"],
                           ["PC10", "0"]]

            for row in soc_row_list:
                line_num += 1
                if (len(row) >= len(pcListRowMatch)):
                    if row[0:len(pcListRowMatch)] == pcListRowMatch:
                        pc_list = []
                        for i in soc_row_list[line_num + 1 : line_num + pcListMaxLineNum]:
                            pc_list.append([i for i in i if i != delim1 and i != delim2])
                        break

            for i in range(len(pc_list)):
                pc_frame[pc_list[i][0]] = [pc_list[i][1]]
            return pc_frame

        # S0iX Data Frame
        def s0ix_df(soc_row_list):

            s0ix_frame  = pd.DataFrame()
            line_num    = 0
            s0ix_list   = [["s0i2.0,", "0"],
                           ["s0i2.1,", "0"],
                           ["s0i2.2,", "0"]]

            if usePTLDCNames:
                s0ix_list = [["s0i2.0", "0"],
                           ["s0i2.1", "0"],
                           ["s0i2.2", "0"]]

            for row in soc_row_list:
                line_num += 1
                if len(row) >= len(s0ixRowMatch):
                    if row[0:len(s0ixRowMatch)] == s0ixRowMatch:
                        s0ix_list = []

                        for i in soc_row_list[line_num + 5 : line_num + 8]:
                            s0ix_list.append([i for i in i if i != delim1 and i != delim2])
                            if removeLatCommaFromColumnName:
                                if len(s0ix_list[-1]) > 0:
                                    if s0ix_list[-1][0][-1] == ',':
                                        s0ix_list[-1][0] = s0ix_list[-1][0][0:-1]
                        break

            for i in range(len(s0ix_list)):
                s0ix_frame[s0ix_list[i][0]] = [s0ix_list[i][1]]

            return s0ix_frame

        # Processes by Platform Busy Duration Data Frame
        def proc_df(soc_row_list):

            proc_frame  = pd.DataFrame()
            line_num    = 0
            proc_list   = [["0", "0", "0", "0"],
                           ["1", "0", "0", "0"],
                           ["2", "0", "0", "0"],
                           ["3", "0", "0", "0"],
                           ["4", "0", "0", "0"],
                           ["5", "0", "0", "0"]]

            for row in soc_row_list:
                line_num += 1
                if len(row) > 1 and row[0] == 'Rank,':
                    proc_list = []

                    for i in soc_row_list[line_num + 1 : line_num + 7]:
                        proc_list.append([i for i in i if i != delim1 and i != delim2])
                        if removeLatCommaFromColumnName:
                            if proc_list[-1][0][-1] == ",":
                                proc_list[-1][0] = proc_list[-1][0][0:-1]
                    break

            for i in range(len(proc_list)):
                proc_frame[proc_list[i][0]] = [proc_list[i][3]]

            return proc_frame

        # Memory Subsystem (MEMSS) P-State Summary (Percentage)
        def sagv_df(soc_row_list):

            line_num    = 0
            gv_points   = 0
            sagv_frame  = pd.DataFrame()
            sagv_list   = [["SAGV0", "0"],
                           ["SAGV1", "0"],
                           ["SAGV2", "0"],
                           ["SAGV3", "0"]]

            for row in soc_row_list:
                line_num += 1
                if (len(row) >= len(sagMatch)):
                    if row[0:len(sagMatch)] == sagMatch:
                        sagv_list = []

                        for i in soc_row_list[line_num + 2 : line_num + 6]:
                            if len(i) != 0:

                                sagv_list.append([i for i in i if i != delim1 and i != delim2])
                                sagv_list[gv_points][0] = "SAGV" + str(gv_points)
                                gv_points += 1
                            else:
                                break

                        for i in range(gv_points):
                            sagv_frame[sagv_list[i][0]] = [sagv_list[i][1]]

                        missing_gv_points = 4 - gv_points

                        for point in range(missing_gv_points):

                            sagv_list.append(["SAGV" + str(gv_points + point), "0"])
                            sagv_frame[sagv_list[gv_points + point][0]] = [sagv_list[gv_points + point][1]]
                        break
                else:
                    for i in range(len(sagv_list)):
                        sagv_frame[sagv_list[i][0]] = [sagv_list[i][1]]

            return sagv_frame

        # Compute Die (CDie) C-State Residency Summary data frame
        def dc_df(soc_row_list):

            line_num    = 0
            dc_frame    = pd.DataFrame()
            dc_list     = [["DC0",      "0"],
                           ["DC2.1,",   "0"],
                           ["DC2.2,",   "0"],
                           ["DC3.1,",   "0"],
                           ["DC3.2,",   "0"],
                           ["DC6",      "0"]]

            if usePTLDCNames:
                dc_list = [["DC0",   "0"],
                           ["DC1",   "0"],
                           ["DC2",   "0"],
                           ["DC3",   "0"],
                           ["DC6",   "0"]]
            for row in soc_row_list:
                line_num += 1
                if len(row) >=  len(dcRowMatch):
                    if (row[0:len(dcRowMatch)] == dcRowMatch):
                        dc_list = []
                        for i in soc_row_list[line_num + 2 : (line_num + dcMaxLine)]:
                            dc_list.append([i for i in i if i != delim1 and i != delim2])
                        break
            for i in range((dcMaxLine-2)):
                # print(dc_list)
                dc_frame[dc_list[i][0]] = [dc_list[i][1]]

            return dc_frame

        # Package C-State (OS) Summary data frame
        def acpi_df(soc_row_list):

            line_num    = 0
            acpi_frame  = pd.DataFrame()
            acpi_list   = [["C0", "0"],
                           ["C1", "0"],
                           ["C2", "0"],
                           ["C3", "0"]]

            for row in soc_row_list:
                line_num += 1
                #if row == ["Package", "C-State", "(OS)", "Summary:", "Residency", "(Percentage", "and", "Time)"]:
                if (len(row) >= 8):
                    if row[0] == "Package" and row[1] == "C-State" and row[2] == "(OS)" and row[3] == "Summary:" and row[4] == "Residency" and row[5] == "(Percentage" and row[6] == "and" and row[7] == "Time)":
                        acpi_list = []
                        for i in soc_row_list[line_num + 2 : line_num + 6]:
                            acpi_list.append([i for i in i if i != delim1 and i != delim2])
                            if removeLatCommaFromColumnName:
                                if (acpi_list[-1][1][-1] == ","):
                                    acpi_list[-1][1] = acpi_list[-1][1][0:-1]
                        break
            for i in range(4):
                acpi_frame[acpi_list[i][1]] = [acpi_list[i][2]]

            return acpi_frame

        # Integrated Graphics C-State Summary data frame
        def rc_df(soc_row_list):

            line_num    = 0
            rc_frame    = pd.DataFrame()
            rc_list     = [["RC0", "0"],
                           ["RC6", "0"]]

            if useNVLSRCNames:
                rc_list = [["RC6", "0"]]
            for row in soc_row_list:
                line_num += 1
                if (len(row) >= len(rcMatch)):
                    if row[0:len(rcMatch)] == rcMatch:
                        rc_list = []

                        for i in soc_row_list[line_num + 2 : line_num + rcMaxLine]:
                            rc_list.append([i for i in i if i != delim1 and i != delim2])
                        break

            for i in range((rcMaxLine-2)):
                rc_frame[rc_list[i][0]] = [rc_list[i][1]]

            return rc_frame

        def is_numerical_string(value):
            try:
                float(value)  # Attempt to convert the string to a float
                return True
            except ValueError:
                return False

        def pch_df(soc_row_list):
            global appendPCH
            line_num    = 0
            pch_frame    = pd.DataFrame()

            for row in soc_row_list:
                line_num += 1
                # if (len(row) > 0):
                    # if row[0] == 'PCD':
                        # print("Trying", row)
                        # print("Needs", pchMatch)
                #['PCD', 'Active', 'State', 'Summary:', 'Residency', '(Percentage)']
                if (len(row) >= len(pchMatch)):
                    if row[0:len(pchMatch)] == pchMatch:
                        pch_list = []

                        for i in soc_row_list[line_num + 2 : line_num + maxPCHLine]:
                            pch_list.append([i for i in i if i != delim1 and i != delim2])
                        for pch in pch_list:
                            tempPCHIDX = 0
                            for val in pch:

                                if is_numerical_string(val):
                                    if is_numerical_string(pch[tempPCHIDX + 1]):
                                        tempVal = val
                                        pch_frame[pch[0]] = [tempVal]
                                        if appendPCH:
                                            pch_index.append(pch[0])
                                        break
                                tempPCHIDX = tempPCHIDX + 1

                        appendPCH = False
                        break

            return pch_frame

        def ioe_pch_df(soc_row_list):
            global appendIOEPCH
            line_num    = 0
            ioe_pch_frame    = pd.DataFrame()
            if (not getIOEPCHData):
                return ioe_pch_frame
            for row in soc_row_list:
                line_num += 1
                if (len(row) >= len(ioepchMatch)):
                    if row[0:len(ioepchMatch)] == ioepchMatch:
                        ioe_pch_list = []

                        for i in soc_row_list[line_num + 2 : line_num + maxIOEPCHLine]:
                            ioe_pch_list.append([i for i in i if i != delim1 and i != delim2])
                        for ioe_pch in ioe_pch_list:
                            tempIOEPCHIDX = 0
                            for val in ioe_pch:

                                if is_numerical_string(val):
                                    if is_numerical_string(ioe_pch[tempIOEPCHIDX + 1]):
                                        tempVal = val
                                        ioe_pch_name = "IOE_"
                                        ioe_pch_name += ioe_pch[0]
                                        ioe_pch_frame[ioe_pch_name] = [tempVal]
                                        if appendIOEPCH:
                                            ioe_pch_index.append(ioe_pch_name)
                                        break
                                tempIOEPCHIDX = tempIOEPCHIDX + 1

                        appendIOEPCH = False
                        break

            return ioe_pch_frame

        # Parses SoCwatch log file
        def soc_parse(useCommaAsWell = False):

            soc_list = []
            with open(filepath, newline = '', encoding='utf-8') as csvfile:
                spamreader = csv.reader(csvfile, delimiter = ' ', quotechar = '|')

                for row in spamreader:
                    if useCommaAsWell:
                        if (len(row) > 0):
                            commConcatElement = row.pop()
                            actualValuesToStore = commConcatElement.split(",")
                            for val in actualValuesToStore:
                                row.append(val)
                    soc_list.append(row)

            return soc_list

        # SoCwatch Data Frame
        def socwatch_frame(data_frame):
            if args.sku in ["lnl-m", "ptl-p", "nvl-s"]:
                soc_list = soc_parse(True)
            else:
                soc_list = soc_parse()
            pc_frame    = pc_df(soc_list)
            s0ix_frame  = s0ix_df(soc_list)
            proc_frame  = proc_df(soc_list)
            sagv_frame  = sagv_df(soc_list)
            dc_frame    = dc_df(soc_list)
            acpi_frame  = acpi_df(soc_list)
            rc_frame    = rc_df(soc_list)
            pch_frame    = pch_df(soc_list)
            ioe_pch_frame    = ioe_pch_df(soc_list)

            soc_frame   = pd.concat([pc_frame,
                                     s0ix_frame,
                                     proc_frame,
                                     sagv_frame,
                                     dc_frame,
                                     acpi_frame,
                                     rc_frame,
                                     pch_frame,
                                     ioe_pch_frame],
                                     axis = 1)
            data_frame  = pd.concat([data_frame, soc_frame], axis = 0)
            return data_frame

        # Parces BrowserEfficiency log
        def browser_efficiency(data_frame):
            log = []
            browser_frame = pd.DataFrame()
            browser_log_dict = {}
            with open(filepath) as browser_efficiency_log:
                # browser_log = csv.reader(browser_efficiency_log, delimiter = " ")
                browser_log = json.load(browser_efficiency_log)
                if ("CatapultBrowsing_v2" in browser_log):
                    browser_log_dict = browser_log["CatapultBrowsing_v2"]
                elif ("4TabBrowsing" in browser_log):
                    browser_log_dict = browser_log["4TabBrowsing"]
                '''
                for i in browser_log:
                    log.append([i for i in i if i != delim1 and i != delim2])
                '''
            '''
            tab_list = []

            for row in log:
                for item in row:
                    if "seconds" in item:
                        tab_list.append(row)
                        break
            for i in range(len(tab_list)):
                browser_frame[tab_list[i][3]] = [tab_list[i][6]]
            '''
            for key, val in browser_log_dict.items():
                if key in browser_efficiency_index:
                    match = re.search(r"[\d.]+", val)
                    if match:
                        numeric_value = float(match.group())
                        browser_frame[key] = [numeric_value]

            data_frame = pd.concat([data_frame, browser_frame], axis = 0)
            return data_frame
        '''
        for subdir, dirs, files in os.walk(rootdir):
            for file in files:

                filepath = subdir + os.sep + file

                if filepath.endswith("_Summary.csv"):
                    folder      = subdir.split('.')
                    folder_name = folder[-1]

                    df      = pd.read_csv(filepath)
                    Index   = df["Name"].tolist()
                    df      = df.T

                    #assumption is if len == 2 then TotalAverage would be present
                    if len(df.index) == 2:
                        df = df.rename(index = {'Total_Average' : folder_name})
                    else:
                        df = df.rename(index = {'workload' : folder_name})

                    # we are getting only column with the name folder name
                    frame = df.loc[[folder_name]]

                    d_frame = data_frame()

                    data = pd.concat([data, frame, d_frame], axis = 0)
                elif filepath.endswith("-socwatch-default.csv") or filepath.endswith("-socwatch.csv"):
                    data = socwatch_frame(data)
                elif "results.json" in filepath:
                    data = browser_efficiency(data)
        '''
        # Replace the main file processing loop with this:

        # Dictionary to track directories and their files
        dir_files = {}
        summary_indices = []  # Store indices from _Summary.csv files

        # First pass: catalog all files by directory
        for subdir, dirs, files in os.walk(self.rootdir):
            dir_files[subdir] = {
                'summary_file': None,
                'socwatch_file': None,
                'results_file': None
            }

            for file in files:
                if file.endswith("_Summary.csv"):
                    dir_files[subdir]['summary_file'] = file
                elif file.endswith("-socwatch-default.csv") or file.endswith("-socwatch.csv"):
                    dir_files[subdir]['socwatch_file'] = file
                elif "results.json" in file:
                    dir_files[subdir]['results_file'] = file
        # Second pass: process directories based on what files they contain
        for subdir, file_info in dir_files.items():
            has_summary = file_info['summary_file'] is not None
            has_socwatch = file_info['socwatch_file'] is not None
            has_results = file_info['results_file'] is not None

            if has_summary:
                # Process _Summary.csv file
                filepath = subdir + os.sep + file_info['summary_file']
                folder = subdir.split('.')
                folder_name = folder[-1]

                df = pd.read_csv(filepath)
                Index = df["Name"].tolist()
                summary_indices = Index.copy()  # Store for standalone socwatch processing
                df = df.T

                if len(df.index) == 2:
                    df = df.rename(index={'Total_Average': folder_name})
                else:
                    df = df.rename(index={'workload': folder_name})

                frame = df.loc[[folder_name]]
                d_frame = data_frame()
                data = pd.concat([data, frame, d_frame], axis=0)

                # Process socwatch if it exists in same directory
                if has_socwatch:
                    filepath = subdir + os.sep + file_info['socwatch_file']
                    data = socwatch_frame(data)

                # Process browser efficiency if it exists in same directory
                if has_results:
                    filepath = subdir + os.sep + file_info['results_file']
                    data = browser_efficiency(data)



        # Rest of your code remains the same...

        data    = data.T

        data    = data.fillna(0.0)
        col     = data.columns
        main_column = 0

        for i in range(len(col)):

            if type(col[i]) != type('string'):
                data.iloc[:, main_column] = data.iloc[:, main_column].astype(float) + data.iloc[:, i].astype(float)
            else:
                main_column = i

        Final_data = pd.DataFrame()
        for i in range(len(col)):
            if type(col[i]) == type("String"):
                Final_data = pd.concat([Final_data, data.iloc[:, i]], axis = 1)

        for i in soc_index:
            Index.append(i)

        for i in browser_efficiency_index:
            Index.append(i)

        for i in pch_index:
            Index.append(i)

        for i in ioe_pch_index:
            Index.append(i)
        try:
            Final_data.index = Index
        except:
            Final_data.index = Index[: max_index]

        if args.sku == "mtl-p":
            data2 = Final_data.loc[mtl_p[:]]

        elif args.sku == "mtl-m":
            data2 = Final_data.loc[mtl_m[:]]

        elif args.sku == "arl-h":
            data2 = Final_data.loc[arl_h[:]]

        elif args.sku == "arl-u":
            data2 = Final_data.loc[arl_u[:]]

        elif args.sku == "arl-s":
            data2 = Final_data.loc[arl_s[:]]

        elif args.sku == "lnl-m":
            data2 = Final_data.loc[lnl_m[:]]

        elif args.sku == "ptl-p":
            data2 = Final_data.loc[ptl_p[:]]

        elif args.sku == "nvl-s":
            data2 = Final_data.loc[nvl_s[:]]

        else:
            print("ERROR: No SKU is chosen! Please choose a sku from the options list!")

        try:
            data2 = pd.concat([data2, Final_data.loc[soc_index[:]]], axis = 0)

        except:
            print("No SoCWatch data")

        try:
            data2 = pd.concat([data2, Final_data.loc[browser_efficiency_index[:]]], axis = 0)

        except:
            print("No BrowserEfficiencyTestLog")

        try:
            data2 = pd.concat([data2, Final_data.loc[pch_index[:]]], axis = 0)

        except:
            print("No PCH Data")

        try:
            data2 = pd.concat([data2, Final_data.loc[ioe_pch_index[:]]], axis = 0)

        except:
            print("No IOE PCH Data")

        with pd.ExcelWriter("{}Summary_{}.xlsx".format(self.rootdir, self.time_stamp)) as writer:
            Final_data.to_excel(writer, sheet_name = "All Rails")

            try:
                data2.to_excel(writer, sheet_name = "Focus Rails")
                print("Data has been written to: {}Summary_{}.xlsx file.".format(self.rootdir, self.time_stamp))

                if args.console:
                    print(data2.to_markdown())

            except:
                print("No data")

        return self.rootdir, "Summary_{}.xlsx".format(self.time_stamp)

if __name__ == '__main__':
    data = PowerRoll("c:\\_hopper_results\\20260203T193430_CMS-Mode-MCS-State\\")
    file_result = data.main()
