import os
import time

class AtomicFile(object):
    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode
        self.handle = None

    def __enter__(self):
        self.handle = open(self.filename, self.mode)
        return self.handle

    def __exit__(self, *exc):
        self.handle.close()


class InputAtomicFile(AtomicFile):
    def __init__(self, filename, mode='r', wait_for_file=True, remove_after_reading=True):
        AtomicFile.__init__(self, filename, mode)
        self.wait_for_file = wait_for_file
        self.remove_after_reading = remove_after_reading

    def do_wait_for_file(self):
        while not os.path.exists(self.filename):
            time.sleep(0.1)

    def do_remove_after_reading(self):
        os.unlink(self.filename)

    def __enter__(self):
        if self.wait_for_file:
            self.do_wait_for_file()
        return AtomicFile.__enter__(self)

    def __exit__(self, *exc):
        AtomicFile.__exit__(self, exc)
        if self.remove_after_reading:
            self.do_remove_after_reading()



class OutputAtomicFile(AtomicFile):
    def __init__(self, filename, mode='w'):
        self.real_filename = filename
        tmp_filename = filename + '.tmp'
        AtomicFile.__init__(self, tmp_filename, mode)

    def __enter__(self):
        return AtomicFile.__enter__(self)

    def __exit__(self, *exc):
        AtomicFile.__exit__(self, exc)
        os.rename(self.filename, self.real_filename)
