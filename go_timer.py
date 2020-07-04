import multiprocessing
import os
import pathlib
import shutil
import sys

from gui.bomb_timer_gui import TimerGui
from listener.gamestate_listener import ListenerWrapper

THIS_DIR = os.path.abspath(os.path.dirname(__file__)) if not hasattr(sys, '_MEIPASS') else sys._MEIPASS
CFG_FILE = os.path.join(THIS_DIR, 'listener', 'gamestate_integration_go_timer.cfg')

multiprocessing.freeze_support()

def get_additional_library_paths():
    ''' try to find additional paths that csgo may be installed to '''
    ADD_TO_FIND_CSGO = pathlib.Path('steamapps') / 'common' / 'Counter-Strike Global Offensive'
    ret_list = []
    if os.name == 'nt':
        vdf_paths = (r"C:\Program Files (x86)\Steam\steamapps\libraryfolders.vdf", "C:\Program Files\Steam\steamapps\libraryfolders.vdf")
        for _p in vdf_paths:
            path = pathlib.Path(_p)
            if path.is_file():
                text = path.read_text()

                # look for steam library in vdf file
                for line in text.splitlines():
                    line = line.strip().replace('\t\t', '\t')
                    try:
                        _, _lib_path = line.split('\t')
                    except ValueError as ex:
                        # isn't a line with a thing then a path after tab
                        continue

                    _lib_path = _lib_path.replace("\\", "/").replace("\"", "")
                    lib_path = pathlib.Path(_lib_path)

                    test_csgo_path = lib_path / ADD_TO_FIND_CSGO
                    if test_csgo_path.is_dir():
                        ret_list.append(test_csgo_path)

    return ret_list

def ensure_cfg_file_is_there():
    ret_val = False
    if os.path.isfile(CFG_FILE):
        # todo... if needed find out more csgo locations
        possible_paths = ['~/.steam/steamapps/common/Counter-Strike Global Offensive/',
                            r"C:\Program Files (x86)\Steam\steamapps\common\Counter-Strike Global Offensive",
                            r"C:\Program Files\Steam\steamapps\common\Counter-Strike Global Offensive"] + get_additional_library_paths()

        for p_str in possible_paths:
            p = pathlib.Path(p_str).expanduser()
            if p.is_dir():
                copy_to_path = p / "csgo" / "cfg"
                if copy_to_path.is_file():
                    copy_to_path.unlink()

                shutil.copy(CFG_FILE, copy_to_path)
                print ("Copied %s -> %s" % (CFG_FILE, copy_to_path))
                ret_val = True

    return ret_val

def main():
    if not ensure_cfg_file_is_there():
        print ("Unable to copy cfg. You'll need to do that manually!")

    # Message queue used for comms between processes
    queue = multiprocessing.Queue()
    gui = TimerGui(queue)
    listener = ListenerWrapper(queue)

    gui.start()
    listener.start()

    try:
        gui.join()
        listener.shutdown()
        listener.join()
    except KeyboardInterrupt:
        os._exit(0)

if __name__ == "__main__":
    main()
