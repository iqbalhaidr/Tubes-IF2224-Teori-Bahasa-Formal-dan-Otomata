class ProgramNode:
    def __init__(self, name, declarations, block):
        self.name = name
        self.declarations = declarations  
        self.block = block
        self.id = None
        self.type = None
        self.lev = None

class BlockNode:
    def __init__(self, statements):
        self.statements = statements
        self.id = None
        self.type = None
        self.lev = None

# ============================ DECLARATIONS ============================
class ConstDeclNode:
    def __init__(self, name, value):
        self.name = name
        self.value = value
        self.id = None
        self.type = None
        self.lev = None


class VarDeclNode:
    def __init__(self, name, var_type, is_var):
        self.names = name
        self.var_type = var_type
        self.is_var = is_var    # True jika ada keyword 'var' (pass-by-reference)
        self.id = None
        self.type = None
        self.lev = None


class TypeDeclNode:
    def __init__(self, name, type_node):
        self.name = name
        self.type_node = type_node
        self.id = None
        self.type = None
        self.lev = None


#  ============================ TYPE ============================
class TypeNode:
    def __init__(self, type_kind, info=None):
        self.type_kind = type_kind   # 'builtin', 'alias', 'array', 'record'
        self.info = info
        self.id = None
        self.type = None
        self.lev = None            


class BuiltinTypeNode(TypeNode):
    def __init__(self, name):
        super().__init__("builtin", name)


class CustomTypeNode(TypeNode):
    def __init__(self, name):
        super().__init__("alias", name)


class ArrayTypeNode(TypeNode):
    def __init__(self, low, high, element_type):
        super().__init__("array", {
            "low": low,
            "high": high,
            "element_type": element_type
        })


class RecordTypeNode(TypeNode):
    def __init__(self, fields):
        # fields = list of (name, type_node)
        super().__init__("record", fields)


#  ============================ SUBPROGRAMS  ============================
class ProcedureDeclNode:
    def __init__(self, name, params, declarations, body):
        self.name = name
        self.params = params        # list of VarDeclNode
        self.declarations = declarations
        self.body = body
        self.id = None
        self.type = None
        self.lev = None

class FunctionDeclNode:
    def __init__(self, name, params, return_type, declarations, body):
        self.name = name
        self.params = params        
        self.return_type = return_type
        self.declarations = declarations
        self.body = body
        self.id = None
        self.type = None
        self.lev = None


#  ============================ STATEMENTS  ============================
class AssignNode:
    def __init__(self, target, value):
        self.target = target
        self.value = value
        self.id = None
        self.type = None
        self.lev = None


class ProcedureCallNode:
    def __init__(self, name, args):
        self.name = name
        self.args = args
        self.id = None
        self.type = None
        self.lev = None

class FunctionCallNode:
    def __init__(self, name, args):
        self.name = name
        self.args = args
        self.id = None
        self.type = None
        self.lev = None


class IfNode:
    def __init__(self, cond, then_stmt, else_stmt=None):
        self.cond = cond
        self.then_stmt = then_stmt
        self.else_stmt = else_stmt
        self.id = None
        self.type = None
        self.lev = None


class WhileNode:
    def __init__(self, cond, body):
        self.cond = cond
        self.body = body
        self.id = None
        self.type = None
        self.lev = None


class ForNode:
    def __init__(self, var, start, end, descending, body):
        self.var = var
        self.start = start
        self.end = end
        self.descending = descending
        self.body = body
        self.id = None
        self.type = None
        self.lev = None


class RepeatNode:
    def __init__(self, body, until):
        self.body = body
        self.until = until
        self.id = None
        self.type = None
        self.lev = None


class CaseNode:
    def __init__(self, expr, branches):
        self.expr = expr
        self.branches = branches
        self.id = None
        self.type = None
        self.lev = None


class CaseBranchNode:
    def __init__(self, labels, stmt):
        self.labels = labels
        self.stmt = stmt
        self.id = None
        self.type = None
        self.lev = None


# -------- EXPRESSIONS --------
class BinOpNode:
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right
        self.id = None
        self.type = None
        self.lev = None


class UnaryOpNode:
    def __init__(self, op, expr):
        self.operand = op
        self.expr = expr
        self.id = None
        self.type = None
        self.lev = None


class VarNode:
    def __init__(self, name):
        self.name = name
        self.id = None
        self.type = None
        self.lev = None


class ArrayAccessNode:
    def __init__(self, var, index):
        self.var = var
        self.index = index
        self.id = None
        self.type = None
        self.lev = None


class RecordAccessNode:
    def __init__(self, var, field):
        self.var = var
        self.field = field
        self.id = None
        self.type = None
        self.lev = None


class NumberNode:
    def __init__(self, value):
        self.value = value
        self.id = None
        self.type = None
        self.lev = None

    def add_negative(self):
        self.value = -self.value


class StringNode:
    def __init__(self, value):
        self.value = value
        self.id = None
        self.type = None
        self.lev = None


class CharNode:
    def __init__(self, value):
        self.value = value
        self.id = None
        self.type = None
        self.lev = None


class BooleanNode:
    def __init__(self, value):
        self.value = value
        self.id = None
        self.type = None
        self.lev = None
