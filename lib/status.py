from lib import colors

def working():
    start   = colors.reset() + "[" + colors.cyan() + "----" + colors.reset() + "]"
    return (start)

def input():
    iu    = colors.reset() + "[" + colors.yellow() + " ~> " + colors.reset() + "]"
    return (iu)

def ko():
    ko   = colors.reset() + "[" + colors.red() + " KO " + colors.reset() + "]"
    return (ko)

def ok():
    ok      = colors.reset() + "[" + colors.green() + " OK " + colors.reset() + "]"
    return (ok)

def info():
    io      = colors.reset() + "[" + colors.purple() + " ?? " + colors.reset() + "]"
    return (io)

def found():
    ye      = colors.reset() + "[" + colors.yellow() + " ## " + colors.reset() + "]"
    return (ye)

def error():
    no      = colors.reset() + "[" + colors.red() + " E: " + colors.reset() + "]"
    return (no)
