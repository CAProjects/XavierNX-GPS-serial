import io
import serial

# Serial setup
serialConf = serial.Serial('/dev/ttyTHS0', 9600, timeout=1.0)
serialio = io.TextIOWrapper(io.BufferedRWPair(serialConf, serialConf))

# Enable only NMEA sentences required
serialConf.write(b'$PMTK314,0,1,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1*34\r\n')

# NMEA sentences required
nmea_list = ['$GPGGA', '$GPGSA', '$GPRMC', '$GPZDA']

def speedCalc(data, u):
    #converts speed to user required units
    if u == 1:
          return f'{round((float(data) * 1.150779448),1)} MPH' 
    elif u == 2:
        return f'{round((float(data) * 1.852),1)} KM/H'
    elif u == 3:
        return f'{round((float(data) * 1.943844),1)} m/s'
    else:
        return f'{round(float(data),1)} kn'

def coordDecode(data, b):
    #decodes lat and lon co-ordinates from GPS NMEA
    sec = round((60*float(f"0.{data.split('.')[1]}")),4)
    return f"{data.split('.')[0][0:-2]}{b} {data.split('.')[0][-2:]}m {sec}s "

def nmeaDecode(data):
    #create dictionary to put data into
    nmea_dict = {}
    
    # for each NMEA sentence, extract the data required
    # and add it to the dictionary
    for x in data:
        if x[0] == '$GPGGA':
            nmea_dict['satelites'] = int(x[7])
            nmea_dict['altitude'] = f'{x[9]} {x[10]}'

        elif x[0] == '$GPGSA':
            nmea_dict['fix'] = True if int(x[2]) > 1 else False
            nmea_dict['fix_type'] = f'{x[2]}D' if int(x[2]) > 1 else ''
        
        elif x[0] == '$GPRMC':
            #decodes lat and lon to degrees and mins
            nmea_dict['latitude'] = coordDecode(x[3], x[4])
            nmea_dict['longitude'] = coordDecode(x[5], x[6])
        
            # for speed, it can be calculated in MPH, KM/H, m/s Knots
            # 1 = MPH | 2 = KM/H | 3 = m/s | any other no. for knots
            nmea_dict['speed'] = speedCalc(x[7], 1)
        elif x[0] == '$GPZDA':
            # gets the date and time from GPS
            nmea_dict['date_time'] = f'{x[2]}/{x[3]}/{x[4][-2:]} {x[1][0:2]}:{x[1][2:4]}:{x[1][4:6]}'
        
    # return the dictionary    
    return nmea_dict

def nmea_display(data):
    # displays the required GPS data
    # to the pi-top[4] miniscreen
    print(f'''
        Lat:  {data['latitude']}\tSpd: {data['speed']}
        Lon: {data['longitude']}\tAlt: {data['altitude']}
        UTC:{data['date_time']}\tFix: {'Yes' if data['fix'] else 'No'}, {data['fix_type']}, {data['satelites']} Sats
    ''')

while 1:
    try:
        # create a list for NMEA sentences
        l=[]
        # Get NMEA sentence
        s = serialio.readline().strip().split(',')
        # look for the start of the sentence queue
        if s[0] =='$GPGGA':
            # get all the sentences that matches the list
            for x in nmea_list:
                # add sentence to the list
                l.append(s)
                # get next sentence
                s = serialio.readline().strip().split(',')
            
            # decode the NMEA sentences and display the information
            # on the pi-top[4] miniscreen
            nmea_display(nmeaDecode(l))
            
    # This exeption is to prevent the script from crashing if there
    # is some garbled GPS data that cannot be decoded to UTF-8
    # this normally happens at the start of running the script
    # and is away of ignoring it
    except UnicodeDecodeError as e:
        continue
