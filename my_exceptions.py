#coding:utf-8
# 用来实现类似goto的功能
# https://stackoverflow.com/questions/438844/is-there-a-label-goto-in-python
# try:
#     while 1:
#         while 1:
#             raise BreakoutException  # Not a real exception, invent your own
# except BreakoutException:
#     pass
class BreakPointException(Exception):
    pass
