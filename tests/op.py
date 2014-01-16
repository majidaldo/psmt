import sys
import operator


if __name__=='__main__':
    opstr=sys.argv[1]
    if opstr=='add':   op=operator.add
    elif opstr=='mul': op=operator.mul
    else:raise ValueError('dont know the operator')	

    o=op(*[float(an) for an in sys.argv[2:]])
    with open('o','w') as of:
        of.write(str(o))