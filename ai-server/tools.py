import ast,operator,math
OPS={ast.Add:operator.add,ast.Sub:operator.sub,ast.Mult:operator.mul,ast.Div:operator.truediv,ast.Pow:operator.pow,ast.Mod:operator.mod}
def calculator(expr:str):
 tree=ast.parse(expr,mode="eval")
 def ev(n):
  if isinstance(n,ast.Constant) and isinstance(n.value,(int,float)): return n.value
  if isinstance(n,ast.UnaryOp) and isinstance(n.op,ast.USub): return -ev(n.operand)
  if isinstance(n,ast.BinOp) and type(n.op) in OPS: return OPS[type(n.op)](ev(n.left),ev(n.right))
  if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id in {"sqrt","sin","cos","tan"}: return getattr(math,n.func.id)(ev(n.args[0]))
  raise ValueError("unsupported expression")
 return ev(tree.body)
