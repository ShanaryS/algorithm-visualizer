class CppPyLock():
    """Create a context manager for any lock from any source.
    Pass in a thread locking and unlocking function. NOTICE: NO PARENTHESIS.
    Example usage:    with CppPyLock(thread_lock_func, thread_unlock_func):
    Exceptions are not handled.
    """
    
    def __init__(self, thread_lock_func, thread_unlock_func):
        self.thread_lock = thread_lock_func
        self.thread_unlock = thread_unlock_func
    
    def __enter__(self):
        self.thread_lock()

    def __exit__(self, _, __, ___):
        self.thread_unlock()
