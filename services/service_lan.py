import sh
import time
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(1)

lan_address: str = ''
lan_play = None
update_timestamp = int(time.time())


def start_lan_play(ip: str):
    print(ip)
    stop_lan_play()
    executor.submit(_start_lan_play, ip)


def stop_lan_play():
    global lan_play, lan_address
    if lan_play is not None:
        lan_play.kill()
        lan_address = ''


def runing():
    global lan_play
    return lan_play is not None


def _start_lan_play(ip):
    global lan_play, lan_address

    r = sh.Command('./packages/lan-play', )
    lan_play = r('--relay-server-addr', ip,
                 _out=_log_out, _err_to_out=True,
                 _bg=True, _done=_done_lan_play,
                 )
    lan_address = ip


def _log_out(line: str):
    global update_timestamp
    print('_log_out', line)
    update_timestamp = int(time.time())


def _log_err(line: str):
    global update_timestamp
    print('_log_err', line)
    update_timestamp = int(time.time())


def _done_lan_play(cmd, success, exit_code):
    global lan_play, lan_address

    print('Close LAN Play')
    lan_play = None
    lan_address = ''
