def run_command(command, **kwargs):
    from subprocess import check_output, STDOUT
    from shlex import split
    splitted = split(command.format(**kwargs))
    return check_output(splitted, shell=False, stderr=STDOUT).decode("UTF-8")
