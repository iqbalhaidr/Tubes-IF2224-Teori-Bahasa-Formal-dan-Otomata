from parser import *
from ast_nodes import *

# Mapping kode tipe ke string agar mudah dibaca manusia
TYPE_MAP = {
    0: 'void', 1: 'integer', 2: 'real', 3: 'boolean', 
    4: 'char', 5: 'larik', 6: 'array', 7: 'string'
}
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
    
    def _get_decoration(self, node):
        """
        [BARU] Mengambil atribut dekorasi (type, idx, lev) dari node
        dan memformatnya menjadi string.
        """
        decorations = []
        
        # 1. Cek Index Symbol Table
        if hasattr(node, 'idx') and node.idx is not None:
            decorations.append(f"index:{node.idx}")

        # 2. Cek Tipe Data
        if hasattr(node, 'type') and node.type is not None:
            t_str = TYPE_MAP.get(node.type, str(node.type))
            decorations.append(f"type:{t_str}")
            
        # 3. Cek Level Scope
        if hasattr(node, 'lev') and node.lev is not None:
            decorations.append(f"lev:{node.lev}")
            
        if decorations:
            # Menggunakan warna Kuning (ANSI code \033[93m) agar mencolok
            return f" \033[93m -> {', '.join(decorations)}\033[0m"
        return ""
    
    def _print_header(self, node, label, indent):
        """
        [BARU] Helper untuk mencetak baris judul node beserta dekorasinya
        """
        deco = self._get_decoration(node)
        return f"{self._indent(indent)}{label}{deco}"

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
        # lines = [f"{self._indent(indent)}Block:"]
        lines = [self._print_header(node, "Block:", indent)]
        if node.statements:
            for stmt in node.statements:
                lines.append(self.print(stmt, indent + 1))
        else:
            lines.append(f"{self._indent(indent + 1)}(empty)")
        return "\n".join(lines)
    
    # ========================= DECLARATIONS =========================
    
    def print_ConstDeclNode(self, node, indent):
        # lines = [f"{self._indent(indent)}ConstDecl: {node.name}"]
        lines = [self._print_header(node, f"ConstDecl: {node.name}", indent)]
        lines.extend(self._print_section("Value", node.value, indent + 1))
        return "\n".join(lines)
    
    def print_VarDeclNode(self, node, indent):
        # lines = [f"{self._indent(indent)}VarDecl: {node.names}"]
        lines = [self._print_header(node, f"VarDecl: {node.names}", indent)]
        lines.extend(self._print_section("Type", node.var_type, indent + 1))
        return "\n".join(lines)
    
    def print_TypeDeclNode(self, node, indent):
        # lines = [f"{self._indent(indent)}TypeDecl: {node.name}"]
        lines = [self._print_header(node, f"TypeDecl: {node.name}", indent)]
        lines.extend(self._print_section("Definition", node.type_node, indent + 1))
        return "\n".join(lines)
    
    # ========================= TYPE NODES =========================
    
    def print_BuiltinTypeNode(self, node, indent):
        # return f"{self._indent(indent)}BuiltinType: {node.info}"
        return self._print_header(node, f"BuiltinType: {node.info}", indent)
    
    def print_CustomTypeNode(self, node, indent):
        # return f"{self._indent(indent)}CustomType: {node.info}"
        return self._print_header(node, f"CustomType: {node.info}", indent)
    
    def print_ArrayTypeNode(self, node, indent):
        # lines = [f"{self._indent(indent)}ArrayType: [{node.info['low'].value}..{node.info['high'].value}]"]
        lines = [self._print_header(node, f"ArrayType: [{node.info['low'].value}..{node.info['high'].value}]", indent)]
        lines.extend(self._print_section("ElementType", node.info["element_type"], indent + 1))
        return "\n".join(lines)
    
    def print_RecordTypeNode(self, node, indent):
        # lines = [f"{self._indent(indent)}RecordType:"]
        lines = [self._print_header(node, "RecordType:", indent)]
        if node.info:
            for name, type_node in node.info:
                lines.append(f"{self._indent(indent + 1)}{name}:")
                lines.append(self.print(type_node, indent + 2))
        else:
            lines.append(f"{self._indent(indent + 1)}(no fields)")
        return "\n".join(lines)
    
    # ============================ STATEMENTS  ============================

    def print_AssignNode(self, node, indent):
        # lines = [f"{self._indent(indent)}Assignment:"]
        lines = [self._print_header(node, "Assignment:", indent)]
        lines.extend(self._print_section("Target", node.target, indent + 1))
        lines.extend(self._print_section("Value", node.value, indent + 1))
        return "\n".join(lines)
    
    def print_IfNode(self, node, indent):
        # lines = [f"{self._indent(indent)}If:"]
        lines = [self._print_header(node, "If:", indent)]
        lines.extend(self._print_section("Condition", node.cond, indent + 1))
        lines.extend(self._print_section("Then", node.then_stmt, indent + 1))
        
        if node.else_stmt:
            lines.extend(self._print_section("Else", node.else_stmt, indent + 1))
        
        return "\n".join(lines)
    
    def print_WhileNode(self, node, indent):
        # lines = [f"{self._indent(indent)}While:"]
        lines = [self._print_header(node, "While:", indent)]
        lines.extend(self._print_section("Condition", node.cond, indent + 1))
        lines.extend(self._print_section("Body", node.body, indent + 1))
        return "\n".join(lines)
    
    def print_ForNode(self, node, indent):
        # lines = [f"{self._indent(indent)}For: {node.var}"]
        lines = [self._print_header(node, f"For: {node.var}", indent)]
        lines.extend(self._print_section("Start", node.start, indent + 1))
        lines.extend(self._print_labeled_value("Direction", node.descending, indent + 1))
        lines.extend(self._print_section("End", node.end, indent + 1))
        lines.extend(self._print_section("Body", node.body, indent + 1))
        return "\n".join(lines)
    
    def print_RepeatNode(self, node, indent):
        # lines = [f"{self._indent(indent)}Repeat:"]
        lines = [self._print_header(node, "Repeat:", indent)]
        lines.extend(self._print_section("Statements", node.body or [], indent + 1))
        lines.extend(self._print_section("Until", node.until, indent + 1))
        return "\n".join(lines)
    
    def print_CaseNode(self, node, indent):
        # lines = [f"{self._indent(indent)}Case:"]
        lines = [self._print_header(node, "Case:", indent)]
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
    
    def _print_call_node(self, kind, name, args, indent, node):
        """Helper to print procedure/function calls"""
        # lines = [f"{self._indent(indent)}{kind}: {name}"]
        lines = [self._print_header(node, f"{kind}: {name}", indent)]
        
        if args:
            lines.append(f"{self._indent(indent + 1)}Arguments:")
            args_list = args if isinstance(args, list) else [args]
            for arg in args_list:
                lines.append(self.print(arg, indent + 2))
        else:
            lines.append(f"{self._indent(indent + 1)}(no arguments)")
        
        return "\n".join(lines)
    
    def print_ProcedureCallNode(self, node, indent):
        return self._print_call_node("ProcedureCall", node.name, node.args, indent, node)
    
    def print_FunctionCallNode(self, node, indent):
        return self._print_call_node("FunctionCall", node.name, node.args, indent, node)
    
    def _print_subprogram(self, kind, name, params, return_type, declarations, body, indent, node):
        """Helper to print procedure/function declarations"""
        # lines = [f"{self._indent(indent)}{kind}: {name}"]
        lines = [self._print_header(node, f"{kind}: {name}", indent)]
        
        if params:
            lines.append(f"{self._indent(indent + 1)}Parameters:")
            for vdn in params: # params ini isinya VarDeclNode
                lines.append(f"{self._indent(indent + 2)}{vdn.names}:")
                lines.append(self.print(vdn.var_type, indent + 3))
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
            node.declarations, node.body, indent, node
        )
    
    def print_FunctionDeclNode(self, node, indent):
        return self._print_subprogram(
            "Function", node.name, node.params, node.return_type,
            node.declarations, node.body, indent, node
        )

    
    def print_BinOpNode(self, node, indent):
        # lines = [f"{self._indent(indent)}BinOp: {node.op}"]
        lines = [self._print_header(node, f"BinOp: {node.op}", indent)]
        lines.extend(self._print_section("Left", node.left, indent + 1))
        lines.extend(self._print_section("Right", node.right, indent + 1))
        return "\n".join(lines)
    
    def print_UnaryOpNode(self, node, indent):
        # lines = [f"{self._indent(indent)}UnaryOp: {node.operand}"]
        lines = [self._print_header(node, f"UnaryOp: {node.operand}", indent)]
        lines.extend(self._print_section("Operand", node.expr, indent + 1))
        return "\n".join(lines)
    
    def print_NumberNode(self, node, indent):
        # return f"{self._indent(indent)}Number: {node.value}"
        return self._print_header(node, f"Number: {node.value}", indent)
    
    def print_StringNode(self, node, indent):
        # return f"{self._indent(indent)}String: {node.value}"
        return self._print_header(node, f"String: {node.value}", indent)
    
    def print_CharNode(self, node, indent):
        # return f"{self._indent(indent)}Char: {node.value}"
        return self._print_header(node, f"Char: {node.value}", indent)
    
    def print_BooleanNode(self, node, indent):
        # return f"{self._indent(indent)}Boolean: {node.value}"
        return self._print_header(node, f"Boolean: {node.value}", indent)
    
    def print_VarNode(self, node, indent):
        # return f"{self._indent(indent)}Variable: {node.name}"
        return self._print_header(node, f"Variable: {node.name}", indent)
    
    def _print_access_node(self, kind, var, extra_info, indent, node):
        """Helper to print array/record access nodes"""
        # lines = [f"{self._indent(indent)}{kind}:"]
        lines = [self._print_header(node, f"{kind}:", indent)]
        lines.extend(self._print_section("Variable", var, indent + 1))
        lines.extend(extra_info)
        return "\n".join(lines)
    
    def print_ArrayAccessNode(self, node, indent):
        extra = self._print_section("Index", node.index, indent + 1)
        return self._print_access_node("ArrayAccess", node.var, extra, indent, node)
    
    def print_RecordAccessNode(self, node, indent):
        extra = self._print_labeled_value("Field", node.field, indent + 1)
        return self._print_access_node("RecordAccess", node.var, extra, indent, node)


def print_ast(ast_root, indent_size=2):
    printer = ASTPrinter(indent_size)
    print(printer.print(ast_root))