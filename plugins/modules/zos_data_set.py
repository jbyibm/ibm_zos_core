#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) IBM Corporation 2019, 2020, 2023
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = r"""
module: zos_data_set
version_added: "1.3.0"
short_description: Manage data sets
description:
  - Create, delete and set attributes of data sets.
  - When forcing data set replacement, contents will not be preserved.
author: "Blake Becker (@blakeinate)"
options:
  name:
    description:
      - The name of the data set being managed. (e.g C(USER.TEST))
      - If I(name) is not provided, a randomized data set name will be generated
        with the HLQ matching the module-runners username.
      - Required if I(type=MEMBER) or I(state!=present) and not using I(batch).
    type: str
    required: false
  state:
    description:
      - The final state desired for specified data set.
      - >
        If I(state=absent) and the data set does not exist on the managed node,
        no action taken, module completes successfully with I(changed=False).
      - >
        If I(state=absent) and the data set does exist on the managed node,
        remove the data set, module completes successfully with I(changed=True).
      - >
        If I(state=absent) and I(type=MEMBER) and I(force=True), the data set
        will be opened with I(DISP=SHR) such that the entire data set can be
        accessed by other processes while the specified member is deleted.
      - >
        If I(state=absent) and I(volumes) is provided, and the data set is not
        found in the catalog, the module attempts to perform catalog using supplied
        I(name) and I(volumes). If the attempt to catalog the data set catalog is successful,
        then the data set is removed. Module completes successfully with I(changed=True).
      - >
        If I(state=absent) and I(volumes) is provided, and the data set is not
        found in the catalog, the module attempts to perform catalog using supplied
        I(name) and I(volumes). If the attempt to catalog the data set catalog fails,
        then no action is taken. Module completes successfully with I(changed=False).
      - >
        If I(state=absent) and I(volumes) is provided, and the data set is found in
        the catalog, the module compares the catalog volume attributes to the provided
        I(volumes). If the volume attributes are different, the cataloged data set
        will be uncataloged temporarily while the requested data set be deleted is cataloged.
        The module will catalog the original data set on completion, if the attempts to
        catalog fail, no action is taken. Module completes successfully with I(changed=False).
      - >
        If I(state=present) and the data set does not exist on the managed node,
        create and catalog the data set, module completes successfully with I(changed=True).
      - >
        If I(state=present) and I(replace=True) and the data set is present on
        the managed node the existing data set is deleted, and a new data set is created and cataloged
        with the desired attributes, module completes successfully with I(changed=True).
      - >
        If I(state=present) and I(replace=False) and the data set is present
        on the managed node, no action taken, module completes successfully with I(changed=False).
      - >
        If I(state=present) and I(type=MEMBER) and the member does not exist in the data set,
        create a member formatted to store data, module completes successfully with I(changed=True).
        Note, a PDSE does not allow a mixture of formats such that there is
        executables (program objects) and data. The member created is formatted to store data,
        not an executable.
      - >
        If I(state=cataloged) and I(volumes) is provided and the data set is already cataloged,
        no action taken, module completes successfully with I(changed=False).
      - >
        If I(state=cataloged) and I(volumes) is provided and the data set is not cataloged,
        module attempts to perform catalog using supplied I(name) and I(volumes). If the attempt to
        catalog the data set catalog is successful, module completes successfully with I(changed=True).
      - >
        If I(state=cataloged) and I(volumes) is provided and the data set is not cataloged,
        module attempts to perform catalog using supplied I(name) and I(volumes). If the attempt to
        catalog the data set catalog fails, returns failure with I(changed=False).
      - >
        If I(state=uncataloged) and the data set is not found, no action taken,
        module completes successfully with I(changed=False).
      - >
        If I(state=uncataloged) and the data set is found, the data set is uncataloged,
        module completes successfully with I(changed=True).
    required: false
    type: str
    default: present
    choices:
      - present
      - absent
      - cataloged
      - uncataloged
  type:
    description:
      - The data set type to be used when creating a data set. (e.g C(pdse))
      - C(MEMBER) expects to be used with an existing partitioned data set.
      - Choices are case-insensitive.
    required: false
    type: str
    choices:
      - KSDS
      - ESDS
      - RRDS
      - LDS
      - SEQ
      - PDS
      - PDSE
      - LIBRARY
      - BASIC
      - LARGE
      - MEMBER
      - HFS
      - ZFS
    default: PDS
  space_primary:
    description:
      - The amount of primary space to allocate for the dataset.
      - The unit of space used is set using I(space_type).
    type: int
    required: false
    default: 5
  space_secondary:
    description:
      - The amount of secondary space to allocate for the dataset.
      - The unit of space used is set using I(space_type).
    type: int
    required: false
    default: 3
  space_type:
    description:
      - The unit of measurement to use when defining primary and secondary space.
      - Valid units of size are C(K), C(M), C(G), C(CYL), and C(TRK).
    type: str
    choices:
      - K
      - M
      - G
      - CYL
      - TRK
    required: false
    default: M
  record_format:
    description:
      - The format of the data set. (e.g C(FB))
      - Choices are case-insensitive.
      - When I(type=KSDS), I(type=ESDS), I(type=RRDS), I(type=LDS) or I(type=ZFS)
        then I(record_format=None), these types do not have a default
        I(record_format).
    required: false
    choices:
      - FB
      - VB
      - FBA
      - VBA
      - U
      - F
    type: str
    default: FB
  sms_storage_class:
    description:
      - The storage class for an SMS-managed dataset.
      - Required for SMS-managed datasets that do not match an SMS-rule.
      - Not valid for datasets that are not SMS-managed.
      - Note that all non-linear VSAM datasets are SMS-managed.
    type: str
    required: false
  sms_data_class:
    description:
      - The data class for an SMS-managed dataset.
      - Optional for SMS-managed datasets that do not match an SMS-rule.
      - Not valid for datasets that are not SMS-managed.
      - Note that all non-linear VSAM datasets are SMS-managed.
    type: str
    required: false
  sms_management_class:
    description:
      - The management class for an SMS-managed dataset.
      - Optional for SMS-managed datasets that do not match an SMS-rule.
      - Not valid for datasets that are not SMS-managed.
      - Note that all non-linear VSAM datasets are SMS-managed.
    type: str
    required: false
  record_length:
    description:
      - The length, in bytes, of each record in the data set.
      - For variable data sets, the length must include the 4-byte prefix area.
      - "Defaults vary depending on format: If FB/FBA 80, if VB/VBA 137, if U 0."
    type: int
    required: false
  block_size:
    description:
      - The block size to use for the data set.
    type: int
    required: false
  directory_blocks:
    description:
      - The number of directory blocks to allocate to the data set.
    type: int
    required: false
  key_offset:
    description:
      - The key offset to use when creating a KSDS data set.
      - I(key_offset) is required when I(type=KSDS).
      - I(key_offset) should only be provided when I(type=KSDS)
    type: int
    required: false
  key_length:
    description:
      - The key length to use when creating a KSDS data set.
      - I(key_length) is required when I(type=KSDS).
      - I(key_length) should only be provided when I(type=KSDS)
    type: int
    required: false
  volumes:
    description:
      - >
        If cataloging a data set, I(volumes) specifies the name of the volume(s) where the data set is located.
      - >
        If creating a data set, I(volumes) specifies the volume(s) where the data set should be created.
      - >
        If I(volumes) is provided when I(state=present), and the data set is not found in the catalog,
        L(zos_data_set,./zos_data_set.html) will check the volume table of contents to see if the data set exists.
        If the data set does exist, it will be cataloged.
      - >
        If I(volumes) is provided when I(state=absent) and the data set is not found in the catalog,
        L(zos_data_set,./zos_data_set.html) will check the volume table of contents to see if the data set exists.
        If the data set does exist, it will be cataloged and promptly removed from the system.
      - I(volumes) is required when I(state=cataloged).
      - Accepts a string when using a single volume and a list of strings when using multiple.
    type: raw
    required: false
    aliases:
      - volume
  replace:
    description:
      - When I(replace=True), and I(state=present), existing data set matching I(name) will be replaced.
      - >
        Replacement is performed by deleting the existing data set and creating a new data set with the same name and desired
        attributes. Since the existing data set will be deleted prior to creating
        the new data set, no data set will exist if creation of the new data set fails.
      - If I(replace=True), all data in the original data set will be lost.
    type: bool
    required: false
    default: false
  tmp_hlq:
    description:
      - Override the default high level qualifier (HLQ) for temporary and backup
        datasets.
      - The default HLQ is the Ansible user used to execute the module and if
        that is not available, then the value C(TMPHLQ) is used.
    required: false
    type: str
  force:
    description:
      - Specifies that the data set can be shared with others during a member
        delete operation which results in the data set you are updating to be
        simultaneously updated by others.
      - This is helpful when a data set is being used in a long running process
        such as a started task and you are wanting to delete a member.
      - The I(force=True) option enables sharing of data sets through the
        disposition I(DISP=SHR).
      - The I(force=True) only applies to data set members when I(state=absent)
        and I(type=MEMBER).
    type: bool
    required: false
    default: false
  batch:
    description:
      - Batch can be used to perform operations on multiple data sets in a single module call.
    type: list
    elements: dict
    required: false
    suboptions:
      name:
        description:
          - The name of the data set being managed. (e.g C(USER.TEST))
          - If I(name) is not provided, a randomized data set name will be generated
            with the HLQ matching the module-runners username.
          - Required if I(type=MEMBER) or I(state!=present)
        type: str
        required: false
      state:
        description:
          - The final state desired for specified data set.
          - >
            If I(state=absent) and the data set does not exist on the managed node,
            no action taken, module completes successfully with I(changed=False).
          - >
            If I(state=absent) and the data set does exist on the managed node,
            remove the data set, module completes successfully with I(changed=True).
          - >
            If I(state=absent) and I(type=MEMBER) and I(force=True), the data
            set will be opened with I(DISP=SHR) such that the entire data set
            can be accessed by other processes while the specified member is
            deleted.
          - >
            If I(state=absent) and I(volumes) is provided, and the data set is not
            found in the catalog, the module attempts to perform catalog using supplied
            I(name) and I(volumes). If the attempt to catalog the data set catalog is successful,
            then the data set is removed. Module completes successfully with I(changed=True).
          - >
            If I(state=absent) and I(volumes) is provided, and the data set is not
            found in the catalog, the module attempts to perform catalog using supplied
            I(name) and I(volumes). If the attempt to catalog the data set catalog fails,
            then no action is taken. Module completes successfully with I(changed=False).
          - >
            If I(state=absent) and I(volumes) is provided, and the data set is found in
            the catalog, the module compares the catalog volume attributes to the provided
            I(volumes). If they volume attributes are different, the cataloged data set
            will be uncataloged temporarily while the requested data set be deleted is cataloged.
            The module will catalog the original data set on completion, if the attempts to
            catalog fail, no action is taken. Module completes successfully with I(changed=False).
          - >
            If I(state=present) and the data set does not exist on the managed node,
            create and catalog the data set, module completes successfully with I(changed=True).
          - >
            If I(state=present) and I(replace=True) and the data set is present on
            the managed node the existing data set is deleted, and a new data set is created and cataloged
            with the desired attributes, module completes successfully with I(changed=True).
          - >
            If I(state=present) and I(replace=False) and the data set is present
            on the managed node, no action taken, module completes successfully with I(changed=False).
          - >
            If I(state=present) and I(type=MEMBER) and the member does not exist in the data set,
            create a member formatted to store data, module completes successfully with I(changed=True).
            Note, a PDSE does not allow a mixture of formats such that there is
            executables (program objects) and data. The member created is formatted to store data,
            not an executable.
          - >
            If I(state=cataloged) and I(volumes) is provided and the data set is already cataloged,
            no action taken, module completes successfully with I(changed=False).
          - >
            If I(state=cataloged) and I(volumes) is provided and the data set is not cataloged,
            module attempts to perform catalog using supplied I(name) and I(volumes). If the attempt to
            catalog the data set catalog is successful, module completes successfully with I(changed=True).
          - >
            If I(state=cataloged) and I(volumes) is provided and the data set is not cataloged,
            module attempts to perform catalog using supplied I(name) and I(volumes). If the attempt to
            catalog the data set catalog fails, returns failure with I(changed=False).
          - >
            If I(state=uncataloged) and the data set is not found, no action taken,
            module completes successfully with I(changed=False).
          - >
            If I(state=uncataloged) and the data set is found, the data set is uncataloged,
            module completes successfully with I(changed=True).
        required: false
        type: str
        default: present
        choices:
          - present
          - absent
          - cataloged
          - uncataloged
      type:
        description:
          - The data set type to be used when creating a data set. (e.g C(PDSE))
          - C(MEMBER) expects to be used with an existing partitioned data set.
          - Choices are case-insensitive.
        required: false
        type: str
        choices:
          - KSDS
          - ESDS
          - RRDS
          - LDS
          - SEQ
          - PDS
          - PDSE
          - LIBRARY
          - BASIC
          - LARGE
          - MEMBER
          - HFS
          - ZFS
        default: PDS
      space_primary:
        description:
          - The amount of primary space to allocate for the dataset.
          - The unit of space used is set using I(space_type).
        type: int
        required: false
        default: 5
      space_secondary:
        description:
          - The amount of secondary space to allocate for the dataset.
          - The unit of space used is set using I(space_type).
        type: int
        required: false
        default: 3
      space_type:
        description:
          - The unit of measurement to use when defining primary and secondary space.
          - Valid units of size are C(K), C(M), C(G), C(CYL), and C(TRK).
        type: str
        choices:
          - K
          - M
          - G
          - CYL
          - TRK
        required: false
        default: M
      record_format:
        description:
          - The format of the data set. (e.g C(FB))
          - Choices are case-insensitive.
          - When I(type=KSDS), I(type=ESDS), I(type=RRDS), I(type=LDS) or
            I(type=ZFS) then I(record_format=None), these types do not have a
            default I(record_format).
        required: false
        choices:
          - FB
          - VB
          - FBA
          - VBA
          - U
          - F
        type: str
        default: FB
      sms_storage_class:
        description:
          - The storage class for an SMS-managed dataset.
          - Required for SMS-managed datasets that do not match an SMS-rule.
          - Not valid for datasets that are not SMS-managed.
          - Note that all non-linear VSAM datasets are SMS-managed.
        type: str
        required: false
      sms_data_class:
        description:
          - The data class for an SMS-managed dataset.
          - Optional for SMS-managed datasets that do not match an SMS-rule.
          - Not valid for datasets that are not SMS-managed.
          - Note that all non-linear VSAM datasets are SMS-managed.
        type: str
        required: false
      sms_management_class:
        description:
          - The management class for an SMS-managed dataset.
          - Optional for SMS-managed datasets that do not match an SMS-rule.
          - Not valid for datasets that are not SMS-managed.
          - Note that all non-linear VSAM datasets are SMS-managed.
        type: str
        required: false
      record_length:
        description:
          - The length, in bytes, of each record in the data set.
          - For variable data sets, the length must include the 4-byte prefix area.
          - "Defaults vary depending on format: If FB/FBA 80, if VB/VBA 137, if U 0."
        type: int
        required: false
      block_size:
        description:
          - The block size to use for the data set.
        type: int
        required: false
      directory_blocks:
        description:
          - The number of directory blocks to allocate to the data set.
        type: int
        required: false
      key_offset:
        description:
          - The key offset to use when creating a KSDS data set.
          - I(key_offset) is required when I(type=KSDS).
          - I(key_offset) should only be provided when I(type=KSDS)
        type: int
        required: false
      key_length:
        description:
          - The key length to use when creating a KSDS data set.
          - I(key_length) is required when I(type=KSDS).
          - I(key_length) should only be provided when I(type=KSDS)
        type: int
        required: false
      volumes:
        description:
          - >
            If cataloging a data set, I(volumes) specifies the name of the volume(s) where the data set is located.
          - >
            If creating a data set, I(volumes) specifies the volume(s) where the data set should be created.
          - >
            If I(volumes) is provided when I(state=present), and the data set is not found in the catalog,
            L(zos_data_set,./zos_data_set.html) will check the volume table of contents to see if the data set exists.
            If the data set does exist, it will be cataloged.
          - >
            If I(volumes) is provided when I(state=absent) and the data set is not found in the catalog,
            L(zos_data_set,./zos_data_set.html) will check the volume table of contents to see if the data set exists.
            If the data set does exist, it will be cataloged and promptly removed from the system.
          - I(volumes) is required when I(state=cataloged).
          - Accepts a string when using a single volume and a list of strings when using multiple.
        type: raw
        required: false
        aliases:
          - volume
      replace:
        description:
          - When I(replace=True), and I(state=present), existing data set matching I(name) will be replaced.
          - >
            Replacement is performed by deleting the existing data set and creating a new data set with
            the same name and desired attributes. Since the existing data set will
            be deleted prior to creating the new data set, no data set will exist if creation of the new data set fails.
          - If I(replace=True), all data in the original data set will be lost.
        type: bool
        required: false
        default: false
      force:
        description:
          - Specifies that the data set can be shared with others during a member
            delete operation which results in the data set you are updating to
            be simultaneously updated by others.
          - This is helpful when a data set is being used in a long running
            process such as a started task and you are wanting to delete a
            member.
          - The I(force=True) option enables sharing of data sets through the
            disposition I(DISP=SHR).
          - The I(force=True) only applies to data set members when
            I(state=absent) and I(type=MEMBER).
        type: bool
        required: false
        default: false

"""
EXAMPLES = r"""
- name: Create a sequential data set if it does not exist
  zos_data_set:
    name: someds.name.here
    type: seq
    state: present

- name: Create a PDS data set if it does not exist
  zos_data_set:
    name: someds.name.here
    type: pds
    space_primary: 5
    space_type: M
    record_format: fba
    record_length: 25

- name: Attempt to replace a data set if it exists
  zos_data_set:
    name: someds.name.here
    type: pds
    space_primary: 5
    space_type: M
    record_format: u
    record_length: 25
    replace: yes

- name: Attempt to replace a data set if it exists. If not found in the catalog, check if it is available on volume 222222, and catalog if found.
  zos_data_set:
    name: someds.name.here
    type: pds
    space_primary: 5
    space_type: M
    record_format: u
    record_length: 25
    volumes: "222222"
    replace: yes

- name: Create an ESDS data set if it does not exist
  zos_data_set:
    name: someds.name.here
    type: esds

- name: Create a KSDS data set if it does not exist
  zos_data_set:
    name: someds.name.here
    type: ksds
    key_length: 8
    key_offset: 0

- name: Create an RRDS data set with storage class MYDATA if it does not exist
  zos_data_set:
    name: someds.name.here
    type: rrds
    sms_storage_class: mydata

- name: Delete a data set if it exists
  zos_data_set:
    name: someds.name.here
    state: absent

- name: Delete a data set if it exists. If data set not cataloged, check on volume 222222 for the data set, and then catalog and delete if found.
  zos_data_set:
    name: someds.name.here
    state: absent
    volumes: "222222"

- name: Write a member to an existing PDS; replace if member exists
  zos_data_set:
    name: someds.name.here(mydata)
    type: MEMBER
    replace: yes

- name: Write a member to an existing PDS; do not replace if member exists
  zos_data_set:
    name: someds.name.here(mydata)
    type: MEMBER

- name: Remove a member from an existing PDS
  zos_data_set:
    name: someds.name.here(mydata)
    state: absent
    type: MEMBER

- name: Remove a member from an existing PDS/E by opening with disposition DISP=SHR
  zos_data_set:
    name: someds.name.here(mydata)
    state: absent
    type: MEMBER
    force: yes

- name: Create multiple partitioned data sets and add one or more members to each
  zos_data_set:
    batch:
      - name:  someds.name.here1
        type: PDS
        space_primary: 5
        space_type: M
        record_format: fb
        replace: yes
      - name: someds.name.here1(member1)
        type: MEMBER
      - name: someds.name.here2(member1)
        type: MEMBER
        replace: yes
      - name: someds.name.here2(member2)
        type: MEMBER

- name: Catalog a data set present on volume 222222 if it is uncataloged.
  zos_data_set:
    name: someds.name.here
    state: cataloged
    volumes: "222222"

- name: Uncatalog a data set if it is cataloged.
  zos_data_set:
    name: someds.name.here
    state: uncataloged

- name: Create a data set on volumes 000000 and 222222 if it does not exist.
  zos_data_set:
    name: someds.name.here
    state: present
    volumes:
      - "000000"
      - "222222"
"""
RETURN = r"""
names:
  description: The data set names, including temporary generated data set names, in the order provided to the module.
  returned: always
  type: list
  elements: str
"""

from ansible_collections.ibm.ibm_zos_core.plugins.module_utils.better_arg_parser import (
    BetterArgParser,
)
from ansible_collections.ibm.ibm_zos_core.plugins.module_utils.data_set import DataSet
from ansible.module_utils.basic import AnsibleModule

import re

# CONSTANTS
DATA_SET_TYPES = [
    "KSDS",
    "ESDS",
    "RRDS",
    "LDS",
    "SEQ",
    "PDS",
    "PDSE",
    "BASIC",
    "LARGE",
    "LIBRARY",
    "MEMBER",
    "HFS",
    "ZFS",
]

DATA_SET_FORMATS = [
    "FB",
    "VB",
    "FBA",
    "VBA",
    "U",
    "F",
]

DEFAULT_RECORD_LENGTHS = {
    "FB": 80,
    "FBA": 80,
    "VB": 137,
    "VBA": 137,
    "U": 0,
}

DATA_SET_TYPES_VSAM = [
    "KSDS",
    "ESDS",
    "RRDS",
    "LDS",
    "ZFS",
]

# ------------- Functions to validate arguments ------------- #


def get_individual_data_set_parameters(params):
    """Builds a list of data set parameters
    to be used in future operations.

    Arguments:
        params {dict} -- The parameters from
        Ansible's AnsibleModule object module.params.

    Raises:
        ValueError: Raised if top-level parameters "name"
        and "batch" are both provided.
        ValueError: Raised if neither top-level parameters "name"
        or "batch" are provided.

    Returns:
        [list] -- A list of dicts where each list item
        represents one data set. Each dictionary holds the parameters
        (passed to the zos_data_set module) for the data set which it represents.
    """
    if params.get("name") and params.get("batch"):
        raise ValueError(
            'Top-level parameters "name" and "batch" are mutually exclusive.'
        )
    elif not params.get("name") and not params.get("batch"):
        raise ValueError(
            'One of the following parameters is required: "name", "batch".'
        )
    if params.get("name"):
        data_sets_parameter_list = [params]
    else:
        data_sets_parameter_list = params.get("batch")
    return data_sets_parameter_list


# * can be replaced by built-in
def data_set_name(contents, dependencies):
    """Validates provided data set name(s) are valid.
    Returns a list containing the name(s) of data sets."""
    if dependencies.get("batch"):
        return None
    if contents is None:
        if dependencies.get("state") != "present":
            raise ValueError('Data set name must be provided when "state!=present"')
        if dependencies.get("type") != "MEMBER":
            tmphlq = dependencies.get("tmp_hlq")
            if tmphlq is None:
                tmphlq = ""
            contents = DataSet.temp_name(tmphlq)
        else:
            raise ValueError(
                'Data set and member name must be provided when "type=MEMBER"'
            )
    dsname = str(contents)
    if not re.fullmatch(
        r"^(?:(?:[A-Z$#@]{1}[A-Z0-9$#@-]{0,7})(?:[.]{1})){1,21}[A-Z$#@]{1}[A-Z0-9$#@-]{0,7}$",
        dsname,
        re.IGNORECASE,
    ):
        if not (
            re.fullmatch(
                r"^(?:(?:[A-Z$#@]{1}[A-Z0-9$#@-]{0,7})(?:[.]{1})){1,21}[A-Z$#@]{1}[A-Z0-9$#@-]{0,7}(?:\([A-Z$#@]{1}[A-Z0-9$#@]{0,7}\)){0,1}$",
                dsname,
                re.IGNORECASE,
            )
            and dependencies.get("type") == "MEMBER"
        ):
            raise ValueError(
                "Value {0} is invalid for data set argument.".format(dsname)
            )
    return dsname.upper()


# * dependent on state
def space_type(contents, dependencies):
    """Validates provided data set unit of space is valid.
    Returns the unit of space."""
    if dependencies.get("state") == "absent":
        return None
    if contents is None:
        return None
    match = re.fullmatch(r"(M|G|K|TRK|CYL)", contents, re.IGNORECASE)
    if not match:
        raise ValueError(
            'Value {0} is invalid for space_type argument. Valid space types are "K", "M", "G", "TRK" or "CYL".'.format(
                contents
            )
        )
    return contents


# * dependent on state
def sms_class(contents, dependencies):
    """Validates provided sms class is of valid length.
    Returns the sms class."""
    if dependencies.get("state") == "absent" or contents is None:
        return None
    if len(contents) < 1 or len(contents) > 8:
        raise ValueError(
            (
                "Value {0} is invalid for an SMS class argument. "
                "SMS class must be at least 1 and at most 8 characters."
            ).format(contents)
        )
    return contents


def valid_when_state_present(contents, dependencies):
    """Ensures no arguments that are invalid when state!=present
    are allowed."""
    if dependencies.get("state") == "absent" or contents is None:
        return None
    return contents


# * dependent on state
# * dependent on format
def record_length(contents, dependencies):
    """Validates provided record length is valid.
    Returns the record length as integer."""
    if dependencies.get("state") == "absent":
        return None
    contents = (
        DEFAULT_RECORD_LENGTHS.get(dependencies.get("record_format"), None)
        if contents is None
        else int(contents)
    )
    if contents is None:
        return None
    if not re.fullmatch(r"[0-9]*", str(contents)) or (contents < 0 or contents > 32768):
        raise ValueError(
            "Value {0} is invalid for record_length argument. record_length must be between 0 and 32768 bytes.".format(
                contents
            )
        )
    return contents


# * dependent on state
# * dependent on record_length
def record_format(contents, dependencies):
    """Validates data set format is valid.
    Returns uppercase data set format."""
    if dependencies.get("state") == "absent":
        return None
    if contents is None:
        return None
    formats = "|".join(DATA_SET_FORMATS)
    if not re.fullmatch(formats, contents, re.IGNORECASE):
        raise ValueError(
            "Value {0} is invalid for format argument. format must be of of the following: {1}.".format(
                contents, ", ".join(DATA_SET_FORMATS)
            )
        )
    return contents.upper()


# * dependent on state
def data_set_type(contents, dependencies):
    """Validates data set type is valid.
    Returns uppercase data set type."""
    # if dependencies.get("state") == "absent" and contents != "MEMBER":
    #     return None
    if contents is None:
        return "PDS"
    types = "|".join(DATA_SET_TYPES)
    if not re.fullmatch(types, contents, re.IGNORECASE):
        raise ValueError(
            "Value {0} is invalid for type argument. type must be of of the following: {1}.".format(
                contents, ", ".join(DATA_SET_TYPES)
            )
        )
    return contents.upper()


# * dependent on state
def volumes(contents, dependencies):
    """Validates volume is valid.
    Returns uppercase volume."""
    if contents is None:
        if dependencies.get("state") == "cataloged":
            raise ValueError("Volume is required when state==cataloged.")
        return None
    if not isinstance(contents, list):
        contents = [contents]
    for vol in contents:
        if not re.fullmatch(
            r"^[A-Z0-9]{1,6}$",
            str(vol),
            re.IGNORECASE,
        ):
            raise ValueError(
                'Invalid argument type for "{0}". expected volume name'.format(vol)
            )
        vol = vol.upper()
    return contents


# * dependent on state
# * dependent on type
def key_length(contents, dependencies):
    """Validates data set key length is valid.
    Returns data set key length as integer."""
    if dependencies.get("state") == "absent":
        return None
    if dependencies.get("type") == "KSDS" and contents is None:
        raise ValueError("key_length is required when requesting KSDS data set.")
    if dependencies.get("type") != "KSDS" and contents is not None:
        raise ValueError("key_length is only valid when type=KSDS.")
    if contents is None:
        return None
    contents = int(contents)
    if not re.match(r"[0-9]+", str(contents)):
        raise ValueError(
            "Value {0} is invalid for key_length argument.".format(contents)
        )
    return contents


# * dependent on state
# * dependent on type
# * dependent on key_length
def key_offset(contents, dependencies):
    """Validates data set key offset is valid.
    Returns data set key offset as integer."""
    if dependencies.get("state") == "absent":
        return None
    if dependencies.get("type") == "KSDS" and contents is None:
        raise ValueError("key_offset is required when requesting KSDS data set.")
    if dependencies.get("type") != "KSDS" and contents is not None:
        raise ValueError("key_offset is only valid when type=KSDS.")
    if contents is None:
        return None
    contents = int(contents)
    if not re.match(r"[0-9]+", str(contents)):
        raise ValueError(
            "Value {0} is invalid for key_offset argument. offset must be between 0 and length of object - 1.".format(
                contents
            )
        )
    return contents


def perform_data_set_operations(name, state, **extra_args):
    """Calls functions to perform desired operations on
    one or more data sets. Returns boolean indicating if changes were made."""
    changed = False
    #  passing in **extra_args forced me to modify the acceptable parameters
    #  for multiple functions in data_set.py including ensure_present, replace
    #  and create where the force parameter has no bearing.
    if state == "present" and extra_args.get("type") != "MEMBER":
        changed = DataSet.ensure_present(name, **extra_args)
    elif state == "present" and extra_args.get("type") == "MEMBER":
        changed = DataSet.ensure_member_present(name, extra_args.get("replace"))
    elif state == "absent" and extra_args.get("type") != "MEMBER":
        changed = DataSet.ensure_absent(name, extra_args.get("volumes"))
    elif state == "absent" and extra_args.get("type") == "MEMBER":
        changed = DataSet.ensure_member_absent(name, extra_args.get("force"))
    elif state == "cataloged":
        changed = DataSet.ensure_cataloged(name, extra_args.get("volumes"))
    elif state == "uncataloged":
        changed = DataSet.ensure_uncataloged(name)
    return changed


def fix_old_size_arg(params):
    """ for backwards compatibility with old styled size argument """
    match = None
    if params.get("size"):
        match = re.fullmatch(
            r"([1-9][0-9]*)(M|G|K|TRK|CYL)", str(params.get("size")), re.IGNORECASE
        )
        if not match:
            raise ValueError(
                'Value {0} is invalid for size argument. Valid size measurements are "K", "M", "G", "TRK" or "CYL".'.format(
                    str(params.get("size"))
                )
            )
    if params.get("space_primary"):
        match = re.fullmatch(
            r"([1-9][0-9]*)(M|G|K|TRK|CYL)",
            str(params.get("space_primary")),
            re.IGNORECASE,
        )
    if match:
        params["space_primary"] = int(match.group(1))
        params["space_type"] = match.group(2)
    return params


def parse_and_validate_args(params):
    params = fix_old_size_arg(params)

    arg_defs = dict(
        # Used for batch data set args
        batch=dict(
            type="list",
            elements="dict",
            options=dict(
                name=dict(
                    type=data_set_name,
                    default=data_set_name,
                    dependencies=["type", "state"],
                ),
                state=dict(
                    type="str",
                    default="present",
                    choices=["present", "absent", "cataloged", "uncataloged"],
                ),
                type=dict(type=data_set_type, required=False, dependencies=["state"]),
                space_type=dict(
                    type=space_type, required=False, dependencies=["state"]
                ),
                space_primary=dict(type="int", required=False, dependencies=["state"]),
                space_secondary=dict(
                    type="int", required=False, dependencies=["state"]
                ),
                record_format=dict(
                    type=record_format,
                    required=False,
                    dependencies=["state"],
                    aliases=["format"],
                ),
                sms_management_class=dict(
                    type=sms_class, required=False, dependencies=["state"]
                ),
                # I know this alias is odd, ZOAU used to document they supported
                # SMS data class when they were actually passing as storage class
                # support for backwards compatability with previous module versions
                sms_storage_class=dict(
                    type=sms_class,
                    required=False,
                    dependencies=["state"],
                    aliases=["data_class"],
                ),
                sms_data_class=dict(
                    type=sms_class, required=False, dependencies=["state"]
                ),
                block_size=dict(
                    type=valid_when_state_present,
                    required=False,
                    dependencies=["state"],
                ),
                directory_blocks=dict(
                    type=valid_when_state_present,
                    required=False,
                    dependencies=["state"],
                ),
                record_length=dict(
                    type=record_length,
                    required=False,
                    dependencies=["state", "record_format"],
                ),
                key_offset=dict(
                    type=valid_when_state_present,
                    required=False,
                    dependencies=["state", "type", "key_length"],
                ),
                key_length=dict(
                    type=valid_when_state_present,
                    required=False,
                    dependencies=["state", "type"],
                ),
                replace=dict(
                    type="bool",
                    default=False,
                ),
                volumes=dict(
                    type=volumes,
                    required=False,
                    aliases=["volume"],
                    dependencies=["state"],
                ),
                force=dict(
                    type="bool",
                    required=False,
                    default=False,
                ),
            ),
        ),
        # For individual data set args
        name=dict(
            type=data_set_name,
            default=data_set_name,
            required=False,
            dependencies=["type", "state", "batch", "tmp_hlq"],
        ),
        state=dict(
            type="str",
            default="present",
            choices=["present", "absent", "cataloged", "uncataloged"],
        ),
        type=dict(type=data_set_type, required=False, dependencies=["state"]),
        space_type=dict(type=space_type, required=False, dependencies=["state"]),
        space_primary=dict(type="int", required=False, dependencies=["state"]),
        space_secondary=dict(type="int", required=False, dependencies=["state"]),
        record_format=dict(
            type=record_format,
            required=False,
            dependencies=["state"],
            aliases=["format"],
        ),
        sms_management_class=dict(
            type=sms_class, required=False, dependencies=["state"]
        ),
        # I know this alias is odd, ZOAU used to document they supported
        # SMS data class when they were actually passing as storage class
        # support for backwards compatability with previous module versions
        sms_storage_class=dict(
            type=sms_class,
            required=False,
            dependencies=["state"],
            aliases=["data_class"],
        ),
        sms_data_class=dict(type=sms_class, required=False, dependencies=["state"]),
        block_size=dict(
            type=valid_when_state_present,
            required=False,
            dependencies=["state"],
        ),
        directory_blocks=dict(
            type=valid_when_state_present,
            required=False,
            dependencies=["state"],
        ),
        record_length=dict(
            type=record_length,
            required=False,
            dependencies=["state", "record_format"],
        ),
        key_offset=dict(type=valid_when_state_present, required=False),
        key_length=dict(type=valid_when_state_present, required=False),
        replace=dict(
            type="bool",
            default=False,
        ),
        volumes=dict(
            type=volumes,
            required=False,
            aliases=["volume"],
            dependencies=["state"],
        ),
        tmp_hlq=dict(
            type='qualifier_or_empty',
            required=False,
            default=None
        ),
        force=dict(
            type="bool",
            required=False,
            default=False,
        ),
        mutually_exclusive=[
            ["batch", "name"],
            # ["batch", "state"],
            # ["batch", "space_type"],
            # ["batch", "space_primary"],
            # ["batch", "space_secondary"],
            ["batch", "record_format"],
            ["batch", "sms_management_class"],
            ["batch", "sms_storage_class"],
            ["batch", "sms_data_class"],
            ["batch", "block_size"],
            ["batch", "record_length"],
            ["batch", "key_offset"],
            ["batch", "key_length"],
            # ["batch", "replace"],
            ["batch", "volumes"],
            # ["batch", "force"],
        ],
    )
    parser = BetterArgParser(arg_defs)
    parsed_args = parser.parse_args(params)
    parsed_args = {
        key: value for key, value in parsed_args.items() if value is not None
    }
    return parsed_args


def run_module():
    # TODO: add logic to handle aliases during parsing

    module_args = dict(
        # Used for batch data set args
        batch=dict(
            type="list",
            elements="dict",
            options=dict(
                name=dict(
                    type="str",
                    required=False,
                ),
                state=dict(
                    type="str",
                    default="present",
                    choices=["present", "absent", "cataloged", "uncataloged"],
                ),
                type=dict(type="str", required=False, default="PDS"),
                space_type=dict(type="str", required=False, default="M"),
                space_primary=dict(type="int", required=False, aliases=["size"], default=5),
                space_secondary=dict(type="int", required=False, default=3),
                record_format=dict(type="str", required=False, aliases=["format"], default="FB"),
                sms_management_class=dict(type="str", required=False),
                # I know this alias is odd, ZOAU used to document they supported
                # SMS data class when they were actually passing as storage class
                # support for backwards compatibility with previous module versions
                sms_storage_class=dict(
                    type="str", required=False, aliases=["data_class"]
                ),
                sms_data_class=dict(type="str", required=False),
                block_size=dict(
                    type="int",
                    required=False,
                ),
                directory_blocks=dict(
                    type="int",
                    required=False,
                ),
                record_length=dict(
                    type="int",
                    required=False,
                ),
                key_offset=dict(type="int", required=False, no_log=False),
                key_length=dict(type="int", required=False, no_log=False),
                replace=dict(
                    type="bool",
                    default=False,
                ),
                volumes=dict(type="raw", required=False, aliases=["volume"]),
                force=dict(
                    type="bool",
                    required=False,
                    default=False,
                ),
            ),
        ),
        # For individual data set args
        name=dict(
            type="str",
            required=False,
        ),
        state=dict(
            type="str",
            default="present",
            choices=["present", "absent", "cataloged", "uncataloged"],
        ),
        type=dict(type="str", required=False, default="PDS"),
        space_type=dict(type="str", required=False, default="M"),
        space_primary=dict(type="raw", required=False, aliases=["size"], default=5),
        space_secondary=dict(type="int", required=False, default=3),
        record_format=dict(type="str", required=False, aliases=["format"], default="FB"),
        sms_management_class=dict(type="str", required=False),
        # I know this alias is odd, ZOAU used to document they supported
        # SMS data class when they were actually passing as storage class
        # support for backwards compatability with previous module versions
        sms_storage_class=dict(type="str", required=False, aliases=["data_class"]),
        sms_data_class=dict(type="str", required=False),
        block_size=dict(
            type="int",
            required=False,
        ),
        directory_blocks=dict(
            type="int",
            required=False,
        ),
        record_length=dict(
            type="int",
            required=False,
        ),
        key_offset=dict(type="int", required=False, no_log=False),
        key_length=dict(type="int", required=False, no_log=False),
        replace=dict(
            type="bool",
            default=False,
        ),
        volumes=dict(
            type="raw",
            required=False,
            aliases=["volume"],
        ),
        tmp_hlq=dict(
            type="str",
            required=False,
            default=None
        ),
        force=dict(
            type="bool",
            required=False,
            default=False
        ),
    )
    result = dict(changed=False, message="", names=[])

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    # This evaluation will always occur as a result of the limitation on the
    # better arg parser, this will serve as a solution for now and ensure
    # the non-batch and batch arguments are correctly set
    if module.params.get("batch") is not None:
        for entry in module.params.get("batch"):
            if entry.get('type') is not None and entry.get("type").upper() in DATA_SET_TYPES_VSAM:
                entry["record_format"] = None
        if module.params.get("type") is not None:
            module.params["type"] = None
        if module.params.get("state") is not None:
            module.params["state"] = None
        if module.params.get("space_type") is not None:
            module.params["space_type"] = None
        if module.params.get("space_primary") is not None:
            module.params["space_primary"] = None
        if module.params.get("space_secondary") is not None:
            module.params["space_secondary"] = None
        if module.params.get("replace") is not None:
            module.params["replace"] = None
        if module.params.get("record_format") is not None:
            module.params["record_format"] = None
    elif module.params.get("type") is not None:
        if module.params.get("type").upper() in DATA_SET_TYPES_VSAM:
            # For VSAM types set the value to nothing and let the code manage it
            module.params["record_format"] = None

    if not module.check_mode:
        try:
            # Update the dictionary for use by better arg parser by adding the
            # batch keyword after the arg spec is evaluated else you get a lint
            # error 'invalid-ansiblemodule-schema'
            module_args['state']['dependencies'] = ['batch']
            params = parse_and_validate_args(module.params)
            data_set_param_list = get_individual_data_set_parameters(params)
            result["names"] = [d.get("name", "") for d in data_set_param_list]

            for data_set_params in data_set_param_list:
                # remove unnecessary empty batch argument
                result["changed"] = perform_data_set_operations(
                    **data_set_params
                ) or result.get("changed", False)
        except Exception as e:
            module.fail_json(msg=repr(e), **result)
    else:
        if module.params.get("replace"):
            result["changed"] = True
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
