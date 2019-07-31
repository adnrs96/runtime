# -*- coding: utf-8 -*-
from storyengine.processing.Services import Services
from storyengine.processing.internal.Decorators import Decorators


def test_decorators_create_service(patch):
    patch.object(Services, 'register_internal')

    def my_func():
        pass

    Decorators.create_service('name', 'command', 'arguments',
                              'output_type')(my_func)()

    Services.register_internal.assert_called_with(
        'name', 'command', 'arguments', 'output_type', my_func)
