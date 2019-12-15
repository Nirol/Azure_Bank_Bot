        #!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os

""" Bot Configuration """


class DefaultConfig:
    """ Bot Configuration """

    PORT = 3978
    APP_ID = os.environ.get("MicrosoftAppId", "57fe4078-1209-4080-931d-b3c49f879027")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", ".7Xq[i/?0ZMJh8h41Ftc-tDAs0.08w5G")
    LUIS_APP_ID = os.environ.get("LuisAppId", "df3e2310-8945-4d7b-9b18-b89c1804b44d")
    LUIS_API_KEY = os.environ.get("LuisAPIKey", "2d46d6305d574f508b3d6ba655dde22a")
    # LUIS endpoint host name, ie "westus.api.cognitive.microsoft.com"
    LUIS_API_HOST_NAME = os.environ.get("LuisAPIHostName", "westus.api.cognitive.microsoft.com")
