from parser import *
from ast_nodes import *

class ASTPrinter:
    """Pretty printer for AST nodes"""
    
    def __init__(self, indent_size=2):
        self.indent_size = indent_size
    
    def print(self, node, indent=0):
        """Print AST node with proper indentation"""
        method_name = f"print_{node.__class__.__name__}"
        method = getattr(self, method_name, self.print_generic)
        return method(node, indent)
    
    def _indent(self, level):
        """Generate indentation string"""
        return " " * (level * self.indent_size)
    
    def _print_section(self, label, content, indent):
        """Helper to print a labeled section"""
        lines = [f"{self._indent(indent)}{label}:"]
        if isinstance(content, list):
            if content:
                for item in content:
                    lines.append(self.print(item, indent + 1))
            else:
                lines.append(f"{self._indent(indent + 1)}(empty)")
        else:
            lines.append(self.print(content, indent + 1))
        return lines
    
    def _print_labeled_value(self, label, value, indent):
        """Helper to print a simple labeled value"""
        return [f"{self._indent(indent)}{label}: {value}"]
    
    def print_generic(self, node, indent):
        """Generic printer for unknown node types"""
        return f"{self._indent(indent)}{node.__class__.__name__}: {node}"

    def print_ProgramNode(self, node, indent):
        lines = [f"{self._indent(indent)}Program: {node.name}"]
        
        if node.declarations:
            lines.extend(self._print_section("Declarations", node.declarations, indent + 1))
        
        lines.extend(self._print_section("Body", node.block, indent + 1))
        return "\n".join(lines)
    
    def print_BlockNode(self, node, indent):
        lines = [f"{self._indent(indent)}Block:"]
        if node.statements:
            for stmt in node.statements:
                lines.append(self.print(stmt, indent + 1))
        else:
            lines.append(f"{self._indent(indent + 1)}(empty)")
        return "\n".join(lines)
    
    # ========================= DECLARATIONS =========================
    
    def print_ConstDeclNode(self, node, indent):
        lines = [f"{self._indent(indent)}ConstDecl: {node.name}"]
        lines.extend(self._print_section("Value", node.value, indent + 1))
        return "\n".join(lines)
    
    def print_VarDeclNode(self, node, indent):
        lines = [f"{self._indent(indent)}VarDecl: {node.names}"]
        lines.extend(self._print_section("Type", node.var_type, indent + 1))
        return "\n".join(lines)
    
    def print_TypeDeclNode(self, node, indent):
        lines = [f"{self._indent(indent)}TypeDecl: {node.name}"]
        lines.extend(self._print_section("Definition", node.type_node, indent + 1))
        return "\n".join(lines)
    
    # ========================= TYPE NODES =========================
    
    def print_BuiltinTypeNode(self, node, indent):
        return f"{self._indent(indent)}BuiltinType: {node.info}"
    
    def print_CustomTypeNode(self, node, indent):
        return f"{self._indent(indent)}CustomType: {node.info}"
    
    def print_ArrayTypeNode(self, node, indent):
        lines = [f"{self._indent(indent)}ArrayType: [{node.info['low'].value}..{node.info['high'].value}]"]
        lines.extend(self._print_section("ElementType", node.info["element_type"], indent + 1))
        return "\n".join(lines)
    
    def print_RecordTypeNode(self, node, indent):
        lines = [f"{self._indent(indent)}RecordType:"]
        if node.info:
            for name, type_node in node.info:
                lines.append(f"{self._indent(indent + 1)}{name}:")
                lines.append(self.print(type_node, indent + 2))
        else:
            lines.append(f"{self._indent(indent + 1)}(no fields)")
        return "\n".join(lines)
    
    # ============================ STATEMENTS  ============================

    def print_AssignNode(self, node, indent):
        lines = [f"{self._indent(indent)}Assignment:"]
        lines.extend(self._print_section("Target", node.target, indent + 1))
        lines.extend(self._print_section("Value", node.value, indent + 1))
        return "\n".join(lines)
    
    def print_IfNode(self, node, indent):
        lines = [f"{self._indent(indent)}If:"]
        lines.extend(self._print_section("Condition", node.cond, indent + 1))
        lines.extend(self._print_section("Then", node.then_stmt, indent + 1))
        
        if node.else_stmt:
            lines.extend(self._print_section("Else", node.else_stmt, indent + 1))
        
        return "\n".join(lines)
    
    def print_WhileNode(self, node, indent):
        lines = [f"{self._indent(indent)}While:"]
        lines.extend(self._print_section("Condition", node.cond, indent + 1))
        lines.extend(self._print_section("Body", node.body, indent + 1))
        return "\n".join(lines)
    
    def print_ForNode(self, node, indent):
        lines = [f"{self._indent(indent)}For: {node.var}"]
        lines.extend(self._print_section("Start", node.start, indent + 1))
        lines.extend(self._print_labeled_value("Direction", node.descending, indent + 1))
        lines.extend(self._print_section("End", node.end, indent + 1))
        lines.extend(self._print_section("Body", node.body, indent + 1))
        return "\n".join(lines)
    
    def print_RepeatNode(self, node, indent):
        lines = [f"{self._indent(indent)}Repeat:"]
        lines.extend(self._print_section("Statements", node.body or [], indent + 1))
        lines.extend(self._print_section("Until", node.until, indent + 1))
        return "\n".join(lines)
    
    def print_CaseNode(self, node, indent):
        lines = [f"{self._indent(indent)}Case:"]
        lines.extend(self._print_section("Selector", node.expr, indent + 1))
        lines.append(f"{self._indent(indent + 1)}Branches:")
        
        for i, branch in enumerate(node.branches):
            lines.append(f"{self._indent(indent + 2)}Branch {i + 1}:")
            lines.append(f"{self._indent(indent + 3)}Labels:")
            for lbl in branch.labels:
                lines.append(self.print(lbl, indent + 4))
            
            if branch.stmt:
                lines.append(f"{self._indent(indent + 3)}Statement:")
                lines.append(self.print(branch.stmt, indent + 4))
            else:
                lines.append(f"{self._indent(indent + 3)}(no statement)")
        
        return "\n".join(lines)
    
    def _print_call_node(self, kind, name, args, indent):
        """Helper to print procedure/function calls"""
        lines = [f"{self._indent(indent)}{kind}: {name}"]
        
        if args:
            lines.append(f"{self._indent(indent + 1)}Arguments:")
            args_list = args if isinstance(args, list) else [args]
            for arg in args_list:
                lines.append(self.print(arg, indent + 2))
        else:
            lines.append(f"{self._indent(indent + 1)}(no arguments)")
        
        return "\n".join(lines)
    
    def print_ProcedureCallNode(self, node, indent):
        return self._print_call_node("ProcedureCall", node.name, node.args, indent)
    
    def print_FunctionCallNode(self, node, indent):
        return self._print_call_node("FunctionCall", node.name, node.args, indent)
    
    def _print_subprogram(self, kind, name, params, return_type, declarations, body, indent):
        """Helper to print procedure/function declarations"""
        lines = [f"{self._indent(indent)}{kind}: {name}"]
        
        if params:
            lines.append(f"{self._indent(indent + 1)}Parameters:")
            for pname, ptype in params:
                lines.append(f"{self._indent(indent + 2)}{pname}:")
                lines.append(self.print(ptype, indent + 3))
        else:
            lines.append(f"{self._indent(indent + 1)}Parameters: (none)")
        
        if return_type is not None:
            lines.extend(self._print_section("Return Type", return_type, indent + 1))
        
        if declarations:
            lines.extend(self._print_section("Declarations", declarations, indent + 1))
        else:
            lines.append(f"{self._indent(indent + 1)}Declarations: (none)")
        
        lines.extend(self._print_section("Body", body, indent + 1))
        
        return "\n".join(lines)
    
    def print_ProcedureDeclNode(self, node, indent):
        return self._print_subprogram(
            "Procedure", node.name, node.params, None,
            node.declarations, node.body, indent
        )
    
    def print_FunctionDeclNode(self, node, indent):
        return self._print_subprogram(
            "Function", node.name, node.params, node.return_type,
            node.declarations, node.body, indent
        )

    
    def print_BinOpNode(self, node, indent):
        lines = [f"{self._indent(indent)}BinOp: {node.op}"]
        lines.extend(self._print_section("Left", node.left, indent + 1))
        lines.extend(self._print_section("Right", node.right, indent + 1))
        return "\n".join(lines)
    
    def print_UnaryOpNode(self, node, indent):
        lines = [f"{self._indent(indent)}UnaryOp: {node.operand}"]
        lines.extend(self._print_section("Operand", node.expr, indent + 1))
        return "\n".join(lines)
    
    def print_NumberNode(self, node, indent):
        return f"{self._indent(indent)}Number: {node.value}"
    
    def print_StringNode(self, node, indent):
        return f"{self._indent(indent)}String: {node.value}"
    
    def print_CharNode(self, node, indent):
        return f"{self._indent(indent)}Char: {node.value}"
    
    def print_BooleanNode(self, node, indent):
        return f"{self._indent(indent)}Boolean: {node.value}"
    
    def print_VarNode(self, node, indent):
        return f"{self._indent(indent)}Variable: {node.name}"
    
    def _print_access_node(self, kind, var, extra_info, indent):
        """Helper to print array/record access nodes"""
        lines = [f"{self._indent(indent)}{kind}:"]
        lines.extend(self._print_section("Variable", var, indent + 1))
        lines.extend(extra_info)
        return "\n".join(lines)
    
    def print_ArrayAccessNode(self, node, indent):
        extra = self._print_section("Index", node.index, indent + 1)
        return self._print_access_node("ArrayAccess", node.var, extra, indent)
    
    def print_RecordAccessNode(self, node, indent):
        extra = self._print_labeled_value("Field", node.field, indent + 1)
        return self._print_access_node("RecordAccess", node.var, extra, indent)


def print_ast(ast_root, indent_size=2):
    printer = ASTPrinter(indent_size)
    print(printer.print(ast_root))