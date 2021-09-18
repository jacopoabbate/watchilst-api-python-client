# This file is licensed under the terms of the MIT License.
# See the LICENSE file in the root of this repository
# for complete details.

"""Watchlist API Client Library for Python."""


from watchlist_api_client import config_retriever, config_sender, data_structures, helpers


__version__ = "1.0.0"

__title__ = "watchlist_api_client"
__description__ = "Watchlist API Client Library for Python"

__author__ = "Jacopo Abbate"
__email__ = "jacopo.abbate@peregrinetraders.com"

__license__ = "MIT License"
__coyright__ = "copyright (c) 2020 " + __author__


__all__ = [
    "config_sender",
    "config_retriever",
    "data_structures",
    "helpers",
]
