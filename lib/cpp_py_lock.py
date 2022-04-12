class CppPyLock():
    """Create a context manager for C++ mutex or Python thread lock.
    Pass in a class that has a thread_lock and thread_unlock methods.
    Example usage:    with CppPyLock(exmpale_class):
    """
    def __init__(self, some_class):
        self.some_class = some_class
    
    def __enter__(self):
        self.some_class.thread_lock()

    def __exit__(self, _, __, ___):
        self.some_class.thread_unlock()


"""This version uses explicts functions rather than a class"""
# class CppPyLock():
#     """Create a context manager for C++ mutex or Python thread lock.
#     Example usage:    with CppPyLock(locking_func, unlocking_func):
#     """
    
#     def __init__(self, thread_lock_func, thread_unlock_func):
#         self.thread_lock = thread_lock_func
#         self.thread_unlock = thread_unlock_func
    
#     def __enter__(self):
#         self.thread_lock()

#     def __exit__(self, _, __, ___):
#         self.thread_unlock()
