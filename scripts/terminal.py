def run_command(command, **kwargs):
    from subprocess import check_output, STDOUT
    from shlex import split
    splitted = command.format(kwargs)
    # command = "sinfo --states='idle,mixed' --partition={partition} --format='%n %P %O %T %C'" \
    #     .format(partition=partition)
    return check_output(split(splitted), shell=False, stderr=STDOUT).decode("UTF-8")
