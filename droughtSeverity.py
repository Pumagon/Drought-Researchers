from noaa_wbgt import getWbgtSummary

lat = 42.36575749436916
lon = -71.00974304515053

currentWbgt, todayMax, todayMin, tomorrowMax, tomorrowMin, weekMax, weekMin = getWbgtSummary(lat, lon)

print("Current WBGT (F): ", currentWbgt)
print("Max WBGT today (F): ", todayMax)
print("Min WBGT today (F): ", todayMin)
print("Max WBGT tomorrow (F): ", tomorrowMax)
print("Min WBGT tomorrow (F): ", tomorrowMin)
