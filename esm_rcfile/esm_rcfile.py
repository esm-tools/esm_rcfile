"""Functions to set, get, and use entries stored in the esmtoolsrc file."""
import os, sys

rcfile = os.path.expanduser("~") + "/.esmtoolsrc"


def set_rc_entry(key, value):
    """
    Sets values in ``esmtoolsrc``

    Parameters
    ----------
    key : str
    value : str

    Returns
    -------
    None

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


def get_rc_entry(key):
    """
    Gets a specific entry

    Parameters
    ----------
    key : str

    Returns
    -------
    str: Value for key

    Raises
    ------
    KeyError : Raised if key cannot be found in the rcfile
    """
    if os.path.isfile(rcfile):
        with open(rcfile) as rc:
            for line in rc.readlines():
                line = line.strip()
                if line.split("=", 1)[0] == key.upper():
                    return line.split("=", 1)[1]
            raise KeyError("No value for %s found in esmtoolsrc file!" % key)
    print (rcfile + " not found, exiting")
    # PG: Probably a not a good idea to trigger a sys.exit --> what happens if
    # this function is used from a library rather than the command line
    # interface?
    sys.exit(-1)
    # Suggestion:
    raise OSError("The file esmtoolsrc file was not found!")

def import_rc_file():
    """
    Gets current values of the esmtoolsrc file

    Returns
    -------
    dict
    """
    if os.path.isfile(rcfile):
        rcdict = {}
        with open(rcfile) as rc:
            for line in rc.readlines():
                line = line.strip()
                rcdict[line.split("=", 1)[0]] = line.split("=", 1)[1]
        return rcdict
    print (rcfile + " not found, exiting")


# PG: Should this be in a if __name__ == "__main__" ?
if os.path.isfile(rcfile):
    FUNCTION_PATH = get_rc_entry("FUNCTION_PATH")
else:
    FUNCTION_PATH = "NONE_YET"
