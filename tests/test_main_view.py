import json
from unittest.mock import Mock

import pytest

from currency.views import main


@pytest.mark.django_db
def test_main_view():
    response = main(Mock())
    assert response.status_code == 200
