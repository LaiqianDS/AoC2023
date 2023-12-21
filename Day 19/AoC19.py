from collections import deque

D = open('input.txt').read().strip()

rules, parts = D.split('\n\n')
R = {}
for rule in rules.split('\n'):
    name, rest = rule.split('{')
    R[name] = rest[:-1]

def accept(part):
    state = 'in'
    while True:
        rule = R[state]
        for cmd in rule.split(','):
            applies = True
            res = cmd
            if ':' in cmd:
                cond,res = cmd.split(':')
                var = cond[0]
                op = cond[1]
                n = int(cond[2:])
                if op=='>':
                    applies = part[var] > n
                else:
                    applies = part[var] < n
            if applies:
                if res=='A':
                    return True
                if res=='R':
                    return False
                state = res
                break

ans = 0
for part in parts.split('\n'):
    part = part[1:-1]
    part = {x.split('=')[0]:int(x.split('=')[1]) for x in part.split(',')}
    if accept(part):
        ans += part['x']+part['m']+part['a']+part['s']
print(ans)

# part 2

# If we started with a pile of parts with range [lo,hi], which of those parts still follow the rule op(n)?
def new_range(op, n, lo, hi):
    if op=='>':
        lo = max(lo, n+1)
    elif op=='<':
        hi = min(hi, n-1)
    elif op=='>=':
        lo = max(lo, n)
    else:
        hi = min(hi, n)
    return (lo,hi)

def new_ranges(var, op, n, xl,xh,ml,mh,al,ah,sl,sh):
    if var=='x':
        xl,xh = new_range(op, n, xl, xh)
    elif var=='m':
        ml,mh = new_range(op, n, ml, mh)
    elif var=='a':
        al,ah = new_range(op, n, al, ah)
    elif var=='s':
        sl,sh = new_range(op, n, sl, sh)
    return (xl,xh,ml,mh,al,ah,sl,sh)

ans = 0
Q = deque([('in', 1, 4000, 1, 4000, 1, 4000, 1,4000)])
while Q:
    state, xl,xh,ml,mh,al,ah,sl,sh = Q.pop()
    if xl>xh or ml>mh or al>ah or sl>sh:
        continue
    if state=='A':
        score = (xh-xl+1)*(mh-ml+1)*(ah-al+1)*(sh-sl+1)
        ans += score
        continue
    elif state=='R':
        continue
    else:
        rule = R[state]
        for cmd in rule.split(','):
            applies = True
            res = cmd
            if ':' in cmd:
                cond,res = cmd.split(':')
                var = cond[0]
                op = cond[1]
                n = int(cond[2:])
                Q.append((res, *new_ranges(var, op, n, xl, xh, ml, mh, al, ah,sl, sh)))
                xl,xh,ml,mh,al,ah,sl,sh = new_ranges(var, '<=' if op=='>' else '>=', n, xl, xh, ml, mh, al, ah,sl, sh)
            else:
                Q.append((res, xl, xh, ml, mh, al, ah, sl, sh))
                break
print(ans)