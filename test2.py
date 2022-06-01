def f(a):
    if float(a) == 0:
        return '0.'
    if float(a) > 0:
        return a.lstrip('0')
    if float(a) < 0:
        return a.replace('-0', '-')

print(f('-0.0'))
print(f('0.0'))
print(f('100230.00234'))
print(f('0.43204'))
print(f('-23.5908'))
print(f('-2901.406'))
print(f('-0.32305'))
