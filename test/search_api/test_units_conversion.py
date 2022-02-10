class TestUnitsConversion:
    # TODO - mock get_parameter_type_units, put data in conftest
    def test_valid_init(self):
        pass

    def test_valid_get_parameter_type_units(self):
        # No need to mock
        pass

    def test_valid_group_units(self):
        pass

    def test_valid_get_unit(self, test_unit, expected_unit):
        pass

    def test_invalid_get_unit(self, test_unit):
        # Should raise SearchAPIError
        pass

    def test_valid_get_unit_type(self, test_unit, expected_dimensionality):
        pass

    def test_valid_get_alternative_units(
        self, test_unit, test_value, expected_alternatives,
    ):
        pass

    def test_invalid_get_alternative_units(self, test_unit, test_value):
        # should raise FilterError
        pass

    def test_valid_change_units_type(
        self, test_input_unit, test_value, test_requested_unit, expected_value,
    ):
        pass

    def test_invalid_change_units_type(
        self, test_input_unit, test_value, test_requested_unit,
    ):
        # Write this if I put try/except in
        pass
