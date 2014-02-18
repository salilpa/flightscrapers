import indigo
p = indigo.Indigo("BLR", "HYD") #10-digit PNR Number
if p.request() == True:
    print p.get_json()
else:
    print p.error

