def fact(a):
    '''n n!'''
    if int(a) <= 1:
        return 1
    return fact(int(a) - 1) * int(a)
