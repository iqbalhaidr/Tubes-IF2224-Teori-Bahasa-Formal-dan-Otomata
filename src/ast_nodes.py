class ProgramNode:
    def __init__(self, name, declarations, block):
        self.name = name
        self.declarations = declarations  
        self.block = block

class BlockNode:
    def __init__(self, statements):
        self.statements = statements


# ============================ DECLARATIONS ============================
class ConstDeclNode:
    def __init__(self, name, value):
        self.name = name
        self.value = value


class VarDeclNode:
    def __init__(self, name, var_type):
        self.names = name
        self.var_type = var_type


class TypeDeclNode:
    def __init__(self, name, type_node):
        self.name = name
        self.type_node = type_node


#  ============================ TYPE ============================
class TypeNode:
    def __init__(self, type_kind, info=None):
        self.type_kind = type_kind   # 'builtin', 'alias', 'array', 'record'
        self.info = info            


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

class FunctionDeclNode:
    def __init__(self, name, params, return_type, declarations, body):
        self.name = name
        self.params = params        
        self.return_type = return_type
        self.declarations = declarations
        self.body = body


#  ============================ STATEMENTS  ============================
class AssignNode:
    def __init__(self, target, value):
        self.target = target
        self.value = value


class ProcedureCallNode:
    def __init__(self, name, args):
        self.name = name
        self.args = args

class FunctionCallNode:
    def __init__(self, name, args):
        self.name = name
        self.args = args


class IfNode:
    def __init__(self, cond, then_stmt, else_stmt=None):
        self.cond = cond
        self.then_stmt = then_stmt
        self.else_stmt = else_stmt


class WhileNode:
    def __init__(self, cond, body):
        self.cond = cond
        self.body = body


class ForNode:
    def __init__(self, var, start, end, descending, body):
        self.var = var
        self.start = start
        self.end = end
        self.descending = descending
        self.body = body


class RepeatNode:
    def __init__(self, body, until):
        self.body = body
        self.until = until


class CaseNode:
    def __init__(self, expr, branches):
        self.expr = expr
        self.branches = branches


class CaseBranchNode:
    def __init__(self, labels, stmt):
        self.labels = labels
        self.stmt = stmt


# -------- EXPRESSIONS --------
class BinOpNode:
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right


class UnaryOpNode:
    def __init__(self, op, expr):
        self.operand = op
        self.expr = expr


class VarNode:
    def __init__(self, name):
        self.name = name


class ArrayAccessNode:
    def __init__(self, var, index):
        self.var = var
        self.index = index


class RecordAccessNode:
    def __init__(self, var, field):
        self.var = var
        self.field = field


class NumberNode:
    def __init__(self, value):
        self.value = value


class StringNode:
    def __init__(self, value):
        self.value = value


class CharNode:
    def __init__(self, value):
        self.value = value


class BooleanNode:
    def __init__(self, value):
        self.value = value
