import math

def pathLength(points):
    total = 0
    for i in range(len(points) - 1):
        total += math.hypot(points[i+1]['x'] - points[i]['x'], points[i+1]['y'] - points[i]['y'])
    return total

def pointAtDistance(points, distance):
    remaining = max(0, distance)
    for i in range(len(points) - 1):
        a = points[i]
        b = points[i+1]
        l = math.hypot(b['x'] - a['x'], b['y'] - a['y'])
        if remaining <= l:
            t = 0 if l == 0 else remaining / l
            return {
                'x': a['x'] + (b['x'] - a['x']) * t,
                'y': a['y'] + (b['y'] - a['y']) * t
            }
        remaining -= l
    return dict(points[-1])

def pathSlice(points, from_dist, to_dist):
    total = pathLength(points)
    from_dist = max(0, min(total, from_dist))
    to_dist = max(from_dist, min(total, to_dist))
    result = [pointAtDistance(points, from_dist)]
    travelled = 0
    for i in range(len(points) - 1):
        a = points[i]
        b = points[i+1]
        travelled += math.hypot(b['x'] - a['x'], b['y'] - a['y'])
        if travelled > from_dist and travelled < to_dist:
            result.append(dict(b))
    result.append(pointAtDistance(points, to_dist))
    return result

def generateArrowSvgData(pts, cornerRadius, triLen, triWidth):
    if not pts or len(pts) < 2:
        return {'bodyD': '', 'headD': '', 'hitboxD': ''}
    clean = [pts[0]]
    for i in range(1, len(pts)):
        prev = clean[-1]
        if math.hypot(pts[i]['x'] - prev['x'], pts[i]['y'] - prev['y']) > 0.5:
            clean.append(pts[i])
    if len(clean) < 2:
        return {'bodyD': '', 'headD': '', 'hitboxD': ''}
    
    tip = clean[-1]
    preTip = clean[-2]
    finalDx = tip['x'] - preTip['x']
    finalDy = tip['y'] - preTip['y']
    finalLen = math.hypot(finalDx, finalDy)
    if finalLen < 0.01:
        return {'bodyD': '', 'headD': '', 'hitboxD': ''}
        
    uDx = finalDx / finalLen
    uDy = finalDy / finalLen
    perpX = -uDy
    perpY = uDx
    
    bx = tip['x'] - triLen * uDx
    by = tip['y'] - triLen * uDy
    
    w1x = bx + triWidth * perpX
    w1y = by + triWidth * perpY
    w2x = bx - triWidth * perpX
    w2y = by - triWidth * perpY
    
    headD = f"M {tip['x']:.1f} {tip['y']:.1f} L {w1x:.1f} {w1y:.1f} L {w2x:.1f} {w2y:.1f} Z"
    return {'headD': headD, 'clean': len(clean)}

arrow_pts = [{'x': 253, 'y': 289}, {'x': 217, 'y': 289}, {'x': 181, 'y': 289}]
origLen = 72
exitDist = 313
extended = arrow_pts + [{'x': 181 - exitDist, 'y': 289}]

for p in range(0, 101, 5):
    prog = p / 100.0
    trav = exitDist * prog
    sliced = pathSlice(extended, trav, origLen + trav)
    svg = generateArrowSvgData(sliced, 15, 17, 10)
    print(f"Prog {prog:.2f}: trav={trav:.1f}, sliced pts={len(sliced)}, head={sliced[-1]['x']:.1f}, tail={sliced[0]['x']:.1f}")
