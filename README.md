IBM z/OS core collection
========================

The **IBM® z/OS® core collection**, also represented as
**ibm_zos_core** in this document, is  part of the broader
initiative to bring Ansible Automation to IBM Z® through the offering
**Red Hat® Ansible Certified Content for IBM Z®**. The
**IBM z/OS core collection** supports automation tasks such as
creating data sets, submitting jobs, querying jobs, retrieving job output,
encoding data, fetching data sets, copying data sets,
executing operator commands, executing TSO commands, ping,
querying operator actions, APF authorizing libraries,
editing textual data in data sets or Unix System Services files,
finding data sets, backing up and restoring data sets and
volumes, mounting file systems, running z/OS programs without JCL,
initializing volumes, archiving, unarchiving and templating with Jinja.


Red Hat Ansible Certified Content for IBM Z
===========================================

**Red Hat® Ansible Certified Content for IBM Z** provides the ability to
connect IBM Z® to clients' wider enterprise automation strategy through the
Ansible Automation Platform ecosystem. This enables development and operations
automation on Z through a seamless, unified workflow orchestration with
configuration management, provisioning, and application deployment in
one easy-to-use platform.

The **IBM z/OS core collection** is following the
**Red Hat® Ansible Certified Content for IBM Z®** method of distributing
content. Collections will be developed in the open, and when content is ready
for use, it is released to
[Ansible Galaxy](https://galaxy.ansible.com/search?keywords=zos_&order_by=-relevance&deprecated=false&type=collection&page=1)
for community adoption. Once contributors review community usage, feedback,
and are satisfied with the content published, the collection will then be
released to [Ansible Automation Hub](https://www.ansible.com/products/automation-hub)
as **certified** and **IBM supported** for
**Red Hat® Ansible Automation Platform subscribers**.

For guides and reference, please review the [documentation](https://ibm.github.io/z_ansible_collections_doc/index.html).

Features
========
The **IBM z/OS core collection**, includes
[connection plugins](https://ibm.github.io/z_ansible_collections_doc/ibm_zos_core/docs/source/plugins.html#connection),
[action plugins](https://ibm.github.io/z_ansible_collections_doc/ibm_zos_core/docs/source/plugins.html#action),
[modules](https://ibm.github.io/z_ansible_collections_doc/ibm_zos_core/docs/source/modules.html),
[filters](https://ibm.github.io/z_ansible_collections_doc/ibm_zos_core/docs/source/filters.html),
and ansible-doc to automate tasks on z/OS.

Ansible version compatibility
=============================
This collection has been tested against **Ansible** and **Ansible Core** versions >=2.9,<2.16.
The Ansible and Ansible Core versions supported for this collection align to the
[ansible-core support matrix](https://docs.ansible.com/ansible/latest/reference_appendices/release_and_maintenance.html#ansible-core-support-matrix). Review the
[Ansible community changelogs](https://docs.ansible.com/ansible/latest/reference_appendices/release_and_maintenance.html#ansible-community-changelogs) for corresponding **Ansible community packages**
and **ansible-core**.

For **Ansible Automation Platform** (AAP) users, review the
[Ansible Automation Platform Certified Content](https://access.redhat.com/articles/3642632)
and [AAP Life Cycle](https://access.redhat.com/support/policy/updates/ansible-automation-platform)
for more more information on supported versions of Ansible.

Copyright
=========
© Copyright IBM Corporation 2020-2023.

License
=======
Some portions of this collection are licensed under [GNU General Public
License, Version 3.0](https://opensource.org/licenses/GPL-3.0), and
other portions of this collection are licensed under [Apache License,
Version 2.0](http://www.apache.org/licenses/LICENSE-2.0).

See individual files for applicable licenses.