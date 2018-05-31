from pysnmp.entity.rfc3413.oneliner import cmdgen
from time import sleep


def get_wlan0(varnames, idx=None):
    if idx is None:
        idx = range(len(varnames))
    cmd = cmdgen.CommandGenerator()
    errorIndication, errorStatus, errorIndex, varBindTable = cmd.nextCmd(
            cmdgen.CommunityData('public'),
            cmdgen.UdpTransportTarget(('10.0.1.1', 161)),
            *varnames)
    if errorIndication:
        print errorIndication
    else:
        if errorStatus:
            print errorStatus.prettyPrint(),
            print errorIndex and varBindTable[-1][int(errorIndex)-1] or '?'
        else:
            vals = []
            for tr in varBindTable:
                if str(tr[0][1]) not in 'wlan0':
                    continue
                for i in idx:
                    vals.append(tr[i][1])
                return vals


def get_ifspeed():
    varnames = (cmdgen.MibVariable('IF-MIB', 'ifDescr'),
                cmdgen.MibVariable('IF-MIB', 'ifSpeed'))
    return [int(v) for v in get_wlan0(varnames, [1])][0]


def get_octets():
    varnames = (cmdgen.MibVariable('IF-MIB', 'ifDescr'),
                cmdgen.MibVariable('IF-MIB', 'ifInOctets'),
                cmdgen.MibVariable('IF-MIB', 'ifOutOctets'))
    vals = get_wlan0(varnames, [1, 2])
    return (int(v) for v in vals)


def diff((a, b)):
    return b - a


def bandwidth_on_halfduplex(ifspeed, (in_, out_), dsec=1):
    return float(diff(in_) + diff(out_)) * 800 / (ifspeed * dsec)


if __name__ == '__main__':
    ifspeed = get_ifspeed()
    dsec, octets = 5, None
    for i in xrange(12):
        in_oct, out_oct = get_octets()
        if octets is None:
            octets = [[in_oct, in_oct], [out_oct, out_oct]]
        else:
            octets = [[octets[0][1], in_oct], [octets[1][1], out_oct]]
        print bandwidth_on_halfduplex(ifspeed, octets, dsec)
        sleep(dsec)
