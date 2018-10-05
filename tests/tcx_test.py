from ..tcx import TCXParser


def tcx_test():
    tcx = TCXParser('/home/sorokin/Downloads/20180425_run_garmin.tcx')
    print(tcx.hr_max)
