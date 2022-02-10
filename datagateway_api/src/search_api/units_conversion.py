from pint import UndefinedUnitError, UnitRegistry

from datagateway_api.src.common.exceptions import FilterError, SearchAPIError
from datagateway_api.src.datagateway_api.icat.filters import (
    PythonICATDistinctFieldFilter,
)
from datagateway_api.src.datagateway_api.icat.helpers import get_entity_with_filters
from datagateway_api.src.search_api.session_handler import (
    client_manager,
    SessionHandler,
)


class UnitsConversion:
    unit_reg = UnitRegistry()

    def __init__(self):
        # TODO - change to self.get_parameter_type_units()
        self.icat_stored_units = good_isis_units
        self.unit_groups = self.group_units()

    # TODO - shouldn't need the decorator in API usage
    @client_manager
    def get_parameter_type_units(self):
        # TODO - probably should make this configurable, between units and unitsFullName
        distinct_name_filter = PythonICATDistinctFieldFilter("units")
        parameter_type_names = get_entity_with_filters(
            SessionHandler.client, "ParameterType", [distinct_name_filter],
        )

        parameter_units = []
        for name_dict in parameter_type_names:
            for _, parameter_name in name_dict.items():
                parameter_units.append(parameter_name)

        return parameter_units

    def group_units(self):
        unit_groups = {}

        for unit in self.icat_stored_units:
            pint_unit = UnitsConversion.get_unit(unit)
            unit_groups.setdefault(str(pint_unit.dimensionality), [])
            unit_groups[str(pint_unit.dimensionality)].append(unit)

        return unit_groups

    @staticmethod
    def get_unit(unit):
        try:
            return getattr(UnitsConversion.unit_reg, unit)
        except UndefinedUnitError as e:
            raise SearchAPIError(e)

    @staticmethod
    def get_unit_type(unit):
        return UnitsConversion.get_unit(unit).dimensionality

    def get_alternative_units(self, input_unit):
        unit_dimensionality = UnitsConversion.get_unit_type(input_unit)
        other_units = self.unit_groups[str(unit_dimensionality)]
        alternative_units = [other_unit for other_unit in other_units]

        return alternative_units

    def get_alternative_unit_values(self, input_unit, input_value):
        unit_dimensionality = UnitsConversion.get_unit_type(input_unit)
        other_units = self.unit_groups[str(unit_dimensionality)]
        try:
            default_unit = input_value * UnitsConversion.get_unit(input_unit)

            alternative_unit_values = {
                other_unit: default_unit.to(other_unit).magnitude
                for other_unit in other_units
            }
        except SearchAPIError as e:
            # 400 should be returned because the user's unit cannot be found
            raise FilterError(e)

        return alternative_unit_values

    def change_units_type(self, input_unit, input_value, request_unit):
        pint_value = input_value * UnitsConversion.get_unit(input_unit)
        try:
            request_pint_value = pint_value.to(request_unit)
        except UndefinedUnitError as e:
            raise FilterError(e)

        return request_pint_value.magnitude


def group_units():
    unit_reg = UnitRegistry()
    unit_groups = {}

    for unit in good_isis_units:
        pint_unit = getattr(unit_reg, unit)
        unit_groups.setdefault(str(pint_unit.dimensionality), [])
        unit_groups[str(pint_unit.dimensionality)].append(unit)

    return unit_groups


good_isis_units = [
    "1",
    "C",
    "G",
    "GPa",
    "Hz",
    "K",
    "MM",
    "MPa",
    "MV",
    "N/A",
    "T",
    "W/sr",
    "cc",
    "counts",
    "degree K",
    "degree c",
    "degrees",
    "g",
    "g in 1 mL water",
    "g/cm^3",
    "gauss",
    "kbar",
    "kelvin",
    "l",
    "m",
    "mK",
    "mL",
    "mg",
    "mg/mL",
    "mg/ml",
    "microseconds",
    "ml",
    "ml ",
    "mm",
    "msec",
    "na",
    "picoseconds",
    "rad",
    "sec",
    "seconds",
    "uA h",
    "uAh",
    "units",
    "°C",
    "¿A",
]
