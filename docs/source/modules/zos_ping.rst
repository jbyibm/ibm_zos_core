
:github_url: https://github.com/ansible-collections/ibm_zos_core/blob/dev/plugins/modules/zos_ping.py

.. _zos_ping_module:


zos_ping -- Ping z/OS and check dependencies.
=============================================



.. contents::
   :local:
   :depth: 1


Synopsis
--------
- `zos_ping <./zos_ping.html>`_ verifies the presence of z/OS Web Client Enablement Toolkit, iconv, and Python.
- `zos_ping <./zos_ping.html>`_ returns ``pong`` when the target host is not missing any required dependencies.
- If the target host is missing optional dependencies, the `zos_ping <./zos_ping.html>`_ will return one or more warning messages.
- If a required dependency is missing from the target host, an explanatory message will be returned with the module failure.







Examples
--------

.. code-block:: yaml+jinja

   
   - name: Ping the z/OS host and perform resource checks
     zos_ping:
     register: result










Return Values
-------------


ping
  Should contain the value "pong" on success.

  | **returned**: always
  | **type**: str
  | **sample**: pong

warnings
  List of warnings returned from stderr when performing resource checks.

  | **returned**: failure
  | **type**: list
  | **elements**: str

