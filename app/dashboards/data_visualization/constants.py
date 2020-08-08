slm280_columns = [
    "Time",
    "Platform",
    "Build Chamber",
    "Pump1",
    "Cabinet",
    "Cabinet 2",
    "Optical Bench",
    "Collimator",
    "Ambiance",
    "Dew point",
    "Oxygen 1",
    "Oxygen 2",
    "Pressure",
    "Filter Status",
    "T_LL",
    "T_LR",
    "T_U",
    "R_LL",
    "-",
    "-.1",
    "-.2",
    "R_LR",
    "R_U",
    "B_F",
    "B_R",
    "-.3",
    "Cyclone",
    "S_MAX",
    "S_MIN",
    "VSTG1",
    "VSTG2",
    "Gas Temp",
    "Gas flow speed",
    "MemTotal",
    "MemProcess",
    "Laser Emission Flags",
    "Laser On Flags",
    "Galvo X0",
    "Galvo Y0",
    "Galvo X1",
    "Galvo Y1",
]

slm500_columns = [
    "Time",
    "Pressure",
    "Filter Status",
    "Gas flow speed",
    "Gas pump power",
    "Oxygen top",
    "Oxygen 2",
    "Gas Temp",
    "Platform",
    "Build Chamber",
    "Optical Bench",
    "Collimator",
    "T_U",
    "T_LL",
    "T_LR",
    "R_LL",
    "R_LR",
    "B_F",
    "B_R",
    "Pump",
    "Cabinet",
    "Cabinet 2",
    "Ambiance",
    "MemTotal",
    "MemProcess",
    "Laser Emission Flags",
    "Laser On Flags",
    "Galvo X0",
    "Galvo Y0",
    "Servo X0",
    "Servo Y0",
    "Optic1 Home-in X1",
    "Optic1 Home-in Y1",
    "Optic1 Home-in X2",
    "Optic1 Home-in Y2",
]

column_mapper = {
    "Gas Temp": "GasTemp",
    "Gas flow speed": "GasFlowSpeed",
    "Build Chamber": "BuildChamber",
    "Filter Status": "FilterStatus",
    "Pump1": "Pump",
    "Cabinet": "Cabinet1",
    "Cabinet 2": "Cabinet2",
    "Optical Bench": "OpticalBench",
    "Oxygen top": "Oxygen1",
    "Oxygen 1": "Oxygen1",
    "Oxygen 2": "Oxygen2",
    "Laser Emission Flags": "LaserEmissionFlags",
    "Laser On Flags": "LaserOnFlags",
}

columns_to_keep = [
    "Time",
    "Pressure",
    "GasTemp",
    "GasFlowSpeed",
    "BuildChamber",
    "Pump",
    "FilterStatus",
    "Platform",
    "Cabinet1",
    "Cabinet2",
    "OpticalBench",
    "Collimator",
    "Ambiance",
    "Oxygen1",
    "Oxygen2",
    "MemTotal",
    "MemProcess",
    "LaserEmissionFlags",
    "LaserOnFlags",
]
