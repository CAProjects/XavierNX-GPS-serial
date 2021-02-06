# dataB is the raw byte string that is obtained from the GPS device
dataB = b'$GPGGA,233030.000,5629.4709,N,00255.3588,W,1,06,1.21,70.0,M,49.2,M,,*45\r\n$GPGSA,A,3,21,27,01,23,22,20,,,,,,,1.51,1.21,0.90*08\r\n$GPGSV,4,1,13,21,69,256,18,01,42,258,34,10,39,058,,27,35,138,22*7A\r\n$GPGSV,4,2,13,14,29,310,20,28,25,317,,22,24,204,33,32,22,105,19*76\r\n$GPGSV,4,3,13,23,10,044,18,20,07,047,17,30,02,281,,24,01,026,*7C\r\n$GPGSV,4,4,13,45,,,*7A\r\n$GPRMC,233030.000,A,5629.4709,N,00255.3588,W,0.15,144.55,040221,,,A*7B\r\n$GPZDA,233030.000,04,02,2021,,*50\r\n$GPGGA,233031.000,5629.4708,N,00255.3587,W,1,06,1.21,70.0,M,49.2,M,,*4A\r\n$GPGSA,A,3,21,27,01,23,22,20,,,,,,,1.51,1.21,0.90*08\r\n$GPRMC,233031.000,A,5629.4708,N,00255.3587,W,0.25,0.73,040221,,,A*72\r\n$GPZDA,233031.000,04,02,2021,,*51\r\n'

# Split the byte string into a list
dataD = dataB.split(b'$')

# List var for sorted data
gpsdata = []

# loop though the DataD list
for x in dataD:
    # ignore list entries that are blank
    if x != b'':        
        # decode byte string into UTF-8 and strip carrage returns
        t = str(x.decode('utf-8')).strip()
        
        # create list of remaning string
        t=t.split(',')
        
        # append it to  list to gpsdata list
        gpsdata.append(t)

# print the resutls
print(gpsdata)
