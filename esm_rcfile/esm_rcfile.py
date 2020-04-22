"""
=====
Usage
=====

This package contains functions to set, get, and use entries stored in the
esmtoolsrc file.

To use ESM RCFile in a project::

    import esm_rcfile

You can set specific values in the ``~/.esmtoolsrc`` with::

    set_rc_entry(key, value)

For example::

    >>> set_rc_entry("SCOPE_CONFIG", "/pf/a/a270077/Code/scope/configs/")

Retriving an entry::

    >>> fpath = get_rc_entry("FUNCTION_PATH")
    >>> print(fpath)
    /pf/a/a270077/Code/esm_tools/esm_tools/configs

With a default value for a non-existing key::

    >>> scope_config = get_rc_entry("SCOPE_CONFIG", "/dev/null")
    >>> print(scope_config)
    /dev/null

Without a default value, you get ``EsmRcfileError``::

    >>> echam_namelist = get_rc_entry("ECHAM_NMLDIR")
    EsmRcFileError: No value for ECHAM_NMLDIR found in esmtoolsrc file!!

This error is also raised if there is no ``~/.esmtoolsrc`` file, and no default
is provided.

You can also get the entire rcfile as a dict::

    >>> rcdict = import_rc_file()

"""
import os

rcfile = os.path.expanduser("~") + "/.esmtoolsrc"


class EsmRcfileError(Exception):
    pass


def set_rc_entry(key, value):
    """
    Sets values in ``esmtoolsrc``

    Parameters
    ----------
    key : str
    value : str

    Note
    ----
    Using this functions modifies the ``rcfile``; which is stored in the
    current user's home directory.
    """
    all_lines = [key + "=" + value]

    if os.path.isfile(rcfile):
        with open(rcfile) as rc:
            for line in rc.readlines():
                line = line.strip()
                if not key == line.split("=", 1)[0]:
                    all_lines.append(line)
        os.remove(rcfile)

    with open(rcfile, "w") as rc:
        for line in all_lines:
            rc.write(line + "\n")


def get_rc_entry(key, default=None):
    """
    Gets a specific entry

    Parameters
    ----------
    key : str
    default : str

    Returns
    -------
    str
        Value for key, or default if provided

    Raises
    ------
    EsmRcfileError
        * Raised if key cannot be found in the rcfile and no default is
          provided
        * Raised if the esmtoolsrc file cannot be found and no default is
          provided.
    """
    if os.path.isfile(rcfile):
        with open(rcfile) as rc:
            for line in rc.readlines():
                line = line.strip()
                if line.split("=", 1)[0] == key.upper():
                    return line.split("=", 1)[1]
            if default:
                return default
            else:
                raise EsmRcfileError("No value for %s found in esmtoolsrc file!" % key)
    if default:
        return default
    else:
        raise EsmRcfileError("The file esmtoolsrc file was not found!")


def import_rc_file():
    """
    Gets current values of the esmtoolsrc file

    Returns
    -------
    dict
        A dictionary representation of the rcfile
    """
    if os.path.isfile(rcfile):
        rcdict = {}
        with open(rcfile) as rc:
            for line in rc.readlines():
                line = line.strip()
                rcdict[line.split("=", 1)[0]] = line.split("=", 1)[1]
        return rcdict
    raise EsmRcfileError("The file esmtoolsrc file was not found!")


# PG: Should this be in a if __name__ == "__main__" ?
if os.path.isfile(rcfile):
    FUNCTION_PATH = get_rc_entry("FUNCTION_PATH")
else:
    FUNCTION_PATH = "NONE_YET"
