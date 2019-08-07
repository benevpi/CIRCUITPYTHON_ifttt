# The MIT License (MIT)
#
# Copyright (c) 2019 Ben Everard for HackSpace magazine
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
`ifttt`
================================================================================

A simple link to If This Then That (IFTTT) webhooks


* Author(s): Ben Everard

Implementation Notes
--------------------

**Hardware:**

* Should work with circuit Python boards with ESP32 wifi.
  Tested with a PyPortal -- https://www.adafruit.com/product/4116

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases
"""

# imports

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/benevip/CircuitPython_ifttt.git"

#pylint: disable-msg=too-many-arguments,too-many-branches
def send_message(wifi, secrets, event, debug=False,
                 reset_wifi_on_error=True, value1=None,
                 value2=None, value3=None):
    """sent a message to the IFTTT webhook service"""
    sent = False
    if 'ifttt_key' not in secrets:
        if debug:
            print("you need to add ifttt_key to your secrets file")
        return
    while not sent:
        try:
            if debug:
                print("Posting data")
            payload = {}
            if value1 is not None:
                payload['value1'] = value1
            if value2 is not None:
                payload['value2'] = value2
            if value3 is not None:
                payload['value3'] = value3
            url = "https://maker.ifttt.com/trigger/" + event + "/with/key/" + \
                secrets['ifttt_key']
            if debug:
                print(url)
            response = wifi.post(url, json=payload)
            response.close()
            if debug:
                print("data sent")
            sent = True
        except (ValueError, RuntimeError) as err:
            if debug:
                print("Failed to get data, retrying\n", err)
            if reset_wifi_on_error:
                wifi.reset()
            else:
                sent = True
