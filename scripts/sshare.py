def get_share_info(user):
    command = 'sshare -U {user_id} -l -m -P'
    from terminal import run_command
    output = run_command(command, user_id=user)
    print(output)
