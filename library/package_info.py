from ansible.module_utils.basic import AnsibleModule
# This is the import for asible 2.2.1 to find distribution
# Import that would be used by the devel branch:
# from ansible.module_utils.facts.system.distribution
# The 2.3.1.0-1 release (most recent) still uses this import
from ansible.module_utils.facts import Facts

DOCUMENTATION = """
---
module: package_info.py
short_description: Extracts package info from package DB
description:
  - Extracts package info from package DB
options:
  packages:
    description:
      The list of packages to gather info for
      Must be the exact package name, Not a URL or relative name.
      This is a Required option
  get_release_num:
    description:
      Some OS distributions include their release version after a "-"
      yum will already have this in a different field.
      Set this option to true to include that part of the version number
      Default False
author: ClearObject DevOps (devops@clearobject.com)
"""

EXAMPLES = """
- name: Gather installed package information
  package_info:
    packages:
      - python-libselinux
      - python-ldap
      - screen
    get_release_num: yes
  register: packages
"""


def extract_yum_package_info(module):
    import yum
    packages = module.params['packages']
    yb = yum.YumBase()
    package_details = []
    for package in packages:
        package_obj = yb.rpmdb.searchNevra(name=package)
        if package_obj:
            current = package_obj[0]
            version = current.version

            if module.params['get_release_num']:
                version = version + '-' + current.release

            package_info = {
                "name": current.name,
                "version": version
            }
            package_details.append(package_info)
        else:
            error_msg = ("ERROR! %s is not an installed package "
                         "name on target Machine" % (package))
            module.fail_json(msg=error_msg)

    return package_details


def extract_apt_package_info(module):
    import apt
    packages = module.params['packages']
    # Don't worry about updating cache.
    # Current cache should have the installed packages
    cache = apt.Cache()
    package_details = []
    for package in packages:
        try:
            package_obj = cache[package]
            version = package_obj.installed.version

            # apt leaves the release in the version field.
            if not module.params['get_release_num']:
                version = version.rsplit('-', 1)[0]

            package_info = {
                "name": package_obj.installed.package.name,
                "version": version
            }
            package_details.append(package_info)
        except KeyError:
            error_msg = ("ERROR! %s is not an installed package "
                         "name on target Machine" % (package))
            module.fail_json(msg=error_msg)

    return package_details


def main():
    module = AnsibleModule(
        argument_spec=dict(
            packages=dict(required=True, type='list'),
            get_release_num=dict(type='bool', default=False)
        )
    )
    facts = Facts(module)
    if facts.facts['os_family'] == 'RedHat':
        package_details = extract_yum_package_info(module)

    elif facts.facts['os_family'] == 'Debian':
        package_details = extract_apt_package_info(module)

    else:
        module.fail_json(msg="FAILED! %s is not a supported OS.\n" +
                             "Supported OS families are " +
                             "Debian and RedHat." % (facts.facts['os_family']))

    module.exit_json(results=package_details, changed=False)


if __name__ == '__main__':
    main()
