import tempfile
import pyutilib.th as unittest
import sys
import os.path
import os
import glob
import pandas as pd
import shutil
import datetime
from datetime import datetime
import mape_maker
from mape_maker import __main__ as mapemain
dir_sep = "/"
p = str(mape_maker.__path__)
l = p.find("'")
r = p.find("'", l+1)
mape_maker_path = p[l+1:r]
file_path = mape_maker_path + dir_sep + "samples"
#to skip non-ops tests
operational_only = False

class TestUM(unittest.TestCase):


    def _base_dict(self):
        basedict = {"input_file"            : "",
                    "target_mape"           : None,
                    "simulated_timeseries"  : "",
                    "base-process"          : "",
                    "a"                     : None,
                    "output_dir"            : "result",
                    "number_simulations"    : 2,
                    "input_start_dt"        : None,
                    "input_end_dt"          : None,
                    "simulation_start_dt"   : None,
                    "simulation_end_dt"     : None,
                    "title"                 : "",
                    "seed"                  : 1234,
                    "curvature"             : None,
                    "time_limit"            : 1,
                    "curvature_target"      : None,
                    "mip"                   : None,
                    "solver"                : None,
                    "full_dataset"          : True,
                    "latex_output"          : False,
                    "show"                  : True
                    }

        return basedict

    @classmethod
    def setUpClass(self):
        self.cwd = os.getcwd()
        print("Current working directory:", self.cwd)
        self.saving = self.cwd + dir_sep + "wind_ops"
        print("the output dir will be saved to:", self.saving)
        # path to the csv files
        self.load_rts = file_path + dir_sep + "rts_gmlc" + dir_sep + \
                         "Load_forecasts_actuals.csv"
        self.load_ops = file_path + dir_sep + "rts_gmlc" + dir_sep + \
                         "load_operations_example.csv"

        self.wind_rts = file_path + dir_sep + "rts_gmlc" + dir_sep + \
                         "WIND_forecasts_actuals.csv"
        self.wind_ops = file_path + dir_sep + "rts_gmlc" + dir_sep + \
                         "wind_operations_example.csv"


    @unittest.skipIf(operational_only,
                     "skipping the first test - test_load_sd_ed_less_range")
    def test_load_sd_ed_less_range(self):
        '''
        The operational examples are giving very bad scenarios as of now.
        This test is using rts_wind test
        target mape             : dataset's mape (=186.39%)
        the input start date    : "2020-01-01 01:00:00"
        the input end date      : "2020-12-29 23:00:00"
        the sim start date      : "2020-12-30 00:00:00"
        the sim end date        : "2020-12-31 23:00:00"
        '''
        print("Running ", str(self.id()).split('.')[2])
        print("THIS TEST WILL FAIL -> sd and ed range is less than 12 days")
        # python -m mape_maker "mape_maker/samples/rts_gmlc/Load_forecasts_actuals.csv" -st "actuals" -n 5 -bp "ARMA" -is "2020-1-1 01:00:00" -ie "2020-12-29 23:00:00" -sd "2020-12-30 00:00:00" -ed "2020-12-31 23:00:00" -o "load_actuals_ARMA" -s 1234
        parm_dict                           = self._base_dict()
        parm_dict["input_file"]             = self.load_rts
        parm_dict["simulated_timeseries"]   = "actuals"
        parm_dict["number_simulations"]     = 5
        parm_dict["base-process"]           = "ARMA"
        parm_dict["input_start_dt"]         = datetime(year=2020, month=1, day=1, hour=0, minute=0, second=0)
        parm_dict["input_end_dt"]           = datetime(year=2020, month=12, day=29, hour=23, minute=0, second=0)
        parm_dict["simulation_start_dt"]    = datetime(year=2020, month=12, day=30, hour=0, minute=0, second=0)
        parm_dict["simulation_end_dt"]      = datetime(year=2020, month=12, day=31, hour=23, minute=0, second=0)
        parm_dict["output_dir"]             = "load_sd_ed_range_less"
        parm_list = list(parm_dict.values())
        # run the test
        mapemain.main_func(*parm_list)

        # save the output dir to the sub temporary directory
        output_dir_path = self.cwd  + dir_sep + parm_dict["output_dir"]
        shutil.move(output_dir_path, self.saving)

        plot1 = "mmFinalFig.png"
        shutil.move(plot1, self.saving + dir_sep + parm_dict["output_dir"] )


    @unittest.skipIf(operational_only,
                     "skipping the second test - test_load_sd_ed_min_range")
    def test_load_sd_ed_min_range(self):
        '''
        The minimum range between the sd and ed as of now is 12 days for load dataset
        otherwise the test fails
        '''
        print("Running ", str(self.id()).split('.')[2])
        print("THIS TEST WILL PASS -> sd and ed range is 12 days")
        # python -m mape_maker "mape_maker/samples/rts_gmlc/Load_forecasts_actuals.csv" -st "actuals" -n 5 -bp "ARMA" -is "2020-1-1 01:00:00" -ie "2020-12-29 23:00:00" -sd "2020-12-20 00:00:00" -ed "2020-12-31 23:00:00" -o "load_actuals_ARMA" -s 1234
        parm_dict                           = self._base_dict()
        parm_dict["input_file"]             = self.load_rts
        parm_dict["simulated_timeseries"]   = "actuals"
        parm_dict["number_simulations"]     = 5
        parm_dict["base-process"]           = "ARMA"
        parm_dict["input_start_dt"]         = datetime(year=2020, month=1, day=1, hour=0, minute=0, second=0)
        parm_dict["input_end_dt"]           = datetime(year=2020, month=12, day=29, hour=23, minute=0, second=0)
        parm_dict["simulation_start_dt"]    = datetime(year=2020, month=12, day=20, hour=0, minute=0, second=0)
        parm_dict["simulation_end_dt"]      = datetime(year=2020, month=12, day=31, hour=23, minute=0, second=0)
        parm_dict["output_dir"]             = "load_sd_ed_range_12"
        parm_list = list(parm_dict.values())
        # run the test
        mapemain.main_func(*parm_list)

        # save the output dir to the sub temporary directory
        output_dir_path = self.cwd  + dir_sep + parm_dict["output_dir"]
        shutil.move(output_dir_path, self.saving)

        plot1 = "mmFinalFig.png"
        shutil.move(plot1, self.saving + dir_sep + parm_dict["output_dir"] )

    '''
    #############################   OPERATIONAL TESTS   ############################
    '''

    def test_WIND_operations_example_1(self):
        print("OPERATIONAL TESTS")
        '''
        The operational examples are giving very bad scenarios as of now.
        This test is using rts_wind test
        target mape             : dataset's mape (=186.39%)
        the input start date    : "2020-01-01 01:00:00"
        the input end date      : "2020-12-29 23:00:00"
        the sim start date      : "2020-12-30 00:00:00"
        the sim end date        : "2020-12-31 23:00:00"
        '''
        print("Running ", str(self.id()).split('.')[2])
        # python -m mape_maker "mape_maker/samples/rts_gmlc/wind_operations_example.csv" -st "actuals" -n 5 -bp "ARMA" -is "2020-1-1 01:00:00" -ie "2020-12-29 23:00:00" -sd "2020-12-30 00:00:00" -ed "2020-12-31 23:00:00" -o "load_operations_example" -s 1234
        parm_dict                           = self._base_dict()
        parm_dict["input_file"]             = self.wind_ops
        parm_dict["simulated_timeseries"]   = "actuals"
        parm_dict["number_simulations"]     = 5
        parm_dict["base-process"]           = "ARMA"
        parm_dict["input_start_dt"]         = datetime(year=2020, month=1, day=1, hour=0, minute=0, second=0)
        parm_dict["input_end_dt"]           = datetime(year=2020, month=12, day=29, hour=23, minute=0, second=0)
        parm_dict["simulation_start_dt"]    = datetime(year=2020, month=12, day=30, hour=0, minute=0, second=0)
        parm_dict["simulation_end_dt"]      = datetime(year=2020, month=12, day=31, hour=23, minute=0, second=0)
        parm_dict["output_dir"]             = "wind_operations_example_1"
        parm_dict["target_mape"]            = 90
        parm_list = list(parm_dict.values())
        # run the test
        mapemain.main_func(*parm_list)

        # save the output dir to the sub temporary directory
        output_dir_path = self.cwd  + dir_sep + parm_dict["output_dir"]
        shutil.move(output_dir_path, self.saving)

        plot1 = "mmFinalFig.png"
        shutil.move(plot1, self.saving + dir_sep + parm_dict["output_dir"] )

    def test_WIND_operations_example_2(self):
        '''
        The operational examples are giving very bad scenarios as of now.
        This test is using rts_wind test
        target mape             : dataset's mape (=186.39%)
        the input start date    : "2020-01-01 01:00:00"
        the input end date      : "2020-12-29 23:00:00"
        the sim start date      : "2020-12-30 12:00:00" ****
        the sim end date        : "2020-12-31 23:00:00"
        '''
        print("Running ", str(self.id()).split('.')[2])
        # python -m mape_maker "mape_maker/samples/rts_gmlc/wind_operations_example.csv" -st "actuals" -n 5 -bp "ARMA" -is "2020-1-1 01:00:00" -ie "2020-12-29 23:00:00" -sd "2020-12-30 12:00:00" -ed "2020-12-31 23:00:00" -o "load_operations_example" -s 1234
        parm_dict                           = self._base_dict()
        parm_dict["input_file"]             = self.wind_ops
        parm_dict["simulated_timeseries"]   = "actuals"
        parm_dict["number_simulations"]     = 5
        parm_dict["base-process"]           = "ARMA"
        parm_dict["input_start_dt"]         = datetime(year=2020, month=1, day=1, hour=0, minute=0, second=0)
        parm_dict["input_end_dt"]           = datetime(year=2020, month=12, day=29, hour=23, minute=0, second=0)
        parm_dict["simulation_start_dt"]    = datetime(year=2020, month=12, day=12, hour=0, minute=0, second=0)
        parm_dict["simulation_end_dt"]      = datetime(year=2020, month=12, day=31, hour=23, minute=0, second=0)
        parm_dict["output_dir"]             = "wind_operations_example_2"
        parm_dict["target_mape"]            = 90
        parm_list = list(parm_dict.values())
        # run the test
        mapemain.main_func(*parm_list)

        # save the output dir to the sub temporary directory
        output_dir_path = self.cwd  + dir_sep + parm_dict["output_dir"]
        shutil.move(output_dir_path, self.saving)

        plot1 = "mmFinalFig.png"
        shutil.move(plot1, self.saving + dir_sep + parm_dict["output_dir"] )


if __name__ == "__main__":
    unittest.main()