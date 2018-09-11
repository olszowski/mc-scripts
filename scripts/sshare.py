def get_sshare_output(user):
    command = 'sshare -U {user_id} -l -m -P'
    from terminal import run_command
    return run_command(command, user_id=user)


def get_user_fairshare(sshare_output):
    lines = sshare_output.split('\n')
    import csv
    reader = csv.DictReader(lines, delimiter="|")
    return float(next(reader)['FairShare'])
