class TestIdentity:
    def test_identity_name_is_returned(self, api):
        assert api.me().name == "Planet express"

    def test_identity_id_is_returned(self, api):
        assert api.me().id == "cmp_55c8c149"
