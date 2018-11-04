from front import RequestOptions


class TestRequestOptions:
    def test_add_parameter_sets_value_in_params_when_not_set(self):
        opts = RequestOptions()
        opts.add_parameter('q', 'foo')

        assert opts.params == {'q': 'foo'}

    def test_add_parameter_creates_list_when_param_is_set(self):
        opts = RequestOptions(params={'q': 'abc'})
        opts.add_parameter('q', 'foo')

        assert opts.params == {'q': ['abc', 'foo']}
