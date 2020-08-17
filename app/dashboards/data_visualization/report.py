from statsmodels.tsa.seasonal import seasonal_decompose
from sklearn.linear_model import LinearRegression

result = []


class Checker:
    def __init__(self, sensor):
        self.sensor = sensor
        self.describe = sensor.describe()

    def checkPressure(self):
        def detect_stable(trend, std, tol):
            sensor_ = trend.loc[
                (trend["Pressure"] > std - tol) & (trend["Pressure"] < std + tol)
            ]
            l, tmp = [], []
            for i in sensor_.index:
                if len(tmp) == 0:
                    tmp.append(i)
                else:
                    if tmp[-1] + 1 == i:
                        tmp.append(i)
                    else:
                        l.append(tmp)
                        tmp = [i]
            if len(tmp) != 0:
                l.append(tmp)
            l_sort = sorted(l, key=len)
            l_sort.reverse()
            start, end = l_sort[0][0], l_sort[0][-1]
            startt, endt = trend.loc[start, "Time"], trend.loc[end, "Time"]
            return start, end, startt, endt

        def detect_unstable(trend, stable_stat):
            trend = pd.DataFrame(trend).reset_index()
            start, end, startt, endt = stable_stat
            before = pd.DataFrame(trend[:start])
            after = pd.DataFrame(trend[end:])
            return before, after

        def check_tur(unstable_stat):
            before, after = unstable_stat
            reg = LinearRegression()
            if len(before) > 100:
                reg.fit(pd.DataFrame(before.index), before["Pressure"])
                score1 = reg.score(pd.DataFrame(before.index), before["Pressure"])
                slope1 = reg.coef_[0]
            else:
                score1 = -1
                slope1 = -1
            if len(after) > 100:
                reg.fit(pd.DataFrame(after.index), after["Pressure"])
                score2 = reg.score(pd.DataFrame(after.index), after["Pressure"])
                slope2 = reg.coef_[0]
            else:
                score2 = -1
                slope2 = -1
            return score1, slope1, score2, slope2

        def check_stable_tur(start, end):
            sensor_before = self.sensor.reset_index()[:start]
            sensor_after = self.sensor.reset_index()[end:]
            maxb, minb, maxa, mina = 0, 0, 0, 0
            reg = LinearRegression()
            if len(sensor_before) > 1000:
                reg.fit(pd.DataFrame(sensor_before.index), sensor_before["Pressure"])
                slope1, score1 = (
                    reg.coef_[0],
                    reg.score(
                        pd.DataFrame(sensor_before.index), sensor_before["Pressure"]
                    ),
                )
                maxb, minb = (
                    sensor_before.describe()["Pressure"]["max"],
                    sensor_before.describe()["Pressure"]["min"],
                )
            else:
                score1 = -1
                slope1 = -1
            if len(sensor_after) > 1000:
                reg.fit(pd.DataFrame(sensor_after.index), sensor_after["Pressure"])
                slope2, score2 = (
                    reg.coef_[0],
                    reg.score(
                        pd.DataFrame(sensor_after.index), sensor_after["Pressure"]
                    ),
                )
                maxa, mina = (
                    sensor_after.describe()["Pressure"]["max"],
                    sensor_after.describe()["Pressure"]["min"],
                )
            else:
                score2 = -1
                slope2 = -1
            return score1, slope1, score2, slope2, maxb, minb, maxa, mina

        decomposition = seasonal_decompose(
            self.sensor["Pressure"], model="additive", freq=len(self.sensor) // 500
        )
        trend = decomposition.trend
        # seasonal = decomposition.seasonal
        # residual = decomposition.resid
        trend_df = pd.DataFrame(trend).reset_index().dropna()
        stable_tuple = detect_stable(trend_df, 12, 0.1)
        unstable_tuple = detect_unstable(
            trend_df, stable_tuple
        )  # roughly divide in 3 sectors, apply linear regression to before and after to see a general trend

        return (
            check_tur(unstable_tuple),
            stable_tuple,
            unstable_tuple,
            check_stable_tur(stable_tuple[0], stable_tuple[1]),
        )

    def checkFilter(self):
        # Filter Status	Pressure inside filter	<80mbar
        # Need to alert to change filter when >100mbar
        std, alert = 80, 100
        max = self.describe["Filter Status"]["max"]
        if max > 100:
            return False, max
        else:
            return True, max

    def checkFlow(self):
        # Gas flow speed	The gas flow speed of argon gas	~20 m/s
        # Need to increase gas pump power when speed is low
        # std, tol = 20, 2
        # if abs(self.describe['Gas flow speed']['50%'] - std) < tol:
        #   return True
        # else:
        #   return False
        return self.checkStability("Gas flow speed")

    # def checkPump(self):
    #     if "Gas pump power" in self.sensor.columns:
    #         return self.checkStability("Gas pump power")  # SLM500
    #     else:
    #         return self.checkStability("Pump1")  # SLM280

    def checkOxygen(self, oxygen):
        # Oxygen top	% of oxygen at powder tank	0.00 after few hours
        # Job can start when <0.10% and should gradually decrease to 0
        if oxygen not in self.sensor.columns:
            oxygen = "Oxygen top"
        sensor_abnormal = self.sensor[self.sensor[oxygen] >= 0.1]
        sensor_less = self.sensor[self.sensor[oxygen] < 0.1]
        sensor_zero = self.sensor[self.sensor[oxygen] < 10 ** -3]
        if len(sensor_abnormal) < len(sensor_less) < len(sensor_zero):
            return True, None, None
        elif len(sensor_zero) < len(sensor_abnormal) or len(sensor_less) < len(
            sensor_abnormal
        ):
            des = sensor_abnormal.describe()[oxygen]
            mean, std = des["mean"], des["std"]
            return False, mean - std, mean + std
        elif len(sensor_less) < len(sensor_abnormal) < len(sensor_zero):
            return False, "abnormal", None
        else:
            return False, "less", None

    def checkOxygen1(self):
        # Oxygen 1	% of oxygen at build chamber	0.00 after few hours
        # Job can start when <0.10% and should gradually decrease to 0
        return self.checkOxygen("Oxygen 1")

    def checkOxygen2(self):
        # Oxygen 2	% of oxygen at build chamber	0.00 after few hours
        # Job can start when <0.10% and should gradually decrease to 0
        return self.checkOxygen("Oxygen 2")

    def checkStability(self, var):
        mean, std = self.describe[var]["mean"], self.describe[var]["std"]
        stable_print = self.sensor[self.sensor[var].between(mean - std, mean + std)]
        # 68–95–99.7 rule to validate stability
        if len(stable_print) / len(self.sensor) >= 0.6827:
            return True, mean - std, mean + std, None
        else:
            return (
                False,
                mean - std,
                mean + std,
                100 - len(stable_print) / len(self.sensor) * 100,
            )

    def checkGasTemp(self):
        # Gas Temp
        # Temperature of the gas flow	Remain stable during printing
        return self.checkStability("Gas Temp")

    def checkPlat(self):
        # Platform
        # Temperature of the platform	Remain stable during printing	Normally it is 200 degrees for printing Ti6Al4V
        return self.checkStability("Platform")

    def checkChamber(self):
        # Build Chamber	Temperature of build chamber
        # Remain stable during printing
        return self.checkStability("Build Chamber")

    def checkOptical(self):
        # Optical bench	Temperature of optical bench
        # Remain stable during printing
        return self.checkStability("Optical Bench")

    def checkCollimator(self):
        # Collimator
        # Temperature of collimator	Remain stable during printing
        return self.checkStability("Collimator")

    # report generation function
    def generateReport(self):
        sep = "---------------------------------------------"
        print("Pressure: ")
        check, stable, unstable, stable_tur = self.checkPressure()
        score1, slope1, score2, slope2 = check
        score10, slope10, score20, slope20, max1, min1, max2, min2 = stable_tur
        print(
            "Pressure remains stable around 12 mbar between {} and {}".format(
                stable[2], stable[3]
            )
        )
        if score1 != -1 and score10 != -1:
            print("For the time before {} : ".format(stable[2]))
            if score1 / score10 > 5:
                print(
                    "The pressure occurs great fluctuation, ranging from {:.2f} to {:.2f} mbar".format(
                        min1, max1
                    )
                )
                result.append(-1)
            elif score1 > 0.85:
                if slope1 > 0:
                    print("The pressure keeps increasing smoothly")
                    result.append(-1)
                else:
                    print("The pressure keeps decreasing smoothly")
                    result.append(-1)
            else:
                if slope1 > 0:
                    print("The pressure keeps increasing with fluctuation")
                    result.append(-1)
                else:
                    print("The pressure keeps decreasing with fluctuation")
                    result.append(-1)
        else:
            result.append(1)

        if score2 != -1 and score20 != -1:
            print("For the time after {} : ".format(stable[3]))
            if score2 / score20 > 5:
                print(
                    "The pressure occurs great fluctuation, ranging from {:.2f} to {:.2f} mbar".format(
                        min2, max2
                    )
                )
                result.append(-1)
            elif score2 > 0.85:
                if slope2 > 0:
                    print("The pressure keeps increasing smoothly")
                    result.append(-1)
                else:
                    print("The pressure keeps decreasing smoothly")
                    result.append(-1)
            else:
                if slope2 > 0:
                    print("The pressure keeps increasing with fluctuation")
                    result.append(-1)
                else:
                    print("The pressure keeps decreasing with fluctuation")
                    result.append(-1)
        else:
            result.append(1)
        print(sep)

        print("Filter: ")
        flag, max = self.checkFilter()
        if flag:
            print(f"OK; Max temperature: {max}°C < 100°C")
            result.append(1)
        else:
            print(f"Abnormal; Max temperature: {max}°C")
            result.append(-1)

        print(sep)

        print("Gas flow speed: ")
        flag, min, max, outlier = self.checkFlow()
        if flag:
            print("OK; Stable between {:.2f} m/s and {:.2f} m/s".format(min, max))
            result.append(1)
        else:
            print(
                "Abnormal; {:.2f}% data fall out the stable range between {:.2f} m/s and {:.2f} m/s".format(
                    outlier, min, max
                )
            )
            result.append(-1)
        print(sep)

        # print("Gas pump power")
        # flag, min, max, outlier = self.checkPump()
        # if max > 90:
        #     print("Alert; Gas pump power reaches {:.2f}% > 90%".format(max))
        #     result.append(-1)
        # elif flag:
        #     print("OK; Stable between {:.2f}% and {:.2f}%".format(min, max))
        #     result.append(1)
        # else:
        #     print(
        #         "Abnormal; {:.2f}% data fall out the stable range between {:.2f}% and {:.2f}%".format(
        #             outlier, min, max
        #         )
        #     )
        #     result.append(-1)
        # print(sep)

        print("Oxygen 1")
        flag, v1, v2 = self.checkOxygen1()
        if flag:
            print("OK; Standard fulfilled")
            result.append(1)
        else:
            if v1 == "abnormal":
                print(
                    "Abnormal; oxygen concentration >0.1% takes up more time that <0.1% decreasing to 0% takes"
                )
                result.append(-1)
            elif v1 == "less":
                print(
                    "Abnormal; it takes too long to decrease the oxygen concentration to 0%"
                )
                result.append(-1)
            else:
                print(
                    "Abnormal; oxygen concentration >0.1% mainly, ranging from {:.4f} to {:.4f} mainly".format(
                        v1, v2
                    )
                )
                result.append(-1)

        print(sep)

        print("Oxygen 2")
        flag, v1, v2 = self.checkOxygen2()
        if flag:
            print("OK; Standard fulfilled")
            result.append(1)
        else:
            if v1 == "abnormal":
                print(
                    "Abnormal; oxygen concentration >0.1% takes up more time that <0.1%"
                )
                result.append(-1)
            elif v1 == "less":
                print(
                    "Abnormal; it takes too long to decrease the oxygen concentration to 0%"
                )
                result.append(-1)
            else:
                print(
                    "Abnormal; oxygen concentration >0.1% mainly, ranging from {:.4f} to {:.4f} mainly".format(
                        v1, v2
                    )
                )
                result.append(-1)

        print(sep)

        print("Gas Temperature: ")
        flag, min, max, outlier = self.checkGasTemp()
        if flag:
            print("OK; Stable between {:.2f}°C and {:.2f}°C".format(min, max))
            result.append(1)
        else:
            print(
                "Abnormal; {:.2f}% data fall out the stable range between {:.2f} m/s and {:.2f} m/s".format(
                    outlier, min, max
                )
            )
            result.append(-1)
        print(sep)

        print("Platform Temperature: ")
        flag, min, max, outlier = self.checkPlat()
        if flag:
            print("OK; Stable between {:.2f}°C and {:.2f}°C".format(min, max))
            result.append(1)
        else:
            print(
                "Abnormal; {:.2f}% data fall out the stable range between {:.2f} m/s and {:.2f} m/s".format(
                    outlier, min, max
                )
            )
            result.append(-1)
        print(sep)

        print("Build Chamber Temperature: ")
        flag, min, max, outlier = self.checkChamber()
        if flag:
            print("OK; Stable between {:.2f}°C and {:.2f}°C".format(min, max))
            result.append(1)
        else:
            print(
                "Abnormal; {:.2f}% data fall out the stable range between {:.2f}°C and {:.2f}°C".format(
                    outlier, min, max
                )
            )
            result.append(-1)
        print(sep)

        print("Optical Bench Temperature: ")
        flag, min, max, outlier = self.checkOptical()
        if flag:
            print("OK; Stable between {:.2f}°C and {:.2f}°C".format(min, max))
            result.append(1)
        else:
            print(
                "Abnormal; {:.2f}% data fall out the stable range between {:.2f}°C and {:.2f}°C".format(
                    outlier, min, max
                )
            )
            result.append(-1)
        print(sep)

        print("Collimator Temperature: ")
        flag, min, max, outlier = self.checkCollimator()
        if flag:
            print("OK; Stable between {:.2f}°C and {:.2f}°C".format(min, max))
            result.append(1)
        else:
            print(
                "Abnormal; {:.2f}% data fall out the stable range between {:.2f}°C and {:.2f}°C".format(
                    outlier, min, max
                )
            )
            result.append(-1)

        print(sep)
        print("Result:")
        alert = result.count(-1)
        print("Number of Alerts = ", alert)
        if "Gas pump power" in self.sensor.columns:
            result1 = str(round(alert / 11, 2))
            print("Level of Alert = ", result1)
        else:
            result1 = str(round(alert / 10, 2))
            print("Level of Alert = ", result1)
