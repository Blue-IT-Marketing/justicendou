# !/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import logging


def verify_account(uid: str, access_token: str) -> bool:
    """
        **verify_account**
            verifies user logging
    """
    from accounts import Accounts
    if not uid:
        return False
    if not access_token:
        return False
    account_instance = Accounts.query(Accounts.uid == uid).get()
    return isinstance(account_instance, Accounts) and account_instance.access_token == access_token


def check_firebase(uid, access_token) -> bool:
    pass
