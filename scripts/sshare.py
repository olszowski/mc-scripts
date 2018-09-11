def get_share_info(user):
    command = 'sshare -U {user} -l -m -P'
    from terminal import run_command
    output = run_command(command, user=user)
    print(output)
