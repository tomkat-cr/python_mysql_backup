# src/do_bkp_db.py
# 2023-01-01 | CR
#
import os
import sys
import datetime
import subprocess
from dotenv import load_dotenv


def get_command_line_args():
    params = dict()
    params['config_filename'] = '.env'
    if len(sys.argv) > 1:
        params['config_filename'] = sys.argv[1]
    return params


def get_formatted_date(to_file_format=False):
    if to_file_format:
        date_format = "%Y%m%d_%H%M%S"
    else:
        date_format = "%Y-%m-%d %H:%M:%S"
    formatted_date = datetime.date.strftime(
        datetime.datetime.today(), date_format
    )
    return formatted_date


def get_filespec(database_name, name_suffix, file_extension, directory):
    filename = f'bkp-db-{database_name}' + \
        (f'-{name_suffix}' if name_suffix else '') + \
        f'-{get_formatted_date(True)}' + \
        f'.{file_extension}'
    filespec = os.path.join(directory, filename)
    return filespec


def log_msg(f, msg, returrn_value=True, interline=True):
    if interline:
        print('')
        f.write("\n")
    print(msg)
    f.write(msg+"\n")
    return returrn_value


def execute_and_report(f, cmd_raw):
    success = False,
    cmd = cmd_raw.split()
    print(cmd)
    try:
        temp = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        # get the output as a string
        output = str(temp.communicate())
        # report the output
        log_msg(f, output)
    except OSError as error_message:
        success = log_msg(
            f,
            f'ERROR: on command execution... {str(error_message)}',
            False
        )
    return success


def read_params():
    par = dict()
    par["mysql_user"] = os.getenv('MYSQL_USER', '')
    par["mysql_password"] = os.getenv('MYSQL_PASSWORD', '')
    par["mysql_port"] = os.getenv('MYSQL_PORT', '')
    par["mysql_server"] = os.getenv('MYSQL_SERVER')
    par["mysql_database"] = os.getenv('MYSQL_DATABASE')
    par["backup_path"] = os.getenv('BACKUP_PATH')
    par["name_suffix"] = os.getenv('NAME_SUFFIX', '')
    par["log_file_path"] = os.getenv('LOG_FILE_PATH')
    return par


def perform_backup(f):
    par = read_params()

    log_msg(
        f,
        f'Database Backup Started | DB: {par["mysql_database"]} '
        f'| Name Suffix: {par["name_suffix"]} | {get_formatted_date()}'
    )

    error = False
    # if not par["mysql_user"]:
    #     error = log_msg(f, "User name must be specified")
    if par["mysql_user"] and not par["mysql_password"]:
        error = log_msg(
            f,
            "ERROR: Password must be specified when user is not empty"
        )
    if not par["mysql_server"]:
        error = log_msg(f, "ERROR: Server name must be specified")
    if not par["backup_path"]:
        error = log_msg(f, "ERROR: Backup directory must be specified")
    if error:
        return

    output_path = os.path.join(par["backup_path"], par["mysql_database"])
    if not os.path.exists(output_path):
        try:
            os.mkdir(output_path)
        except OSError as error_message:
            error = log_msg(
                f,
                "ERROR: Output directory could not be create:"
                f"\n{error_message}"
            )
    elif not os.path.isdir(output_path):
        error = log_msg(
            f,
            "ERROR: Output directory exists but is not a directory"
        )
    if error:
        return

    dump_filespec = get_filespec(
        par["mysql_database"], par["name_suffix"], 'sql', output_path
    )
    zip_filespec = get_filespec(
        par["mysql_database"], par["name_suffix"], 'zip', output_path
    )

    log_msg(f, f"Creating Backup: {dump_filespec}")

    mysql_options = ''
    if par["mysql_user"]:
        mysql_options = f'-h{par["mysql_server"]}' + \
            f' --port {par["mysql_port"]}' + \
            f' -u{par["mysql_user"]} -p"{par["mysql_password"]}"' # + \
            # ' --protocol tcp '

    cmd = f'mysqldump {mysql_options} {par["mysql_database"]}' + \
          f' >"{dump_filespec}"'
    print(cmd.replace(par["mysql_password"], '******'))
    os.system(cmd)
    # if not execute_and_report(f, cmd):
    #     return

    log_msg(f, f'Mysqldump successfully finished at {get_formatted_date()}')
    log_msg(f, 'Zipping File:')

    cmd = f'zip "{zip_filespec}" "{dump_filespec}"'
    if not execute_and_report(f, cmd):
        return

    log_msg(
        f,
        f'Zip of mysqldump successfully finished at {get_formatted_date()}'
    )
    log_msg(f, f'Deleting Dump File: {dump_filespec}')

    cmd = f'rm "{dump_filespec}"'
    if not execute_and_report(f, cmd):
        return False

    log_msg(f, 'Backup Completed')
    log_msg(f, 'The backup is in:')
    cmd = f'ls -la "{zip_filespec}"'
    return execute_and_report(f, cmd)


def load_config(params):
    config_filespec = params.get('config_filename', '')
    if config_filespec and not os.path.exists(config_filespec):
        print('ERROR: specified config file {config_filespec} doesn\'t exist')
        return
    load_dotenv(config_filespec)


def main():
    params = get_command_line_args()
    load_config(params)
    par = read_params()

    if not par["mysql_database"]:
        print("ERROR: Database name must be specified")
        return

    log_filespec = get_filespec(
        par["mysql_database"], par["name_suffix"], 'log', par["log_file_path"]
    )

    with open(log_filespec, 'w') as f:
        perform_backup(f)
        log_msg(f, f'The Log file is in: {log_filespec}')
        log_msg(f, f'Backup Completed at {get_formatted_date()}')


if __name__ == '__main__':
    main()
