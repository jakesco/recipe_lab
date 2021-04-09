from pint import UnitRegistry, Context
from pint.errors import UndefinedUnitError

ureg = UnitRegistry()
Q_ = ureg.Quantity

c = Context('cook')
c.add_transformation('[volume]', '[mass]',
                     lambda ureg, x: x * (1 * ureg.oz / ureg.floz))
c.add_transformation('[mass]', '[volume]',
                     lambda ureg, x: x / (1 * ureg.oz / ureg.floz))
ureg.add_context(c)
ureg.enable_contexts('cook')

