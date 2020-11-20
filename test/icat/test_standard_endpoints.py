class TestStandardEndpoints:
    def test_all_endpoints_exist(self):
        pass

    def test_valid_get_with_filters(self):
        pass

    def test_invalid_get_with_filters(self):
        # Invalid data?
        pass

    def test_filters_applied_get_with_filters(self):
        pass

    def test_valid_create_data(self):
        pass

    def test_invalid_create_data(self):
        # Invalid request body
        pass

    def test_invalid_create_data_1(self):
        # TODO - Rename function
        # Target ICATObjectExistsError
        pass

    def test_valid_update_data(self):
        pass

    def test_valid_boundary_update_data(self):
        """ Request body is a dictionary, not a list of dictionaries"""
        pass

    def test_invalid_update_data(self):
        # Exclude an ID at in one of the data pieces
        pass

    def test_valid_get_one_with_filters(self):
        pass

    def test_filters_applied_get_one_with_filters(self):
        # Can't be a limit filter, maybe order desc would be better
        pass

    def test_valid_count_with_filters(self):
        pass

    def test_filters_applied_count_with_filters(self):
        pass

    def test_valid_get_with_id(self):
        pass

    def test_invalid_get_with_id(self):
        # Do a get one with filters (order desc), extract the id of that, add 5 and do a
        # request for that
        pass

    def test_valid_delete_with_id(self):
        pass

    def test_invalid_delete_with_id(self):
        # like invalid get, but try to delete
        pass

    def test_valid_update_with_id(self):
        pass

    def test_invalid_update_with_id(self):
        pass
