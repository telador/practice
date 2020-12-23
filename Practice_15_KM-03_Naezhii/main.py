from factorial import factorial
from exp_root import root, exponentiation
from logarithm import logarithm


def ch(a, t=float):
    try:
        a = t(a)
    except ValueError:
        return False
    return True


f = {'1': (factorial.fact, (lambda x: x.isdecimal(),)), '2': (exponentiation.exp2, (lambda x: ch(x),)),
     '3': (exponentiation.exp3, (lambda x: ch(x),)), '4': (root.root2, (lambda x: ch(x) and float(x) > 0,)),
     '5': (root.root3, (lambda x: ch(x),)),
     '6': (logarithm.log, (lambda x: ch(x) and float(x) > 0 and float(x) != 1, lambda x: ch(x) and float(x) > 0)),
     '7': (logarithm.ln, (lambda x: ch(x) and float(x) > 0),), '8': (logarithm.lg, (lambda x: ch(x) and float(x) > 0,))}


def ask_user(checker, msg='', hint=''):
    while True:
        var = input(msg)
        if checker(var):
            return var
        if len(hint) != 0:
            print(hint)


def main():
    for k in f.keys():
        print(f'{k} - {f[k][0].__name__}')
    ans = ask_user(lambda x: x in f.keys(), 'Your choice(1-8): ',
                   'There is no such key. Try again')
    d = f[ans][0].__doc__.split()
    par = []
    for i in range(len(f[ans][1])):
        par.append(ask_user(f[ans][1][i], msg=d[i]+': '))
    print(d[-1], '=', f[ans][0](*par))


if __name__ == '__main__':
    main()
