def find_delta(toponym):
    delta_x1, delta_y1 = [float(x) for x in toponym["boundedBy"]["Envelope"]["lowerCorner"].split()]
    delta_x2, delta_y2 = [float(x) for x in toponym["boundedBy"]["Envelope"]["upperCorner"].split()]
    delta_x = abs(delta_x1 - delta_x2)
    delta_y = abs(delta_y1 - delta_y2)
    span = f'{delta_x},{delta_y}'
    return span