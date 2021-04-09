import pint

ureg = pint.UnitRegistry()
c = pint.Context('cook')

c.add_transformation('[volume]', '[mass]',
                     lambda ureg, x: x * (1 * ureg.oz / ureg.floz))
c.add_transformation('[mass]', '[volume]',
                     lambda ureg, x: x / (1 * ureg.oz / ureg.floz))
ureg.add_context(c)
ureg.enable_contexts('cook')

# this works fine
a = 1 * ureg.oz
print('%s = %s' % (a, a.to('floz')))

b = 10 * ureg.floz
c = 10 * ureg.gram
d = 8 * ureg.tbsp

# both these fail, see exception output below
print('%s = %s' % (c, c.to('floz')))
print('%s = %s' % (b, b.to('oz')))
print('%s = %s = %s = %s' % (c, c.to('oz'), c.to('floz'), c.to('cup')))
print('%s = %s = %s = %s' % (d, d.to('oz'), d.to('floz'), d.to('cup')))
print(f"{b:~}")

x = ureg.Quantity(20, 'adljsjf')
print(x)