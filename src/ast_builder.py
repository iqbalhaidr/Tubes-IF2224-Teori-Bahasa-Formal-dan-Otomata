from parser import *
from ast_nodes import *

class AST_Builder:
    def __init__(self, root: TreeNode):
        self.root = root

    def build(self):
        return self.visit(self.root)

    def visit(self, node: TreeNode, raw_str: str = None):
        method_name = "procedure_call" if node.name == "<procedure/function-call>" else self._clean(node.name)
        method = getattr(self, f"visit_{method_name}", self.generic_visit)
        return method(node)

    def _clean(self, name: str):
        return name.replace("<", "").replace(">", "").replace("-", "_")

    def _extract_value(self, raw: str):
        """Extract value from token format: TOKEN_TYPE(value)"""
        return raw[raw.find("(") + 1:raw.rfind(")")]

    def generic_visit(self, node):
        raise Exception(f"No visit_ method for {node.name}")
    
    # PROGRAM
    def visit_program(self, node: TreeNode):
        prog_name = self._extract_value(node.children[0].children[1].name)
        declarations = self.visit_declaration_part(node.children[1])
        block = self.visit_compound_statement(node.children[2])
        return ProgramNode(prog_name, declarations, block)

    def visit_compound_statement(self, node: TreeNode):
        print("ini nama anak pertama dari compound statement " + node.children[1].name)
        stmt_list = self.visit_statement_list(node.children[1])
        return BlockNode(stmt_list)

    # DECLARATIONS
    def visit_declaration_part(self, node):
        declarations = []
        for child in node.children:
            if child.name in ("<const-declaration>", "<var-declaration>", "<type-declaration>", "<subprogram-declaration>"):
                result = self.visit(child)
                declarations.extend(result if isinstance(result, list) else [result])
        return declarations

    def visit_const_declaration(self, node: TreeNode):
        declarations = []
        idx = 1

        while idx < len(node.children):
            name = self._extract_value(node.children[idx].name)
            const_node = node.children[idx + 2].children[0]
            
            if const_node.name == "<number-statement>":
                value = self.visit_number_statement(const_node)
            elif const_node.name.startswith("STRING_LITERAL"):
                value = StringNode(self._extract_value(const_node.name))
            elif const_node.name.startswith("CHAR_LITERAL"):
                value = CharNode(self._extract_value(const_node.name))
            else:
                raise Exception("Unhandled const literal: " + const_node.name)

            declarations.append(ConstDeclNode(name, value))
            idx += 4

        return declarations

    def visit_var_declaration(self, node: TreeNode):
        declarations = []
        idx = 1

        while idx < len(node.children):
            names = self._extract_identifier_list(node.children[idx])
            type_node = self.visit_type(node.children[idx + 2])
            
            declarations.extend([VarDeclNode(name, type_node) for name in names])
            idx += 4

        return declarations

    #ni fungsi pokoknya buat balikin semua nama dari identif yang ada di idlist
    def _extract_identifier_list(self, ident_list_node):    
        names = []
        k = 0
        while k < len(ident_list_node.children):
            if not ident_list_node.children[k].name.startswith("COMMA"):
                names.append(self._extract_value(ident_list_node.children[k].name))
            k += 1
        return names

    def visit_type_declaration(self, node: TreeNode):
        declarations = []
        idx = 1
        while idx < len(node.children):
            name = self._extract_value(node.children[idx].name)
            type_node = self.visit_type(node.children[idx + 2])
            declarations.append(TypeDeclNode(name, type_node))
            idx += 4
        return declarations
    
    def visit_subprogram_declaration(self, node: TreeNode):
        return self.visit(node.children[0])

    def visit_array_type(self, node: TreeNode):
        range_node = node.children[2]
        low = self.visit_expression(range_node.children[0])
        high = self.visit_expression(range_node.children[2])
        elem_type = self.visit(node.children[5])
        return ArrayTypeNode(low, high, elem_type)

    def visit_record_type(self, node: TreeNode):
        fields = []
        idx = 1
        while idx < len(node.children) - 1:
            identifier_list = self.visit_identifier_list(node.children[idx])
            type_node = self.visit_type(node.children[idx + 2])
            fields.extend([(elem, type_node) for elem in identifier_list])
            idx += 4
        return RecordTypeNode(fields)

    def visit_identifier_list(self, node: TreeNode):
        return [self._extract_value(elem.name) for elem in node.children]
    
    def visit_procedure_declaration(self, node: TreeNode):
        name = self._extract_value(node.children[1].name)
        idx = 2
        params = []

        if node.children[idx].name == "<formal-parameter-list>":
            params = self.visit_formal_parameter_list(node.children[idx])
            idx += 1

        idx += 1  # SEMICOLON

        declarations = []
        if node.children[idx].name == "<declaration-part>":
            declarations = self.visit_declaration_part(node.children[idx])
            idx += 1

        body = self.visit_compound_statement(node.children[idx])
        return ProcedureDeclNode(name, params, declarations, body)

    def visit_function_declaration(self, node: TreeNode):
        name = self._extract_value(node.children[1].name)
        idx = 2
        params = []

        if node.children[idx].name == "<formal-parameter-list>":
            params = self.visit_formal_parameter_list(node.children[idx])
            idx += 1

        idx += 1  # COLON
        return_type = self.visit_type(node.children[idx])
        idx += 2  # SEMICOLON

        decl_part = self.visit_declaration_part(node.children[idx])
        body = self.visit_compound_statement(node.children[idx + 1])

        return FunctionDeclNode(name, params, return_type, decl_part, body)

    def visit_formal_parameter_list(self, node: TreeNode):
        params = []
        for child in node.children[1:-1]:  # Skip LPARENTHESIS and RPARENTHESIS
            if child.name == "<parameter-group>":
                params.extend(self.visit(child))
        return params

    def visit_parameter_group(self, node: TreeNode):
        names = self.visit_identifier_list(node.children[0])
        type_node = self.visit_type(node.children[2])
        return [(name, type_node) for name in names]

    # STATEMENTS
    def visit_assignment_statement(self, node: TreeNode):
        target = self.visit_variable(node.children[0])
        value_node = self.visit_expression(node.children[2])
        return AssignNode(target, value_node)

    def visit_if_statement(self, node: TreeNode):
        cond = self.visit_expression(node.children[1])
        print("ini dia if statement visit then si " + str(node.children[3].children[0].name))
        then_stmt = self.visit(node.children[3].children[0])
        else_stmt = self.visit(node.children[5]) if len(node.children) > 4 else None
        return IfNode(cond, then_stmt, else_stmt)

    def visit_while_statement(self, node: TreeNode):
        cond = self.visit_expression(node.children[1])
        body = self.visit_statement(node.children[3])
        return WhileNode(cond, body)

    def visit_for_statement(self, node: TreeNode):
        var_name = self._extract_value(node.children[1].name)
        start_expr = self.visit_expression(node.children[3])
        direction = self._extract_value(node.children[4].name)
        end_expr = self.visit_expression(node.children[5])
        body = self.visit_statement(node.children[7])

        return ForNode(var_name, start_expr, end_expr, direction, body)

    def visit_repeat_statement(self, node: TreeNode):
        stmts = self.visit_statement_list(node.children[1])
        cond = self.visit_expression(node.children[3])
        return RepeatNode(stmts, cond)

    def visit_case_statement(self, node: TreeNode):
        selector = self.visit_expression(node.children[1])
        branches = []
        idx = 3

        while idx < len(node.children) and not node.children[idx].name.startswith("KEYWORD(akhir"):
            labels = self._extract_case_labels(node, idx)
            idx = self._skip_to_colon(node, idx) + 1
            stmt = self.visit_statement(node.children[idx])
            branches.append(CaseBranchNode(labels, stmt))
            idx += 1
            if idx < len(node.children) and node.children[idx].name.startswith("SEMICOLON"):
                idx += 1

        return CaseNode(selector, branches)

    def _extract_case_labels(self, node, start_idx):
        """Extract case labels until COLON"""
        labels = []
        idx = start_idx
        
        while idx < len(node.children):
            cur = node.children[idx]
            if cur.name.startswith("COLON"):
                break
            if cur.name.startswith("COMMA"):
                idx += 1
                continue

            if cur.name == "<const>":
                lit = cur.children[0].name
                raw = self._extract_value(lit)
                
                if lit.startswith("NUMBER("):
                    labels.append(NumberNode(int(raw)))
                elif lit.startswith("CHAR_LITERAL("):
                    labels.append(CharNode(raw))
                elif lit.startswith("STRING_LITERAL("):
                    labels.append(StringNode(raw))
                elif lit.startswith("IDENTIFIER("):
                    labels.append(VarNode(raw))
            idx += 1
        
        return labels

    def _skip_to_colon(self, node, start_idx):
        """Skip to COLON token"""
        idx = start_idx
        while idx < len(node.children) and not node.children[idx].name.startswith("COLON"):
            idx += 1
        return idx

    def visit_procedure_call(self, node: TreeNode):
        name = self._extract_value(node.children[0].name)
        args = self.visit_formal_parameter_list(node.children[2]) if len(node.children) > 2 else []
        return ProcedureCallNode(name, args)

    def visit_function_call(self, node):
        name = self._extract_value(node.children[0].name)
        args = self.visit_formal_parameter_list(node.children[2]) if len(node.children) > 2 else []
        return FunctionCallNode(name, args)
    
    # EXPRESSIONS
    def visit_expression(self, node: TreeNode):
        if len(node.children) == 1:
            return self.visit_simple_expression(node.children[0])

        left = self.visit_simple_expression(node.children[0])
        op = self._extract_value(node.children[1].children[0].name)
        right = self.visit_simple_expression(node.children[2])
        return BinOpNode(op, left, right)

    def visit_simple_expression(self, node: TreeNode):
        idx = 0
        
        if node.children[0].name.startswith("ARITHMETIC_OPERATOR"):
            op = self._extract_value(node.children[0].name)
            expr = self.visit(node.children[1])
            left = UnaryOpNode(op, expr)
            idx = 2
        else:
            left = self.visit(node.children[0])
            idx = 1

        while idx < len(node.children):
            op = self._extract_value(node.children[idx].children[0].name)
            right = self.visit(node.children[idx + 1])
            left = BinOpNode(op, left, right)
            idx += 2

        return left

    def visit_term(self, node: TreeNode):
        left = self.visit(node.children[0])
        i = 1
        
        while i < len(node.children):
            op = self._extract_value(node.children[i].children[0].name)
            right = self.visit_factor(node.children[i + 1])
            left = BinOpNode(op, left, right)
            i += 2

        return left

    def visit_factor(self, node: TreeNode):
        child = node.children[0]

        if child.name.startswith("LPARENTHESIS"):
            return self.visit_expression(node.children[1])

        if child.name.startswith("LOGICAL_OPERATOR"):
            op = self._extract_value(child.name)
            return UnaryOpNode(op, self.visit(node.children[1]))

        if child.name.startswith("ARITHMETIC_OPERATOR(-)"):
            return UnaryOpNode("-", self.visit(node.children[1]))

        if child.name == "<number-statement>":
            return self.visit_number_statement(child)

        if child.name.startswith("STRING_LITERAL"):
            return StringNode(self._extract_value(child.name))

        if child.name.startswith("CHAR_LITERAL"):
            return CharNode(self._extract_value(child.name))

        if child.name.startswith("KEYWORD(true)") or child.name.startswith("KEYWORD(false)"):
            return BooleanNode(self._extract_value(child.name) == "true")

        if child.name == "<procedure/function-call>":
            return self.visit_function_call(child)

        if child.name == "<variable>":
            return self.visit_variable(child)

        if child.name.startswith("IDENTIFIER"):
            return VarNode(self._extract_value(child.name))

        return self.visit(child)

    # HELPER
    def visit_statement_list(self, node: TreeNode):
        print('masuk statement list')
        print('ini panjang si ganteng di statement list' + str(len(node.children)))
        statements = []
        idx = 0
        
        while idx < len(node.children) - 2:
            print("ini nama dari anak statement di statement list " + node.children[idx].children[0].name)
            statements.append(self.visit(node.children[idx].children[0]))
            idx += 2
        
        return statements

    def visit_parameter_list(self, node: TreeNode):
        print("ini dia masuk parameter list")
        args = []
        
        for idx, child in enumerate(node.children):
            if child.name.startswith("<expression"):
                print('ini dia parameter ke- ' + str(idx))
                args.append(self.visit(child))

        return args[0] if len(args) == 1 else args

    def visit_number_statement(self, node: TreeNode):
        if len(node.children) == 3:
            left = self._extract_value(node.children[0].name)
            right = self._extract_value(node.children[2].name)
            return NumberNode(float(f"{left}.{right}"))

        value = int(self._extract_value(node.children[0].name))
        return NumberNode(value)

    def visit_type(self, node: TreeNode):
        child = node.children[0]
        
        keyword_types = {
            "KEYWORD(integer)": "integer",
            "KEYWORD(real)": "real",
            "KEYWORD(boolean)": "boolean",
            "KEYWORD(char)": "char"
        }
        
        for keyword, type_name in keyword_types.items():
            if child.name.startswith(keyword):
                return BuiltinTypeNode(type_name)

        if child.name == "<array-type>":
            return self.visit_array_type(child)
        if child.name == "<record-type>":
            return self.visit_record_type(child)
        if child.name.startswith("IDENTIFIER"):
            return CustomTypeNode(self._extract_value(child.name))

        raise Exception("Unknown type: " + child.name)
    
    def visit_variable(self, node: TreeNode):
        current = VarNode(self._extract_value(node.children[0].name))
        i = 1

        while i < len(node.children):
            child = node.children[i]

            if child.name.startswith("DOT"):
                field_name = self._extract_value(node.children[i + 1].name)
                current = RecordAccessNode(current, field_name)
                i += 2
            elif child.name.startswith("LBRACKET"):
                index_expr = self.visit_expression(node.children[i + 1].children[0])
                current = ArrayAccessNode(current, index_expr)
                i += 3
            else:
                i += 1

        return current

    def visit_statement(self, node: TreeNode):
        return self.visit(node.children[0]) if node.children else None