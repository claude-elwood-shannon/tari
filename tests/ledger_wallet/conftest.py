# Ragger configuration for Tari Ledger Wallet tests
# This file includes the default Ragger configuration and fixtures

# This line includes the default Ragger configuration
# It can be modified to suit local needs
from ragger.conftest import configuration

# This line will be interpreted by pytest which will load the code from the
# given modules, in this case ragger.conftest.base_conftest
# This module will define several fixtures, parametrized with the fields of
# configuration.OPTIONAL variable
pytest_plugins = ("ragger.conftest.base_conftest",)
