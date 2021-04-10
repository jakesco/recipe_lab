import logging
from pint import UnitRegistry, Context
from pint.errors import UndefinedUnitError, DimensionalityError

DEBUGFORMATTER = '%(levelname)s:%(name)s:%(filename)s:%(funcName)s:%(lineno)d: %(message)s'
INFOFORMATTER = '%(levelname): %(message)s'


def init_log():
    log = logging.getLogger(__name__)
    log.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setFormatter(logging.Formatter(DEBUGFORMATTER))
    log.addHandler(ch)
    return log


def init_unit_registry():
    ureg = UnitRegistry()
    c = Context('cook')
    c.add_transformation('[volume]', '[mass]',
                        lambda ureg, x: x * (1 * ureg.oz / ureg.floz))
    c.add_transformation('[mass]', '[volume]',
                         lambda ureg, x: x / (1 * ureg.oz / ureg.floz))
    ureg.add_context(c)
    ureg.enable_contexts('cook')
    return ureg


log = init_log()
unit_registry = init_unit_registry()
Q_ = unit_registry.Quantity
