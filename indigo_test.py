import indigo
from datetime import datetime, timedelta
p = indigo.Indigo("BLR", "DIB") #10-digit PNR Number
if p.request() == True:
    print p.get_json()
else:
    print p.error

