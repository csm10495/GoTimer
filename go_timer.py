import multiprocessing
import os
import pathlib
import shutil

from gui.bomb_timer_gui import TimerGui
from listener.gamestate_listener import ListenerWrapper

THIS_DIR = os.path.abspath(os.path.dirname(__file__))
CFG_FILE = os.path.join(THIS_DIR, 'listener', 'gamestate_integration_go_timer.cfg')

multiprocessing.freeze_support()

def ensure_cfg_file_is_there():
    if os.path.isfile(CFG_FILE):
        # todo... if needed find out more csgo locations
        possible_paths = ['~/.steam/steamapps/common/Counter-Strike Global Offensive/',
                            r"C:\Program Files (x86)\Steam\steamapps\common\Counter-Strike Global Offensive"]
        for p_str in possible_paths:
            p = pathlib.Path(p_str).expanduser()
            if p.is_dir():
                copy_to_path = p / "csgo" / "cfg"
                if copy_to_path.is_file():
                    copy_to_path.unlink()

                shutil.copy(CFG_FILE, copy_to_path)
                print ("Copied %s -> %s" % (CFG_FILE, copy_to_path))
                return True

    return False

def main():
    if not ensure_cfg_file_is_there():
        print ("Unable to copy cfg. You'll need to do that manually!")

    # Message queue used for comms between processes
    queue = multiprocessing.Queue()
    gui = TimerGui(queue)
    listener = ListenerWrapper(queue)

    gui.start()
    listener.start()

    gui.join()
    listener.shutdown()
    listener.join()

if __name__ == "__main__":
    main()
