# Proper Tail Recursion

class TailRecursion(Exception):
  def __init__(self, func, func_args, func_kwargs):
    self.func = (func,) # protect bound methods
    self.func_args = func_args
    self.func_kwargs = func_kwargs

def tail_recursive(f):
  def g(*args, **kwargs):
    q = f
    while True:
      try:
        return q(*args, **kwargs)
      except TailRecursion, ex:
        q, args, kwargs = ex.func[0], ex.func_args, ex.func_kwargs
        while getattr(q, 'tail_recursion_wrapped', False):
          # unwrap it; avoid the extra stack frame
          import types
          if type(q) == types.MethodType: # ugh, take care of bound methods
            q = types.MethodType(q.original, q.__self__)
          else:
            q = q.original
  g.original = f
  g.tail_recursion_wrapped = True
  g.__name__ = f.__name__
  g.__doc__ = f.__doc__
  g.__dict__.update(f.__dict__)
  return g

def goto(f, *args, **kwargs):
  raise TailRecursion(f, args, kwargs)

if __name__ == '__main__':
  @tail_recursive
  def count(i):
    if not i % 100000: print i
    goto (count, i + 1)

  count(0)
