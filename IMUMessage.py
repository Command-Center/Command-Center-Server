class IMUMessage(object):
    def __init__(self, dt, AccM_Rf, AccM_Pf, T_sensor_house, Roll, Pitch, HeavePeriod, AccMru_F, AccMru_S, AccMru_D, AccMru_Ff, AccMru_Sf, AccMru_Df, PosMru_D):
        self.AccM_Rf = AccM_Rf
        self.AccM_Pf = AccM_Pf
        self.T_sensor_house = T_sensor_house
        self.Roll = Roll
        self.Pitch = Pitch
        self.HeavePeriod = HeavePeriod
        self.AccMru_F = AccMru_F
        self.AccMru_S = AccMru_S
        self.AccMru_D = AccMru_D
        self.AccMru_Ff = AccMru_Ff
        self.AccMru_Sf = AccMru_Sf
        self.AccMru_Df = AccMru_Df
        self.PosMru_D = PosMru_D
        self.timestamp = dt

