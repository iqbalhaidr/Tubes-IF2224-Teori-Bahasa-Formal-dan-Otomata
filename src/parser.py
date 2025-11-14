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

        node = TreeNode(f"{self.SYM["type"]}({self.SYM["value"]})")

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

    #7 <identifier-list> -> IDENTIFIER (COMMA + IDENTIFIER)*

    #8 <type> -> KEYWORD(integer)|KEYWORD(real)|KEYWORD(boolean)|KEYWORD(char)|array-type

    #9 <array-type> -> KEYWORD(larik) + LBRACKET + range + RBRACKET + KEYWORD(dari) + type

    #10 <range> -> expression + RANGE_OPERATOR(..) + expression

    #11 <subprogram-declaration> -> procedure-declaration|function-declaration
    def subprogram_declaration(self):
        node = TreeNode("<subprogram-declaration>")
        if self.SYM["type"] == "KEYWORD" and self.SYM["value"] == "prosedur":
            node.add_child(self.procedure_declaration())
        elif self.SYM["type"] == "KEYWORD" and self.SYM["value"] == "fungsi":
            node.add_child(self.function_declaration())
        return node

    #12 <procedure-declaration> -> KEYWORD(prosedur) + IDENTIFIER + (formal-parameter-list)? + SEMICOLON + block + SEMICOLON

    #13 <function-declaration> -> KEYWORD(fungsi) + IDENTIFIER + (formal-parameter-list)? + COLON + type + SEMICOLON + block + SEMICOLON
    
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
        # TODO: Implement statement_list()
        # node.add_child(self.statement_list())
        node.add_child(self.accept(type="KEYWORD", value="selesai"))
        return node
    
    #16 <statement-list> -> statement + (SEMICOLON + statement)*
    def statement_list(self):
        node = TreeNode("<statement-list>")
        self.peek()["type"], self.peek()["value"]

        if self.SYM["type"] == "IDENTIFIER":
            node.add_child(self.assignment_statement())
        elif self.SYM["type"] == "KEYWORD" and self.SYM["value"] == "jika":
            node.add_child(self.if_statement()) 
        elif self.SYM["type"] == "KEYWORD" and self.SYM["value"] == "selama":
            node.add_child(self.while_statement())
        elif self.SYM["type"] == "KEYWORD" and self.SYM["value"] == "untuk":
            node.add_child(self.for_statement())
        elif self.SYM["type"] == "IDENTIFIER":
            node.add_child(self.procedure_function_call())
        else:
            # tidak boleh kosong
            print("Empty statement list encountered") 
            pass

        while self.SYM["type"] == "SEMICOLON":
            node.add_child(self.accept(type="SEMICOLON"))
            self.peek()["type"], self.peek()["value"]
            if self.SYM["type"] == "IDENTIFIER":
                node.add_child(self.assignment_statement())
            elif self.SYM["type"] == "KEYWORD" and self.SYM["value"] == "jika":
                node.add_child(self.if_statement())
            elif self.SYM["type"] == "KEYWORD" and self.SYM["value"] == "selama":
                node.add_child(self.while_statement())
            elif self.SYM["type"] == "KEYWORD" and self.SYM["value"] == "untuk":
                node.add_child(self.for_statement())
            elif self.SYM["type"] == "IDENTIFIER":
                node.add_child(self.procedure_function_call())  
            
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

    #20 <for-statement> -> KEYWORD(untuk) + IDENTIFIER + ASSIGN_OPERATOR + expression + (KEYWORD(ke)/KEYWORD(turun-ke)) + expression + KEYWORD(lakukan ) + statement

    #21 <procedure/function-call> -> IDENTIFIER + (LPARENTHESIS + parameter-list + RPARENTHESIS)
    
    #22 <parameter-list> -> expression + (COMMA + expression)*
    
    #23 <expression> -> simple-expression + (relational-operator + simple-expression)?
    
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

    #26 <factor> -> IDENTIFIER|NUMBER|CHAR_LITERAL|STRING_LITERAL|(LPARENTHESIS + expression + RPARENTHESIS)|LOGICAL_OPERATOR(tidak) + factor|function-call

    #28 <relational-operator> -> =|<>|<|<=|>|>=
    
    #29 <additive-operator> -> +|-|atau
    
    #30 <multiplicative-operator> -> *|/|bagi|mod|dan