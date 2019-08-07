Introduction
============

.. image:: https://readthedocs.org/projects/circuitpython-ifttt/badge/?version=latest
    :target: https://circuitpython-ifttt.readthedocs.io/
    :alt: Documentation Status

.. image:: https://img.shields.io/discord/327254708534116352.svg
    :target: https://discord.gg/nBQh6qu
    :alt: Discord

.. image:: https://travis-ci.com/benevip/CircuitPython_ifttt.svg?branch=master
    :target: https://travis-ci.com/benevip/CircuitPython_ifttt
    :alt: Build Status

A simple link to If This Then That (IFTTT) webhooks


Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://github.com/adafruit/Adafruit_CircuitPython_Bundle>`_.

Installing from PyPI
=====================
.. note:: This library is not available on PyPI yet. Install documentation is included
   as a standard element. Stay tuned for PyPI availability!

.. todo:: Remove the above note if PyPI version is/will be available at time of release.
   If the library is not planned for PyPI, remove the entire 'Installing from PyPI' section.

On supported GNU/Linux systems like the Raspberry Pi, you can install the driver locally `from
PyPI <https://pypi.org/project/adafruit-circuitpython-ifttt/>`_. To install for current user:

.. code-block:: shell

    pip3 install adafruit-circuitpython-ifttt

To install system-wide (this may be required in some cases):

.. code-block:: shell

    sudo pip3 install adafruit-circuitpython-ifttt

To install in a virtual environment in your current project:

.. code-block:: shell

    mkdir project-name && cd project-name
    python3 -m venv .env
    source .env/bin/activate
    pip3 install adafruit-circuitpython-ifttt

Usage Example
=============

Sending an event with a value1 of 'touchy touchy' when a PyPortal is touched:

The event name (circuitpylink in the below example) has to match what you have setup in IFTTT, and value1, value2 and value3 are varibles that you can pass through your IFTTT app.

.. code-block:: python
	import time
	import board
	import busio
	from digitalio import DigitalInOut
	import neopixel
	from adafruit_esp32spi import adafruit_esp32spi
	from adafruit_esp32spi import adafruit_esp32spi_wifimanager
	import adafruit_touchscreen
	import ifttt

	#setup touchscreen
	ts = adafruit_touchscreen.Touchscreen(board.TOUCH_XL, board.TOUCH_XR,
										  board.TOUCH_YD, board.TOUCH_YU,
										  calibration=((7000,59000),(8700,55000)),
										  size=(320,240))
	 
	# Get wifi details and more from a secrets.py file
	try:
		from secrets import secrets
	except ImportError:
		print("WiFi secrets are kept in secrets.py, please add them there!")
		raise

	esp32_cs = DigitalInOut(board.ESP_CS)
	esp32_ready = DigitalInOut(board.ESP_BUSY)
	esp32_reset = DigitalInOut(board.ESP_RESET)
	spi = busio.SPI(board.SCK, board.MOSI, board.MISO) 

	esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)

	#comment out if no neopixel
	status_light = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.2) # Uncomment for Most Boards

	wifi = adafruit_esp32spi_wifimanager.ESPSPI_WiFiManager(esp, secrets, status_light)
	 
	print("ready")
		
	while True:
		p=ts.touch_point
		if p:
			print("touched")
			ifttt.send_message(wifi, secrets, "circuitpylink", debug=True, value1="touchy touchy updated")
			time.sleep(10)

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/benevip/CircuitPython_ifttt/blob/master/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.

Sphinx documentation
-----------------------

Sphinx is used to build the documentation based on rST files and comments in the code. First,
install dependencies (feel free to reuse the virtual environment from above):

.. code-block:: shell

    python3 -m venv .env
    source .env/bin/activate
    pip install Sphinx sphinx-rtd-theme

Now, once you have the virtual environment activated:

.. code-block:: shell

    cd docs
    sphinx-build -E -W -b html . _build/html

This will output the documentation to ``docs/_build/html``. Open the index.html in your browser to
view them. It will also (due to -W) error out on any warning like Travis will. This is a good way to
locally verify it will pass.
