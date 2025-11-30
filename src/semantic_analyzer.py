import sys
from ast_nodes import *

# ================= KST & TIPE DATA =================
TYPE_UNDEFINED = 0
TYPE_INTEGER = 1
TYPE_REAL = 2
TYPE_BOOLEAN = 3
TYPE_CHAR = 4
TYPE_ARRAY = 5
TYPE_RECORD = 6
TYPE_STRING = 7

TYPE_MAP = {
            0: '[0] undef', 1: '[1] int', 2: '[2] real', 3: '[3] boolean', 
            4: '[4] char', 5: '[5] array', 6: '[6] record', 7: '[7] string'
        }

# Size dalam satuan memori abstrak
SIZE_INTEGER = 1
SIZE_REAL = 1
SIZE_BOOLEAN = 1
SIZE_CHAR = 1

class SemanticError(Exception):
    def __init__(self, message):
        super().__init__(message)

class SemanticAnalyzer:
    def __init__(self):
        self.tab = [
            {"idx": 0, "id": "dan", "link": -1, "obj": "keyword", 
            "type": TYPE_UNDEFINED, "ref": -1, "nrm": 0, "lev": -1, "adr": 0, "init": 1},
            
            {"idx": 1, "id": "larik", "link": 0, "obj": "keyword", 
            "type": TYPE_UNDEFINED, "ref": -1, "nrm": 0, "lev": -1, "adr": 0, "init": 1},

            {"idx": 2, "id": "mulai", "link": 1, "obj": "keyword", 
            "type": TYPE_UNDEFINED, "ref": -1, "nrm": 0, "lev": -1, "adr": 0, "init": 1},

            {"idx": 3, "id": "kasus", "link": 2, "obj": "keyword", 
            "type": TYPE_UNDEFINED, "ref": -1, "nrm": 0, "lev": -1, "adr": 0, "init": 1},

            {"idx": 4, "id": "konstanta", "link": 3, "obj": "keyword", 
            "type": TYPE_UNDEFINED, "ref": -1, "nrm": 0, "lev": -1, "adr": 0, "init": 1},

            {"idx": 5, "id": "div", "link": 4, "obj": "keyword", 
            "type": TYPE_UNDEFINED, "ref": -1, "nrm": 0, "lev": -1, "adr": 0, "init": 1},

            {"idx": 6, "id": "turunke", "link": 5, "obj": "keyword", 
            "type": TYPE_UNDEFINED, "ref": -1, "nrm": 0, "lev": -1, "adr": 0, "init": 1},
            
            {"idx": 7, "id": "lakukan", "link": 6, "obj": "keyword", 
            "type": TYPE_UNDEFINED, "ref": -1, "nrm": 0, "lev": -1, "adr": 0, "init": 1},
            
            {"idx": 8, "id": "selainitu", "link": 7, "obj": "keyword", 
            "type": TYPE_UNDEFINED, "ref": -1, "nrm": 0, "lev": -1, "adr": 0, "init": 1},
            
            {"idx": 9, "id": "selesai", "link": 8, "obj": "keyword", 
            "type": TYPE_UNDEFINED, "ref": -1, "nrm": 0, "lev": -1, "adr": 0, "init": 1},
            
            {"idx": 10, "id": "untuk", "link": 9, "obj": "keyword", 
            "type": TYPE_UNDEFINED, "ref": -1, "nrm": 0, "lev": -1, "adr": 0, "init": 1},
            
            {"idx": 11, "id": "fungsi", "link": 10, "obj": "keyword", 
            "type": TYPE_UNDEFINED, "ref": -1, "nrm": 0, "lev": -1, "adr": 0, "init": 1},
            
            {"idx": 12, "id": "jika", "link": 11, "obj": "keyword", 
            "type": TYPE_UNDEFINED, "ref": -1, "nrm": 0, "lev": -1, "adr": 0, "init": 1},
            
            {"idx": 13, "id": "mod", "link": 12, "obj": "keyword", 
            "type": TYPE_UNDEFINED, "ref": -1, "nrm": 0, "lev": -1, "adr": 0, "init": 1},
            
            {"idx": 14, "id": "tidak", "link": 13, "obj": "keyword", 
            "type": TYPE_UNDEFINED, "ref": -1, "nrm": 0, "lev": -1, "adr": 0, "init": 1},
            
            {"idx": 15, "id": "dari", "link": 14, "obj": "keyword", 
            "type": TYPE_UNDEFINED, "ref": -1, "nrm": 0, "lev": -1, "adr": 0, "init": 1},
            
            {"idx": 16, "id": "atau", "link": 15, "obj": "keyword", 
            "type": TYPE_UNDEFINED, "ref": -1, "nrm": 0, "lev": -1, "adr": 0, "init": 1},
            
            {"idx": 17, "id": "prosedur", "link": 16, "obj": "keyword", 
            "type": TYPE_UNDEFINED, "ref": -1, "nrm": 0, "lev": -1, "adr": 0, "init": 1},
            
            {"idx": 18, "id": "program", "link": 17, "obj": "keyword", 
            "type": TYPE_UNDEFINED, "ref": -1, "nrm": 0, "lev": -1, "adr": 0, "init": 1},
            
            {"idx": 19, "id": "rekaman", "link": 18, "obj": "keyword", 
            "type": TYPE_UNDEFINED, "ref": -1, "nrm": 0, "lev": -1, "adr": 0, "init": 1},
            
            {"idx": 20, "id": "ulangi", "link": 19, "obj": "keyword", 
            "type": TYPE_UNDEFINED, "ref": -1, "nrm": 0, "lev": -1, "adr": 0, "init": 1},
            
            {"idx": 21, "id": "string", "link": 20, "obj": "keyword", 
            "type": TYPE_UNDEFINED, "ref": -1, "nrm": 0, "lev": -1, "adr": 0, "init": 1},
            
            {"idx": 22, "id": "maka", "link": 21, "obj": "keyword", 
            "type": TYPE_UNDEFINED, "ref": -1, "nrm": 0, "lev": -1, "adr": 0, "init": 1},

            {"idx": 23, "id": "ke", "link": 22, "obj": "keyword", 
            "type": TYPE_UNDEFINED, "ref": -1, "nrm": 0, "lev": -1, "adr": 0, "init": 1},
            
            {"idx": 24, "id": "tipe", "link": 23, "obj": "keyword", 
            "type": TYPE_UNDEFINED, "ref": -1, "nrm": 0, "lev": -1, "adr": 0, "init": 1},
            
            {"idx": 25, "id": "sampai", "link": 24, "obj": "keyword", 
            "type": TYPE_UNDEFINED, "ref": -1, "nrm": 0, "lev": -1, "adr": 0, "init": 1},
            
            {"idx": 26, "id": "var", "link": 25, "obj": "keyword", 
            "type": TYPE_UNDEFINED, "ref": -1, "nrm": 0, "lev": -1, "adr": 0, "init": 1},
            
            {"idx": 27, "id": "selama", "link": 26, "obj": "keyword", 
            "type": TYPE_UNDEFINED, "ref": -1, "nrm": 0, "lev": -1, "adr": 0, "init": 1},
            
            {"idx": 28, "id": "packed", "link": 27, "obj": "keyword", 
            "type": TYPE_UNDEFINED, "ref": -1, "nrm": 0, "lev": -1, "adr": 0, "init": 1}
        ]    

        # ini block 29 reserved word
        self.btab = [{
            "blocks": 0,
            "last": 28, # -1 artinya NULL
            "lpar": 0,
            "psze": 0,
            "vsze": 0
        }]

        # btab perlu dimasukkin yang baru lagi ga (terpisah dari block keyword)???
        self.btab.append({
            "blocks": 1,
            "last": -1, # -1 artinya NULL
            "lpar": -1,
            "psze": 0,
            "vsze": 0
        })

        self.atab = []   

        self.display = [0] * 20 
        self.display[0] = 1
        self.level = 0
    
    def visit(self, node):
        if node is None:
            return None
        if isinstance(node, list):
            return [self.visit(n) for n in node]
    
        method_name = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)
    
    def generic_visit(self, node):
        raise SemanticError(f"No visit_{node.__class__.__name__} method defined")
    
    def decorate(self, node, type, idx=None, lev=None):
        node.type = type
        if idx is not None:
            node.idx = idx
        if lev is not None:
            node.lev = lev

    def lookup(self, name):
        """Mencari identifier dari scope terdalam (level saat ini) ke global"""
        lev = self.level
        while lev >= 0:
            btab_idx = self.display[lev]
            link = self.btab[btab_idx]["last"]
            
            while link != -1:
                record = self.tab[link]
                if record["id"] == name:
                    return record
                link = record["link"]
            lev -= 1
        return None

    def lookup_block(self, name, btab_idx):
        """Mencari identifier spesifik di blok tertentu (untuk Record field)"""
        if btab_idx >= len(self.btab): return None
        
        link = self.btab[btab_idx]["last"]
        while link != -1:
            record = self.tab[link]
            if record["id"] == name:
                return record
            link = record["link"]
        return None

    def enter_block(self):
        new_idx = len(self.btab)
        self.btab.append({
            "blocks": new_idx,
            "last": -1,
            "lpar": 0,
            "psze": 0,
            "vsze": 0
        })
        self.level += 1
        self.display[self.level] = new_idx
        return new_idx

    def exit_block(self):
        self.level -= 1

    def get_type_size(self, type_code, type_ref=-1):
        """Mengembalikan unit size memori untuk tipe data tertentu."""
        if type_code == TYPE_INTEGER:
            return SIZE_INTEGER
        elif type_code == TYPE_REAL:
            return SIZE_REAL
        elif type_code == TYPE_BOOLEAN:
            return SIZE_BOOLEAN
        elif type_code == TYPE_CHAR:
            return SIZE_CHAR
        elif type_code == TYPE_STRING:
            return SIZE_CHAR * 256 # INI BELOM JADI WOY, HARUSNYA GA GINI
        elif type_code == TYPE_ARRAY:
            if type_ref != -1 and type_ref < len(self.atab):
                return self.atab[type_ref]["size"]
            raise SemanticError(f"Referensi array tidak valid (ref: {type_ref}) saat menghitung ukuran.")
        elif type_code == TYPE_RECORD:
            if type_ref != -1 and type_ref < len(self.btab):
                return self.btab[type_ref]["vsze"]
            raise SemanticError(f"Referensi record tidak valid (ref: {type_ref}) saat menghitung ukuran.")
        return 0

    def insert_tab(self, name, obj, type_code, ref=-1, nrm=1, adr=0, init=0):
        btab_idx = self.display[self.level]
        link_head = self.btab[btab_idx]["last"]
        
        # Cek duplikasi di scope yang sama
        curr = link_head
        while curr != -1:
            if self.tab[curr]["id"] == name:
                raise SemanticError(f"Duplicate identifier '{name}' in current scope")
            curr = self.tab[curr]["link"]

        new_idx = len(self.tab)
        
        new_entry = {
            "idx": new_idx,
            "id": name,
            "link": link_head,
            "obj": obj,        
            "type": type_code,
            "ref": ref,
            "nrm": nrm, # 1 normal, 0 by-reference
            "lev": self.level,
            "adr": adr,
            "init": init
        }
        
        self.tab.append(new_entry)
        self.btab[btab_idx]["last"] = new_idx

        return new_idx

    def insert_atab(self, xtyp, etyp, low, high, eref=-1):
        new_idx = len(self.atab)

        elsz = self.get_type_size(type_code=etyp, type_ref=eref)
        size = (high - low + 1) * elsz
        
        self.atab.append({
            "arrays": new_idx,
            "xtyp": xtyp,
            "etyp": etyp,
            "eref": eref,
            "low": low,
            "high": high,
            "elsz": elsz,
            "size": size
        })
        return new_idx

    def get_parameter_indexes(self, proc_or_func_tab_idx):
        if proc_or_func_tab_idx < 0 or proc_or_func_tab_idx >= len(self.tab):
            raise SemanticError(f"Invalid tab idx for procedure/function in get_parameter_count()")
        
        entry = self.tab[proc_or_func_tab_idx]

        if entry["obj"] not in ["prosedur", "fungsi"]:
            raise SemanticError(f"error tab idx is not procedure/function in get_parameter_count()")
        
        lpar = self.btab[entry["ref"]]["lpar"]
        indexes = []

        while lpar != -1:
            tab_entry = self.tab[lpar]
            indexes.append(lpar)
            lpar = tab_entry["link"]
        
        indexes.reverse()
        return indexes

    def visit_ProgramNode(self, node):
        tab_idx = self.insert_tab(node.name, "program", TYPE_UNDEFINED, init=1)
        
        if node.declarations:
            self.visit(node.declarations)
        
        if node.block:
            self.visit(node.block)
        
        self.decorate(node, type=None, idx=tab_idx, lev=self.level)

    def visit_BlockNode(self, node):
        self.visit(node.statements)
        
        btab_idx = self.display[self.level]
        self.decorate(node, type=None, idx=btab_idx, lev=self.level)

    def visit_ConstDeclNode(self, node):
        visit_value = self.visit(node.value)
        
        if "value" not in visit_value or visit_value["value"] is None:
            raise SemanticError(f"Constant '{node.name}' value cannot be evaluated at compile time")
        
        const_type = visit_value["typecode"]
        const_value = visit_value["value"]
        final_adr = 0
        # print(f"const_value: {const_value} ({type(const_value)})")
        if const_type == TYPE_STRING:
            final_adr = len(const_value.strip("'"))  # Simplifikasi: alamat = panjang string
        elif const_type == TYPE_CHAR:
            # print(f"const_value: {const_value} ({type(const_value)})")
            final_adr = ord(const_value.strip("'"))   # Alamat = kode ASCII (cdc tuwir ga ada lowercase jadi tentatif)
        else:
            final_adr = round(const_value) & 0xFFFFFFFF # kalau desimal buletin jd integer, kalau negatif jadi positif pake two's complement

        tab_idx = self.insert_tab(
            name=node.name, 
            obj="konstanta", 
            type_code=visit_value["typecode"], 
            adr=final_adr, 
            init=1
        )

        self.decorate(node, type=visit_value["typecode"], idx=tab_idx, lev=self.level)

    def visit_VarDeclNode(self, node):
        var_name = node.names
        
        visit_var_type = self.visit(node.var_type)
        type_code = visit_var_type["typecode"]
        ref = visit_var_type.get("ptr", -1)

        initial_offset = 5
        # kalo var lokal, offset awal + param size
        if self.btab[self.display[self.level]]["psze"] > 0:
            initial_offset += self.btab[self.display[self.level]]["psze"]
        
        block_offset = self.btab[self.display[self.level]]["vsze"]
        final_addr = initial_offset + block_offset

        tab_idx = self.insert_tab(
            name=var_name, 
            obj="variabel", 
            type_code=type_code, 
            ref=ref, 
            adr=final_addr,
            init=0 
        )

        self.decorate(node, type=type_code, idx=tab_idx, lev=self.level)
        var_size = self.get_type_size(type_code, ref)
        self.btab[self.display[self.level]]["vsze"] += var_size

    def visit_TypeDeclNode(self, node):
        visit_type_node = self.visit(node.type_node)
        type_code = visit_type_node["typecode"]
        ref = visit_type_node.get("ptr", -1)
        type_size = self.get_type_size(type_code, ref)
        tab_idx = self.insert_tab(
            name=node.name,
            obj="tipe",
            type_code=visit_type_node["typecode"],
            ref=visit_type_node.get("ptr", -1),
            adr=type_size,
            init=1 
        )

        self.decorate(node, type=visit_type_node["typecode"], idx=tab_idx, lev=self.level)

    def visit_ProcedureDeclNode(self, node):
        proc_name = node.name

        proc_idx = self.insert_tab(proc_name, "prosedur", TYPE_UNDEFINED, init=1)
    
        blk_idx = self.enter_block()
        self.tab[proc_idx]["ref"] = blk_idx
        
        param_offset = 5
        total_psze = 0
        last_param_idx = -1  # Track the last parameter index
        for param in node.params: 
            p_name = ""
            p_type_node = None
            p_is_var = False 
            
            if isinstance(param, tuple): # Harusnya udah ga mungkin masuk sini
                p_name, p_type_node = param
            elif isinstance(param, VarDeclNode): # Jaga-jaga jika format berubah
                p_name = param.names
                p_type_node = param.var_type
                p_is_var = param.is_var
            
            type_res = self.visit(p_type_node)
            type_code, type_ref = type_res["typecode"], type_res.get("ptr", -1)
            nrm_val = 0 if p_is_var else 1

            last_param_idx = self.insert_tab(
                name=p_name, 
                obj="variabel", 
                type_code=type_code, 
                ref=type_ref, 
                init=1,
                nrm=nrm_val,
                adr=param_offset # adr dari parameter
            )
            param_size = 1 if p_is_var else self.get_type_size(type_code, type_ref)
            param_offset += param_size
            total_psze += param_size

        self.btab[blk_idx]["psze"] = total_psze
        self.btab[blk_idx]["lpar"] = last_param_idx

        if node.declarations:
            self.visit(node.declarations)
            
        self.visit(node.body)
        self.exit_block()
        self.decorate(node, type=None, idx=proc_idx, lev=self.level)

    def visit_FunctionDeclNode(self, node):
        func_name = node.name

        ret_type_res = self.visit(node.return_type)
        ret_code = ret_type_res["typecode"]

        func_idx = self.insert_tab(func_name, "fungsi", ret_code, init=1)

        blk_idx = self.enter_block()
        self.tab[func_idx]["ref"] = blk_idx

        total_psze = 0
        param_offset = 5
        last_param_idx = -1  # Track the last parameter index
        for param in node.params:
            p_name = ""
            p_type_node = None
            p_is_var = False
            
            if isinstance(param, tuple): # Harusnya udah ga mungkin masuk sini
                p_name, p_type_node = param
            elif isinstance(param, VarDeclNode):
                p_name = param.names
                p_type_node = param.var_type
                p_is_var = param.is_var

            type_res = self.visit(p_type_node)
            type_code, type_ref = type_res["typecode"], type_res.get("ptr", -1)
            nrm_val = 0 if p_is_var else 1

            last_param_idx = self.insert_tab(p_name, "variabel", type_code, type_ref, init=1, nrm=nrm_val, adr=param_offset)
            param_size = 1 if p_is_var else self.get_type_size(type_code, type_ref)
            param_offset += param_size
            total_psze += param_size
            
        self.btab[blk_idx]["psze"] = total_psze
        self.btab[blk_idx]["lpar"] = last_param_idx
        
        if node.declarations:
            self.visit(node.declarations)
            
        self.visit(node.body)
        self.exit_block()
        self.decorate(node, type=ret_code, idx=func_idx, lev=self.level)

    def visit_BuiltinTypeNode(self, node):
        mapping = {
            "integer": TYPE_INTEGER, "real": TYPE_REAL,
            "boolean": TYPE_BOOLEAN, "char": TYPE_CHAR,
            "string" : TYPE_STRING
        }

        typecode = mapping.get(node.info, TYPE_UNDEFINED)
        self.decorate(node, type=typecode, idx=None, lev=None)
        return {"typecode": typecode}

    def visit_CustomTypeNode(self, node):
        tab_entry = self.lookup(node.info)
        if not tab_entry:
            raise SemanticError(f"Undeclared type: {node.info}")
        if tab_entry["obj"] != "tipe":
            raise SemanticError(f"{node.info} is not a type identifier")
        self.decorate(node, type=tab_entry["type"], idx=tab_entry["idx"], lev=tab_entry["lev"])
        return {"typecode": tab_entry["type"], "ptr": tab_entry["ref"]}

    def visit_ArrayTypeNode(self, node):
        visit_low = self.visit(node.info["low"])
        visit_high = self.visit(node.info["high"])
        
        if visit_low["typecode"] != TYPE_INTEGER or visit_high["typecode"] != TYPE_INTEGER:
             raise SemanticError("Array bounds must be integer")
        
        if "value" not in visit_low or "value" not in visit_high:
            raise SemanticError("Array bounds must be constant expressions")
            
        low = visit_low["value"]
        high = visit_high["value"]

        if low > high:
            raise SemanticError("Invalid array bound value (left must be smaller than right)")
        
        visit_element_type = self.visit(node.info["element_type"])
        atab_idx = self.insert_atab(TYPE_INTEGER, visit_element_type["typecode"], low, high, visit_element_type.get("ptr", -1))
        
        self.decorate(node, type=TYPE_ARRAY, idx=atab_idx, lev=None)
        return {"typecode": TYPE_ARRAY, "ptr": atab_idx}

    def visit_RecordTypeNode(self, node):
        new_idx = self.enter_block() 
        
        for name, type_node in node.info:
            visit_type_node = self.visit(type_node)
            type_code, ref = visit_type_node["typecode"], visit_type_node.get("ptr", -1)
            current_adr = self.btab[new_idx]["vsze"]
            self.insert_tab(name=name, 
                            obj="variabel", 
                            type_code=type_code, 
                            ref=ref, 
                            adr=current_adr, 
                            init=1)
            field_size = self.get_type_size(type_code, ref)
            self.btab[new_idx]["vsze"] += field_size

        self.exit_block() 
        self.decorate(node, type=TYPE_RECORD, idx=new_idx, lev=None)
        return {"typecode": TYPE_RECORD, "ptr": new_idx}

    def visit_AssignNode(self, node):
        visit_value = self.visit(node.value)
        rhs_ptr = None
        try:
            rhs_ptr = visit_value['ptr']
        except:
            rhs_ptr = -1

        rhs_type = visit_value["typecode"]
        target = node.target
        
        # Case 1: Complex Access (Array[...] or Record.Field)
        if isinstance(target, (ArrayAccessNode, RecordAccessNode)):
            # mark init dulu supaya ga error saat LHS traversal
            root_var = target
            while isinstance(root_var, (ArrayAccessNode, RecordAccessNode)):
                root_var = root_var.var
            
            if isinstance(root_var, VarNode):
                tab_entry = self.lookup(root_var.name)
                if tab_entry:
                    tab_entry["init"] = 1 # Mark initialized because we are writing to it
            lhs = self.visit(target) 
            lhs_name = TYPE_MAP.get(lhs['typecode'], 'unknown')
            rhs_name = TYPE_MAP.get(rhs_type, 'unknown')

            if lhs["typecode"] != rhs_type or lhs['ptr'] != rhs_ptr:
                 # Allow assigning Int to Real
                 if not (lhs["typecode"] == TYPE_REAL and rhs_type == TYPE_INTEGER):
                    raise SemanticError(f"Type mismatch in assignment: {lhs_name} := {rhs_name}, if it was a record it might be a different record")
            
            # Mark the root variable as initialized
            root_var = target
            while isinstance(root_var, (ArrayAccessNode, RecordAccessNode)):
                root_var = root_var.var
            
            if isinstance(root_var, VarNode):
                tab_entry = self.lookup(root_var.name)
                if tab_entry:
                    tab_entry["init"] = 1
                    
        # Case 2: Simple Variable Assignment (x := 5)
        elif isinstance(target, VarNode):
            name = target.name
            tab_entry = self.lookup(name)
            if not tab_entry: raise SemanticError(f"Undeclared identifier '{name}'")
            
            # Subcase A: Function Return Value Assignment
            if tab_entry["obj"] == "fungsi":
                # Check scope (must be inside the function)
                current_scope_idx = self.display[self.level]
                if tab_entry["ref"] != current_scope_idx:
                     raise SemanticError(f"Cannot assign to function '{name}' outside its block")
                
                lhs_type = tab_entry["type"]
                if not (lhs_type == TYPE_REAL and rhs_type == TYPE_INTEGER) and lhs_type != rhs_type:
                    raise SemanticError(f"Return type mismatch for '{name}'")
                
                self.decorate(target, type=lhs_type, idx=tab_entry["idx"], lev=tab_entry["lev"])

            # Subcase B: Standard Variable
            elif tab_entry["obj"] == "variabel":
                if tab_entry["obj"] == "konstanta": 
                    raise SemanticError(f"Cannot assign to constant '{name}'")
                
                tab_entry["init"] = 1 #early mark init to make lhs no eror when visited
                lhs_type = tab_entry["type"]
                lhs_value = self.visit(node.target)
                # print(lhs_value)
                # print("diatas ini lhs")
                lhs_ptr = lhs_value['ptr']
                if not (lhs_type == TYPE_REAL and rhs_type == TYPE_INTEGER) and lhs_type != rhs_type  :
                    # print(lhs_type)
                    # print(rhs_type)
                    tab_entry["init"] = 0
                    raise SemanticError(f"Type mismatch assign '{name}': {lhs_type} := {rhs_type}")
                elif (lhs_ptr != rhs_ptr):
                    raise SemanticError(f"Type mismatch in assignment: {lhs_value['typecode']} := {rhs_type}, if it was a record it might be a different record")
                self.decorate(target, type=lhs_type, idx=tab_entry["idx"], lev=tab_entry["lev"])
            
            else:
                raise SemanticError(f"Cannot assign to {tab_entry['obj']} '{name}'")
        
        self.decorate(node, type=TYPE_UNDEFINED, idx=None, lev=None)

    def visit_IfNode(self, node):
        cond = self.visit(node.cond)
        if cond["typecode"] != TYPE_BOOLEAN:
            raise SemanticError("IF condition must be boolean")
        self.visit(node.then_stmt)
        if node.else_stmt: self.visit(node.else_stmt)
        self.decorate(node, type=None, idx=None, lev=self.level)

    def visit_WhileNode(self, node):
        cond = self.visit(node.cond)
        if cond["typecode"] != TYPE_BOOLEAN:
            raise SemanticError("WHILE condition must be boolean")
        self.visit(node.body)

        self.decorate(node, type=None, idx=None, lev=self.level)

    def visit_ForNode(self, node):
        entry = self.lookup(node.var)
        if not entry: raise SemanticError(f"Undeclared loop variable '{node.var}'")
        if entry["type"] != TYPE_INTEGER: raise SemanticError("Loop variable must be integer") # Only support integer (char and bool not currently supported)
        
        start = self.visit(node.start)
        end = self.visit(node.end)
        
        if start["typecode"] != TYPE_INTEGER or end["typecode"] != TYPE_INTEGER:
             raise SemanticError("For-loop bounds must be integers")
        
        if entry["obj"] != "variabel":
            raise SemanticError(f"Loop variable '{node.var}' must be a variable")

        entry["init"] = 1
        self.visit(node.body)

        self.decorate(node, type=None, idx=None, lev=self.level)

    def visit_RepeatNode(self, node):
        self.visit(node.body) 
        until = self.visit(node.until)
        if until["typecode"] != TYPE_BOOLEAN:
            raise SemanticError("REPEAT-UNTIL condition must be boolean")
        
        self.decorate(node, type=None, idx=None, lev=self.level)

    def visit_CaseNode(self, node):
        selector = self.visit(node.expr)
        sel_type = selector["typecode"]
        
        if sel_type not in [TYPE_INTEGER, TYPE_CHAR, TYPE_BOOLEAN]:
            raise SemanticError("CASE selector must be ordinal type (int, char, bool)")
        
        used_labels = set()

        for branch in node.branches:
            for label in branch.labels:
                lbl_res = self.visit(label)
                if lbl_res["typecode"] != sel_type:
                    raise SemanticError("CASE label type mismatch with selector")

                if "value" in lbl_res:
                    lbl_value = lbl_res["value"]
                    if lbl_value in used_labels:
                        raise SemanticError("Duplicate CASE label value")
                    used_labels.add(lbl_value)
                    
            self.visit(branch.stmt)

        self.decorate(node, type=None, idx=None, lev=self.level)

    def visit_ProcedureCallNode(self, node):
        entry = self.lookup(node.name)
        # Built-in check
        if not entry: 
            raise SemanticError(f"Undeclared procedure '{node.name}'")
            
        if entry["obj"] != "prosedur": raise SemanticError(f"'{node.name}' is not a procedure")
        
        params_indexes = self.get_parameter_indexes(entry["idx"])

        if len(node.args) != len(params_indexes):
            raise SemanticError("Argument count mismatch")

        # Visit args
        if hasattr(node, 'args') and isinstance(node.args, list):
            ctr = 0
            for arg in node.args: 
                param_entry = self.tab[params_indexes[ctr]]

                # Check VAR parameter (Reference)
                if param_entry["nrm"] == 0:
                    if not isinstance(arg, (VarNode, ArrayAccessNode, RecordAccessNode)): # Must pass a variable, not a literal value
                        raise SemanticError("VAR parameter must be a variable")
                    
                    if isinstance(arg, VarNode):
                        arg_entry = self.lookup(arg.name)
                        if not arg_entry:
                            raise SemanticError(f"Undeclared identifier '{arg.name}'")
                        
                        visit_arg = {
                            "typecode": arg_entry["type"],
                            "ptr": arg_entry["ref"]
                        }
                        
                        # Mark as initialized after the call (VAR param can initialize it)
                        arg_entry["init"] = 1
                        self.decorate(arg, type=arg_entry["type"], idx=arg_entry["idx"], lev=arg_entry["lev"])
                    else:
                        # For complex access (array/record), visit normally
                        visit_arg = self.visit(arg)
                else:
                    # Normal value parameter - must be initialized
                    visit_arg = self.visit(arg)

                # Check Type Mismatch
                if visit_arg["typecode"] != param_entry["type"]:
                    # Handle Int->Real implicit conversion if allowed
                    if not (param_entry["type"] == TYPE_REAL and visit_arg["typecode"] == TYPE_INTEGER):
                        raise SemanticError(f"Type mismatch for param {param_entry['id']}")
                    
                ctr += 1

        self.decorate(node, type=None, idx=entry["idx"], lev=entry["lev"])

    def visit_BinOpNode(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        
        op = node.op.lower()
        l_type, r_type = left["typecode"], right["typecode"]
        l_val, r_val = left.get("value"), right.get("value")
        
        has_val = (l_val is not None) and (r_val is not None)
        res = {"typecode": TYPE_UNDEFINED}

        arith_ops = ['+', '-', '*', 'div', 'mod', '/', 'bagi', 'kali', 'kurang', 'tambah']
        
        if op in arith_ops:
            # 'bagi' atau '/' selalu menghasilkan REAL
            # Jika salah satu operand REAL, hasil REAL (kecuali div/mod)
            is_real_result = (op in ['/']) or (l_type == TYPE_REAL or r_type == TYPE_REAL)
            
            if is_real_result:
                res["typecode"] = TYPE_REAL
                if has_val:
                    if op in ['+', 'tambah']: res["value"] = l_val + r_val
                    elif op in ['-', 'kurang']: res["value"] = l_val - r_val
                    elif op in ['*', 'kali']: res["value"] = l_val * r_val
                    elif op in ['/']: res["value"] = l_val / r_val if r_val != 0 else 0
            
            elif l_type == TYPE_INTEGER and r_type == TYPE_INTEGER:
                res["typecode"] = TYPE_INTEGER
                if has_val:
                    if op in ['+', 'tambah']: res["value"] = l_val + r_val
                    elif op in ['-', 'kurang']: res["value"] = l_val - r_val
                    elif op in ['*', 'kali']: res["value"] = l_val * r_val
                    elif op == 'div': res["value"] = l_val // r_val if r_val != 0 else 0
                    elif op == 'mod': res["value"] = l_val % r_val if r_val != 0 else 0
            else:
                raise SemanticError(f"Invalid operand types for '{op}'")

        elif op in ['=', '<>', '<', '>', '<=', '>=']:
            res["typecode"] = TYPE_BOOLEAN 
            # Compatible jika tipe sama atau keduanya numerik (int/real)
            if l_type == r_type or (l_type in [TYPE_INTEGER, TYPE_REAL] and r_type in [TYPE_INTEGER, TYPE_REAL]):
                pass
            else:
                raise SemanticError(f"Cannot compare {l_type} with {r_type}")

        elif op in ['and', 'or', 'dan', 'atau']:
            if l_type == TYPE_BOOLEAN and r_type == TYPE_BOOLEAN:
                res["typecode"] = TYPE_BOOLEAN
                if has_val:
                    if op in ['and', 'dan']: res["value"] = l_val and r_val
                    else: res["value"] = l_val or r_val
            else:
                raise SemanticError("Logical operators require booleans")
        
        self.decorate(node, type=res["typecode"], idx=None, lev=None)
        return res

    def visit_UnaryOpNode(self, node):
        res = self.visit(node.expr)
        op = node.operand.lower()
        
        has_val = res.get("value") is not None
        final_res = {"typecode": res["typecode"]}

        if op == '-':
            if res["typecode"] not in [TYPE_INTEGER, TYPE_REAL]:
                raise SemanticError("Unary minus requires numeric")
            if has_val: final_res["value"] = -res["value"]
            
        elif op in ['not', 'tidak']:
            if res["typecode"] != TYPE_BOOLEAN:
                raise SemanticError("NOT requires boolean")
            if has_val: final_res["value"] = not res["value"]
            
        self.decorate(node, type=final_res["typecode"], idx=None, lev=None)
        return final_res

    def visit_VarNode(self, node):
        tab_entry = self.lookup(node.name)
        if not tab_entry: raise SemanticError(f"Undeclared identifier '{node.name}'")
        
        obj_type = tab_entry["obj"]

        if obj_type == "fungsi":
            raise SemanticError(f"Function '{node.name}' requires parentheses")
        # Cek Inisialisasi
        if obj_type == "variabel" and tab_entry["init"] == 0:
            raise SemanticError(f"Variable '{node.name}' not initialized yet")
            
        self.decorate(node, type=tab_entry["type"], idx=tab_entry["idx"], lev=None)

        result =  {
            "typecode": tab_entry["type"],
            "ptr": tab_entry["ref"]
        }

        # Only include "value" for constants (compile-time known values)
        if obj_type == "konstanta":
            result["value"] = tab_entry["adr"]
        
        return result

    def visit_FunctionCallNode(self, node):
        entry = self.lookup(node.name)
        if not entry: raise SemanticError(f"Undeclared function '{node.name}'")
        if entry["obj"] != "fungsi": raise SemanticError(f"'{node.name}' is not a function")
        
        params_indexes = self.get_parameter_indexes(entry["idx"])
        if len(node.args) != len(params_indexes):
            raise SemanticError("Argument count mismatch")

        # Visit args
        if hasattr(node, 'args') and isinstance(node.args, list):
            ctr = 0
            for arg in node.args: 
                param_entry = self.tab[params_indexes[ctr]]

                # For VAR parameters, skip initialization check
                if param_entry["nrm"] == 0:  # VAR parameter
                    if not isinstance(arg, (VarNode, ArrayAccessNode, RecordAccessNode)):
                        raise SemanticError(f"VAR parameter '{param_entry['id']}' requires a variable")
                    
                    if isinstance(arg, VarNode):
                        arg_entry = self.lookup(arg.name)
                        if not arg_entry:
                            raise SemanticError(f"Undeclared identifier '{arg.name}'")
                        
                        visit_arg = {
                            "typecode": arg_entry["type"],
                            "ptr": arg_entry["ref"]
                        }
                        
                        arg_entry["init"] = 1  # Mark as initialized
                        self.decorate(arg, type=arg_entry["type"], idx=arg_entry["idx"], lev=arg_entry["lev"])
                    else:
                        visit_arg = self.visit(arg)
                else:
                    visit_arg = self.visit(arg)

                # Check Type Mismatch
                if visit_arg["typecode"] != param_entry["type"]:
                    # Handle Int->Real implicit conversion if allowed
                    if not (param_entry["type"] == TYPE_REAL and visit_arg["typecode"] == TYPE_INTEGER):
                        raise SemanticError(f"Type mismatch for param {param_entry['id']}")
                    
                ctr += 1
        
        self.decorate(node, type=entry["type"], idx=entry["idx"], lev=entry["lev"])
        return {"typecode": entry["type"]} 

    def visit_ArrayAccessNode(self, node):
        visit_var = self.visit(node.var)
        if visit_var["typecode"] != TYPE_ARRAY:
            raise SemanticError("Indexing on non-array variable")
            
        visit_index = self.visit(node.index)
        atab_idx = visit_var["ptr"]
        
        if atab_idx < 0 or atab_idx >= len(self.atab):
            raise SemanticError("Invalid array table reference")
            
        atab_entry = self.atab[atab_idx]
        if visit_index["typecode"] != atab_entry["xtyp"]:
            raise SemanticError("Array index type mismatch")
        
        if "value" in visit_index and visit_index["value"] is not None:
            idx_val = visit_index["value"]

            # If the index type is CHAR, convert to ASCII int for comparison
            # because atab usually stores low/high as integers.
            # Disclaimer: seharusnya tidak akan masuk sini, karena dibatasi index hanya bisa TYPE_INTEGER
            if visit_index["typecode"] == TYPE_CHAR:
                if isinstance(idx_val, str):
                    idx_val = ord(idx_val[0])

            if idx_val < atab_entry["low"] or idx_val > atab_entry["high"]:
                raise SemanticError(
                    f"Array index out of bounds. Got {idx_val}, "
                    f"expected range {atab_entry['low']}..{atab_entry['high']}"
                )
            
        self.decorate(node, type=None, idx=atab_idx, lev=None)
        return {"typecode": atab_entry["etyp"], "ptr": atab_entry["eref"]}

    def visit_RecordAccessNode(self, node):
        visit_var = self.visit(node.var)
        btab_idx = visit_var["ptr"]
        
        if visit_var["typecode"] != TYPE_RECORD:
             raise SemanticError("Accessing field of non-record")
        
        if btab_idx < 0 or btab_idx >= len(self.btab):
             raise SemanticError("Invalid block table reference for record")

        # Lookup field di scope record (btab record)
        lookup_field = self.lookup_block(node.field, btab_idx)

        if lookup_field is None:
            raise SemanticError(f"Field '{node.field}' not found in record")
        
        self.decorate(node, type=None, idx=btab_idx, lev=lookup_field["idx"])
        return {"typecode": lookup_field["type"], "ptr": lookup_field["ref"]}

    def visit_NumberNode(self, node):
        tc = TYPE_REAL if isinstance(node.value, float) else TYPE_INTEGER
        self.decorate(node, type=tc, idx=None, lev=None)
        return {"typecode": tc, "value": node.value}

    def visit_StringNode(self, node):
        self.decorate(node, type=TYPE_STRING, idx=None, lev=None)
        return {"typecode": TYPE_STRING, "value": node.value}

    def visit_CharNode(self, node):
        self.decorate(node, type=TYPE_CHAR, idx=None, lev=None)
        return {"typecode": TYPE_CHAR, "value": node.value}

    def visit_BooleanNode(self, node):
        self.decorate(node, type=TYPE_BOOLEAN, idx=None, lev=None)
        return {"typecode": TYPE_BOOLEAN, "value": node.value}
    
# ================= PRINT TABLES FUNCTION =================
    def print_all_tables(self):

        OBJ_MAP = {
            'konstanta': '[0] konstanta',
            'variabel':  '[1] variabel',
            'tipe':      '[2] tipe',
            'prosedur':  '[3] prosedur',
            'fungsi':    '[4] fungsi',
            'program':   '[5] program',
            'keyword':   '[6] keyword'
        }

        w_id  = len('identifiers')
        for item in self.tab:
            w_id  = max(w_id, len(item['id']))
        w_id  += 2
        t_len = 85 + w_id

        print("\n" + "="*t_len)
        print(f"{'TAB (Identifier Table)':^{t_len}}")
        print("="*t_len)
        print(f"{'idx':<5} {'identifiers':<{w_id}} {'link':<6} {'obj':<15} {'type':<14} {'ref':<6} {'nrm':<5} {'lev':<5} {'adr':<10} {'init':<5}")
        print("-" * t_len)
        
        for item in self.tab:
            t_str = TYPE_MAP.get(item['type'], str(item['type']))
            o_str = OBJ_MAP.get(item['obj'], str(item['obj']))
            print(f"{item['idx']:<5} {item['id']:<{w_id}} {item['link']:<6} {o_str:<15} "
                  f"{t_str:<14} {item['ref']:<6} {item['nrm']:<5} {item['lev']:<5} "
                  f"{str(item['adr']):<10} {item['init']:<5}")

        print("\n" + "="*60)
        print(f"{'BTAB (Block Table)':^60}")
        print("="*60)
        print(f"{'blocks':<8} {'last':<8} {'lpar':<8} {'psze':<8} {'vsze':<8}")
        print("-" * 60)
        
        for i, item in enumerate(self.btab):
            print(f"{i:<8} {item['last']:<8} {item['lpar']:<8} {item['psze']:<8} {item['vsze']:<8}")

        print("\n" + "="*80)
        print(f"{'ATAB (Array Table)':^80}")
        print("="*80)
        
        if not self.atab:
            print(" (Empty) ")
        else:
            print(f"{'arrays':<8} {'xtyp':<8} {'etyp':<8} {'eref':<6} {'low':<6} {'high':<6} {'elsz':<6} {'size':<6}")
            print("-" * 80)
            
            for item in self.atab:
                xtyp_str = TYPE_MAP.get(item['xtyp'], str(item['xtyp']))
                etyp_str = TYPE_MAP.get(item['etyp'], str(item['etyp']))
                
                print(f"{item['arrays']:<8} {xtyp_str:<8} {etyp_str:<8} {item['eref']:<6} "
                    f"{item['low']:<6} {item['high']:<6} {item['elsz']:<6} {item['size']:<6}")

        print("="*80 + "\n")

    def print_tab_entries(self, indexes):
        """Print specific tab entries for debugging"""
        TYPE_MAP = {
            0: 'undef', 1: 'int', 2: 'real', 3: 'bool', 
            4: 'char', 5: 'array', 6: 'record', 7: 'string'
        }
        
        print("\n" + "="*100)
        print(f"DEBUG: Tab Entries {indexes}")
        print("="*100)
        print(f"{'idx':<5} {'id':<15} {'link':<6} {'obj':<12} {'type':<10} {'ref':<5} {'nrm':<5} {'lev':<5} {'adr':<6} {'init':<5}")
        print("-"*100)
        
        for idx in indexes:
            if idx < 0 or idx >= len(self.tab):
                print(f"{idx:<5} [OUT OF BOUNDS]")
                continue
                
            item = self.tab[idx]
            t_str = TYPE_MAP.get(item['type'], str(item['type']))
            
            print(f"{item['idx']:<5} {item['id']:<15} {item['link']:<6} {item['obj']:<12} "
                f"{t_str:<10} {item['ref']:<5} {item['nrm']:<5} {item['lev']:<5} "
                f"{item['adr']:<6} {item['init']:<5}")
        print("="*100 + "\n")