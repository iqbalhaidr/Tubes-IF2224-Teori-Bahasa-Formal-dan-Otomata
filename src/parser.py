import sys

class TreeNode:
    def __init__(self, name):
        self.name = name
        self.children = []

    def add_child(self, node):
        self.children.append(node)

    def display(self):
        print(self.name)
        self._display_children_recursive("")

    def _display_children_recursive(self, indent):
        children_list = self.children
        
        for i, child_node in enumerate(children_list):
            is_last_child = (i == len(children_list) - 1)
            
            if is_last_child:
                prefix = indent + "L- "
                child_indent = indent + "   "
            else:
                prefix = indent + "|- "
                child_indent = indent + "|  "
                
            print(f"{prefix}{child_node.name}")
            
            if child_node.children:
                child_node._display_children_recursive(child_indent)

class Parser:
    def __init__(self, list_token):
        self.list_token = list_token
        self.next_SYM_idx = 0
        self.SYM = {
            "type": None,
            "value": None
        }
    
    def read(self):
        if (self.next_SYM_idx < len(self.list_token)):
            next_SYM = self.list_token[self.next_SYM_idx]
            self.SYM["type"] = next_SYM.split('(')[0]
            self.SYM["value"] = next_SYM.split('(')[1].rstrip(')')
            self.next_SYM_idx = self.next_SYM_idx + 1

    def accept(self, type, value=None):
        if (self.SYM["type"] != type):
            # TODO: Add more error details "error on line ... expected bla bla"
            print("Type error")
            sys.exit("Exiting program")
        
        if (value and self.SYM["value"] != value):
            # TODO: Add more error details "error on line ... expected bla bla"
            print("Value error")
            sys.exit("Exiting program")

        node = TreeNode(f'{self.SYM["type"]}({self.SYM["value"]})')

        # Baca SYM selanjutnya
        self.read()
        return node
    
    def peek(self):
        if (self.next_SYM_idx < len(self.list_token)):
            next_SYM = self.list_token[self.next_SYM_idx]
            peeked_type = next_SYM.split('(')[0]
            peeked_value = next_SYM.split('(')[1].rstrip(')')
            return {
                "type": peeked_type,
                "value": peeked_value
            }
        else:
            return None
    
    def parse(self):
        self.read()
        result = self.program()

        print("Parse success, code error free")
        result.display()

    #1 <program> -> <program-header> + <declaration-part> + <compound-statement> + DOT
    def program(self):
        node = TreeNode("<program>")
        node.add_child(self.program_header())
        node.add_child(self.declaration_part())
        node.add_child(self.compound_statement())
        node.add_child(self.accept(type="DOT", value="."))
        return node
    
    #2 <program-header> -> KEYWORD(program) + IDENTIFIER + SEMICOLON
    def program_header(self):
        node = TreeNode("<program-header>")
        node.add_child(self.accept(type="KEYWORD", value="program"))
        node.add_child(self.accept(type="IDENTIFIER"))
        node.add_child(self.accept(type="SEMICOLON"))
        return node
    
    #3 <declaration-part> -> (const-declaration)* + (type-declaration)* + (var-declaration)* + (subprogram-declaration)*
    def declaration_part(self):
        node = TreeNode("<declaration-part>")
        
        # (const-declaration)*
        while self.SYM["type"] == "KEYWORD" and self.SYM["value"] == "konstanta":
            node.add_child(self.const_declaration())
        
        # (type-declaration)*
        while self.SYM["type"] == "KEYWORD" and self.SYM["value"] == "tipe":
            node.add_child(self.type_declaration())
            
        # (var-declaration)*
        while self.SYM["type"] == "KEYWORD" and self.SYM["value"] == "variabel":
            node.add_child(self.variabel_declaration())
        
        # (subprogram-declaration)*
        while self.SYM["type"] == "KEYWORD" and (self.SYM["value"] == "prosedur" or self.SYM["value"] == "fungsi"):
            node.add_child(self.subprogram_declaration())
            
        return node
    
    #4 <const-declaration> -> KEYWORD(konstanta) + (IDENTIFIER = value + SEMICOLON)+
    def const_declaration(self):
        node = TreeNode("<const-declaration>")

        node.add_child(self.accept(type="KEYWORD", value="konstanta"))
    
        node.add_child(self.accept(type="IDENTIFIER"))
        node.add_child(self.accept(type="ASSIGN_OPERATOR", value=":="))
        node.add_child(self.accept(type="NUMBER"))
        node.add_child(self.accept(type="SEMICOLON"))

        while self.SYM["type"] == "IDENTIFIER":
            node.add_child(self.accept(type="IDENTIFIER"))
            node.add_child(self.accept(type="ASSIGN_OPERATOR", value=":="))
            node.add_child(self.accept(type="NUMBER"))
            node.add_child(self.accept(type="SEMICOLON"))
        return node

    #5 <type-declaration> -> KEYWORD(tipe) + (IDENTIFIER = type-definition + SEMICOLON)+

    #6 <var-declaration> -> KEYWORD(variabel) + (identifier-list + COLON + type + SEMICOLON)+
    def var_declaration(self):
        node = TreeNode("<var-declaration>")

        node.add_child(self.accept(type="KEYWORD", value="variabel"))
        
        # pastikan minimal 1 kali kemunculan (identifier-list + COLON + type + SEMICOLON)
        node.add_child(self.identifier_list())
        node.add_child(self.accept(type="COLON", value=":"))
        node.add_child(self.type())
        node.add_child(self.accept(type="SEMICOLON", value=";"))

        while self.SYM["type"] == "IDENTIFIER":
            node.add_child(self.identifier_list())
            node.add_child(self.accept(type="COLON", value=":"))
            node.add_child(self.type())
            node.add_child(self.accept(type="SEMICOLON", value=";"))

        return node


    #7 <identifier-list> -> IDENTIFIER (COMMA + IDENTIFIER)*
    def identifier_list(self):
        node = TreeNode("<identifier-list>")

        node.add_child(self.accept(type="IDENTIFIER"))
        while self.SYM["type"] == "COMMA" and self.SYM["value"] == ",":
            node.add_child(self.accept(type="COMMA", value=","))
            node.add_child(self.accept(type="IDENTIFIER"))
        
        return node

    #8 <type> -> KEYWORD(integer)|KEYWORD(real)|KEYWORD(boolean)|KEYWORD(char)|array-type
    def type(self):
        node = TreeNode("<type>")
        if self.SYM["type"] == "KEYWORD":
            match self.SYM["value"]:
                case "integer":
                    node.add_child(self.accept(type="KEYWORD", value="integer"))
                case "real":
                    node.add_child(self.accept(type="KEYWORD", value="real"))
                case "boolean":
                    node.add_child(self.accept(type="KEYWORD", value="boolean"))
                case "char":
                    node.add_child(self.accept(type="KEYWORD", value="char"))
                case _:
                    pass

        else:
            node.add_child(self.array_type())
        return node

    #9 <array-type> -> KEYWORD(larik) + LBRACKET + range + RBRACKET + KEYWORD(dari) + type

    #10 <range> -> expression + RANGE_OPERATOR(..) + expression
    def range(self):
        node = TreeNode("<range>")
        node.add_child(self.expression())
        node.add_child(self.accept(type="RANGE_OPERATOR", value=".."))
        node.add_child(self.expression())
        return node

    #11 <subprogram-declaration> -> procedure-declaration|function-declaration
    def subprogram_declaration(self):
        node = TreeNode("<subprogram-declaration>")
        if self.SYM["type"] == "KEYWORD" and self.SYM["value"] == "prosedur":
            node.add_child(self.procedure_declaration())
        elif self.SYM["type"] == "KEYWORD" and self.SYM["value"] == "fungsi":
            node.add_child(self.function_declaration())
        return node

    #12 <procedure-declaration> -> KEYWORD(prosedur) + IDENTIFIER + (formal-parameter-list)? + SEMICOLON + block + SEMICOLON
    def procedure_declaration(self):
        node = TreeNode("<procedure-declaration>")

        node.add_child(self.accept(type="KEYWORD", value="prosedur"))
        node.add_child(self.accept(type="IDENTIFIER"))
        if self.SYM["type"] == "LPARENTHESIS" and self.SYM["value"] == "(":
            node.add_child(self.formal_parameter_list())
        node.add_child(self.accept(type="SEMICOLON", value=";"))
        node.add_child(self.declaration_part())
        node.add_child(self.compound_statement())
        node.add_child(self.accept(type="SEMICOLON", value=";"))
        return node

    #13 <function-declaration> -> KEYWORD(fungsi) + IDENTIFIER + (formal-parameter-list)? + COLON + type + SEMICOLON + block + SEMICOLON
    def function_declaration(self):
        node = TreeNode("<function-declaration>")
        node.add_child(self.accept(type="KEYWORD", value="fungsi"))
        node.add_child(self.accept(type="IDENTIFIER"))

        if self.SYM["type"] == "LPARENTHESIS":
            node.add_child(self.formal_parameter_list())

        node.add_child(self.accept(type="COLON", value=":"))
        node.add_child(self.type())
        node.add_child(self.accept(type="SEMICOLON", value=";"))
        # mewakili block
        node.add_child(self.declaration_part())
        node.add_child(self.compound_statement())

        node.add_child(self.accept(type="SEMICOLON", value=";"))
        return node

    #14 <formal-parameter-list> -> LPARENTHESIS + parameter-group (SEMICOLON + parameter-group)* + RPARENTHESIS
    def formal_parameter_list(self):
        node = TreeNode("<formal-parameter-list>")
        node.add_child(self.accept(type="LPARENTHESIS"))

        node.add_child(self.parameter_group())

        while self.SYM["type"] == "SEMICOLON":
            node.add_child(self.accept(type="SEMICOLON"))
            node.add_child(self.parameter_group())

        node.add_child(self.accept(type="RPARENTHESIS"))
        return node

    #tambahan <parameter-group> -> identifier-list + COLON + type
    def parameter_group(self):
        node = TreeNode("<parameter-group>")
        node.add_child(self.identifier_list())
        node.add_child(self.accept(type="COLON"))
        node.add_child(self.type())
        return node
    
    #15 <compound-statement> -> KEYWORD(mulai) + statement-list + KEYWORD(selesai)
    def compound_statement(self):
        node = TreeNode("<compound-statement>")
        node.add_child(self.accept(type="KEYWORD", value="mulai"))
        node.add_child(self.statement_list())
        node.add_child(self.accept(type="KEYWORD", value="selesai"))
        return node
    
    #16 <statement-list> -> statement + (SEMICOLON + statement)*
    def statement_list(self):
        node = TreeNode("<statement-list>")
        peektype = self.peek()["type"]
        peekvalue = self.peek()["value"]

        if peektype == "IDENTIFIER":
            node.add_child(self.assignment_statement())
        elif peektype == "KEYWORD" and peekvalue == "jika":
            node.add_child(self.if_statement()) 
        elif peektype == "KEYWORD" and peekvalue == "selama":
            node.add_child(self.while_statement())
        elif peektype == "KEYWORD" and peekvalue == "untuk":
            node.add_child(self.for_statement())
        elif peektype == "IDENTIFIER":
            node.add_child(self.procedure_function_call())
        elif peektype == "KEYWORD" and peekvalue == "mulai":
            node.add_child(self.compound_statement())
        elif peektype == "KEYWORD" and peekvalue == "fungsi":
            node.add_child(self.function_declaration())
        elif peektype == "KEYWORD" and peekvalue == "prosedur":
            node.add_child(self.procedure_declaration())
        else:
            # tidak boleh kosong
            print("Empty statement list encountered") 
            pass

        while self.SYM["type"] == "SEMICOLON":
            node.add_child(self.accept(type="SEMICOLON"))
            peektype = self.peek()["type"]
            peekvalue = self.peek()["value"]

            if peektype == "IDENTIFIER":
                node.add_child(self.assignment_statement())
            elif peektype == "KEYWORD" and peekvalue == "jika":
                node.add_child(self.if_statement()) 
            elif peektype == "KEYWORD" and peekvalue == "selama":
                node.add_child(self.while_statement())
            elif peektype == "KEYWORD" and peekvalue == "untuk":
                node.add_child(self.for_statement())
            elif peektype == "IDENTIFIER":
                node.add_child(self.procedure_function_call())
            elif peektype == "KEYWORD" and peekvalue == "mulai":
                node.add_child(self.compound_statement())
            elif peektype == "KEYWORD" and peekvalue == "fungsi":
                node.add_child(self.function_declaration())
            elif peektype == "KEYWORD" and peekvalue == "prosedur":
                node.add_child(self.procedure_declaration())  
            
        return node

    #17 <assignment-statement> -> IDENTIFIER + ASSIGN_OPERATOR(:=) + expression
    def assignment_statement(self):
        node = TreeNode("<assignment-statement>")
        node.add_child(self.accept(type="IDENTIFIER"))
        node.add_child(self.accept(type="ASSIGN_OPERATOR", value=":="))
        node.add_child(self.expression())
        return node

    #18 <if-statement> -> KEYWORD(jika) + expression + KEYWORD(maka) + statement + (KEYWORD(selain-itu) + statement)?
    
    #19 <while-statement> -> KEYWORD(selama) + expression + KEYWORD(lakukan) + statement
    def while_statement(self):
        node = TreeNode("<while-statement>")

        node.add_child(self.accept(type="KEYWORD", value="selama"))
        node.add_child(self.expression())
        node.add_child(self.accept(type="KEYWORD", value="lakukan"))
        node.add_child(self.statement())
        return node

    #20 <for-statement> -> KEYWORD(untuk) + IDENTIFIER + ASSIGN_OPERATOR + expression + (KEYWORD(ke)/KEYWORD(turun-ke)) + expression + KEYWORD(lakukan ) + statement
    def for_statement(self):
        node = TreeNode("<for-statement>")

        node.add_child(self.accept(type="KEYWORD", value="untuk"))
        node.add_child(self.accept(type="IDENTIFIER"))
        node.add_child(self.accept(type="ASSIGN_OPERATOR"))
        node.add_child(self.expression())

        match self.SYM:
            case {"type": "KEYWORD", "value": "ke"}:
                node.add_child(self.accept(type="KEYWORD", value="ke"))
            case {"type": "KEYWORD", "value": "turun-ke"}:
                node.add_child(self.accept(type="KEYWORD", value="turun-ke"))
            case _:
                sys.exit("Error: Expected 'ke' or 'turun-ke'! (<statement>) Exiting program")

        node.add_child(self.expression())
        node.add_child(self.accept(type="KEYWORD", value="lakukan"))
        node.add_child(self.statement())
        
        return node

    #21 <procedure/function-call> -> IDENTIFIER + (LPARENTHESIS + parameter-list + RPARENTHESIS)
    def procedure_function_call(self):
        node = TreeNode("<procedure/function-call>")
        node.add_child(self.accept(type="IDENTIFIER"))

        node.add_child(self.accept(type="LPARENTHESIS"))
        node.add_child(self.parameter_list())
        node.add_child(self.accept(type="RPARENTHESIS"))
        return node
    
    #22 <parameter-list> -> expression + (COMMA + expression)*
    
    #23 <expression> -> simple-expression + (relational-operator + simple-expression)?
    def expression(self):
        node = TreeNode("<expression>")
        node.add_child(self.simple_expression())
        if self.SYM["type"] == "RELATIONAL_OPERATOR":
            node.add_child(self.relational_operator())
            node.add_child(self.simple_expression())
        return node
    
    #24 <simple-expression> -> (ARITHMETIC_OPERATOR(+)|ARITHMETIC_OPERATOR(-))? + term + (additive-operator + term)*
    def simple_expression(self):
        node = TreeNode("<simple-expression>")
        
        if self.SYM["type"] == "ARITHMETIC_OPERATOR" and (self.SYM["value"] == "+" or self.SYM["value"] == "-"):
            node.add_child(self.accept(type="ARITHMETIC_OPERATOR"))
        
        node.add_child(self.term())
        
        while self.SYM["type"] == "KEYWORD" and (self.SYM["value"] == "atau" ) or self.SYM["type"] == "ARITHMETIC_OPERATOR" and (self.SYM["value"] == "+" or self.SYM["value"] == "-"):
            if self.SYM["type"] == "KEYWORD" and self.SYM["value"] == "atau":
                node.add_child(self.accept(type="KEYWORD", value="atau"))
            else:
                node.add_child(self.accept(type="ARITHMETIC_OPERATOR"))
            node.add_child(self.term())
        
        return node
    
    #25 <term> -> factor + (multiplicative-operator + factor)*
    def term(self):
        node = TreeNode("<term>")

        node.add_child(self.factor())
        # Ini harusnya while(SYM == FIRST(<multiplicative-operator>)). terpaksa manual karena campur dengan "dan"
        while (self.SYM["type"] == "ARITHMETIC_OPERATOR" and self.SYM["value"] == "*") or (self.SYM["type"] == "ARITHMETIC_OPERATOR" and self.SYM["value"] == "/") or (self.SYM["type"] == "ARITHMETIC_OPERATOR" and self.SYM["value"] == "bagi") or (self.SYM["type"] == "ARITHMETIC_OPERATOR" and self.SYM["value"] == "mod") or (self.SYM["type"] == "LOGICAL_OPERATOR" and self.SYM["value"] == "dan"):
            node.add_child(self.multiplicative_operator())
            node.add_child(self.factor())

        return node

    #26 <factor> -> IDENTIFIER|NUMBER|CHAR_LITERAL|STRING_LITERAL|(LPARENTHESIS + expression + RPARENTHESIS)|LOGICAL_OPERATOR(tidak) + factor|function-call
    def factor(self):
        node = TreeNode("<factor>")

        match self.SYM:
            case {"type": "IDENTIFIER"}:
                # Ngebedain function call (IDENTIFIER+LPARENTHESIS...) sama IDENTIFIER biasa
                if self.peek() and self.peek()["type"] == "LPARENTHESIS":
                    node.add_child(self.procedure_function_call())
                else:
                    node.add_child(self.accept(type="IDENTIFIER"))
            case {"type": "NUMBER"}:
                node.add_child(self.accept(type="NUMBER"))
            case {"type": "CHAR_LITERAL"}:
                node.add_child(self.accept(type="CHAR_LITERAL"))
            case {"type": "STRING_LITERAL"}:
                node.add_child(self.accept(type="STRING_LITERAL"))
            case {"type": "LPARENTHESIS"}:
                node.add_child(self.accept(type="LPARENTHESIS"))
                node.add_child(self.expression())
                node.add_child(self.accept(type="RPARENTHESIS"))
            case {"type": "LOGICAL_OPERATOR", "value": "tidak"}:
                node.add_child(self.accept(type="LOGICAL_OPERATOR", value="tidak"))
                node.add_child(self.factor())
            case _:
                pass
        return node

    #28 <relational-operator> -> =|<>|<|<=|>|>=
    def relational_operator(self):
        node = TreeNode("<relational-operator>")
        match self.SYM:
            case {"type": "RELATIONAL_OPERATOR", "value": "="}:
                node.add_child(self.accept(type="RELATIONAL_OPERATOR", value="="))
            case {"type": "RELATIONAL_OPERATOR", "value": "<>"}:
                node.add_child(self.accept(type="RELATIONAL_OPERATOR", value="<>"))
            case {"type": "RELATIONAL_OPERATOR", "value": "<"}:
                node.add_child(self.accept(type="RELATIONAL_OPERATOR", value="<"))
            case {"type": "RELATIONAL_OPERATOR", "value": "<="}:
                node.add_child(self.accept(type="RELATIONAL_OPERATOR", value="<="))
            case {"type": "RELATIONAL_OPERATOR", "value": ">"}:
                node.add_child(self.accept(type="RELATIONAL_OPERATOR", value=">"))
            case {"type": "RELATIONAL_OPERATOR", "value": ">="}:
                node.add_child(self.accept(type="RELATIONAL_OPERATOR", value=">="))
        return node
    
    #29 <additive-operator> -> +|-|atau
    
    #30 <multiplicative-operator> -> *|/|bagi|mod|dan

    #31 <statement>
    def statement(self):
        node = TreeNode("<statement>")

        match self.SYM:
            case {"type": "IDENTIFIER"}:
                # Kita gaskan jadi LL2 lah anjeng. ini intinya cek type next SYM tanpa increment next_SYM_idx
                next_SYM_type = self.list_token[self.next_SYM_idx].split('(')[0] if (self.next_SYM_idx < len(self.list_token)) else None
                if next_SYM_type == "ASSIGN_OPERATOR":
                    node.add_child(self.assignment_statement())
                elif next_SYM_type == "LPARENTHESIS":
                    node.add_child(self.procedure_function_call())
                else:
                    sys.exit("Error: Expected ':=' or '(' after identifier! (<statement>) Exiting program")
            case {"type": "KEYWORD", "value": "mulai"}:
                node.add_child(self.compound_statement())
            case {"type": "KEYWORD", "value": "jika"}:
                node.add_child(self.if_statement())
            case {"type": "KEYWORD", "value": "kasus"}:
                # TODO: Implementasi case_statement()
                sys.exit("<case-statement> belum diimplmentasikan woy! Exiting program")
            case {"type": "KEYWORD", "value": "selama"}:
                node.add_child(self.while_statement())
            case {"type": "KEYWORD", "value": "ulangi"}:
                node.add_child(self.repeat_statement())
            case {"type": "KEYWORD", "value": "untuk"}:
                node.add_child(self.for_statement())
            case _:
                pass
        
        return node

    #32 <case-statement>

    #33 <repeat-statement>
    def repeat_statement(self):
        node = TreeNode("<repeat-statement>")
        node.add_child(self.accept(type="KEYWORD", value="ulangi"))
        node.add_child(self.statement_list())
        node.add_child(self.accept(type="KEYWORD", value="sampai"))
        node.add_child(self.expression())
        return node
