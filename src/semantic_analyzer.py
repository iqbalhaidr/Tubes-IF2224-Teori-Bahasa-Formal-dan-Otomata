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
        # 1. tab: Identifier Table
        self.tab = [

            {"idx": 0, "id": "false", "link": -1, "obj": "konstanta", 
            "type": TYPE_BOOLEAN, "ref": -1, "nrm": 0, "lev": 0, "adr": 0, "init": 1},
            
            {"idx": 1, "id": "true", "link": 0, "obj": "konstanta", 
            "type": TYPE_BOOLEAN, "ref": -1, "nrm": 0, "lev": 0, "adr": 1, "init": 1},

            {"idx": 2, "id": "real", "link": 1, "obj": "tipe", 
            "type": TYPE_REAL, "ref": -1, "nrm": 0, "lev": 0, "adr": SIZE_REAL, "init": 1},

            {"idx": 3, "id": "char", "link": 2, "obj": "tipe", 
            "type": TYPE_CHAR, "ref": -1, "nrm": 0, "lev": 0, "adr": SIZE_CHAR, "init": 1},

            {"idx": 4, "id": "boolean", "link": 3, "obj": "tipe", 
            "type": TYPE_BOOLEAN, "ref": -1, "nrm": 0, "lev": 0, "adr": SIZE_BOOLEAN, "init": 1},

            {"idx": 5, "id": "integer", "link": 4, "obj": "tipe", 
            "type": TYPE_INTEGER, "ref": -1, "nrm": 0, "lev": 0, "adr": SIZE_INTEGER, "init": 1},

            {"idx": 6, "id": "abs", "link": 5, "obj": "fungsi", 
            "type": TYPE_REAL, "ref": -1, "nrm": 0, "lev": 0, "adr": 0, "init": 1},
            
            {"idx": 7, "id": "sqr", "link": 6, "obj": "fungsi", 
            "type": TYPE_REAL, "ref": -1, "nrm": 0, "lev": 0, "adr": 2, "init": 1},
            
            {"idx": 8, "id": "odd", "link": 7, "obj": "fungsi", 
            "type": TYPE_BOOLEAN, "ref": -1, "nrm": 0, "lev": 0, "adr": 4, "init": 1},
            
            {"idx": 9, "id": "chr", "link": 8, "obj": "fungsi", 
            "type": TYPE_CHAR, "ref": -1, "nrm": 0, "lev": 0, "adr": 5, "init": 1},
            
            {"idx": 10, "id": "ord", "link": 9, "obj": "fungsi", 
            "type": TYPE_INTEGER, "ref": -1, "nrm": 0, "lev": 0, "adr": 6, "init": 1},
            
            {"idx": 11, "id": "succ", "link": 10, "obj": "fungsi", 
            "type": TYPE_CHAR, "ref": -1, "nrm": 0, "lev": 0, "adr": 7, "init": 1},
            
            {"idx": 12, "id": "pred", "link": 11, "obj": "fungsi", 
            "type": TYPE_CHAR, "ref": -1, "nrm": 0, "lev": 0, "adr": 8, "init": 1},
            
            {"idx": 13, "id": "round", "link": 12, "obj": "fungsi", 
            "type": TYPE_INTEGER, "ref": -1, "nrm": 0, "lev": 0, "adr": 9, "init": 1},
            
            {"idx": 14, "id": "trunc", "link": 13, "obj": "fungsi", 
            "type": TYPE_INTEGER, "ref": -1, "nrm": 0, "lev": 0, "adr": 10, "init": 1},
            
            {"idx": 15, "id": "sin", "link": 14, "obj": "fungsi", 
            "type": TYPE_REAL, "ref": -1, "nrm": 0, "lev": 0, "adr": 11, "init": 1},
            
            {"idx": 16, "id": "cos", "link": 15, "obj": "fungsi", 
            "type": TYPE_REAL, "ref": -1, "nrm": 0, "lev": 0, "adr": 12, "init": 1},
            
            {"idx": 17, "id": "exp", "link": 16, "obj": "fungsi", 
            "type": TYPE_REAL, "ref": -1, "nrm": 0, "lev": 0, "adr": 13, "init": 1},
            
            {"idx": 18, "id": "ln", "link": 17, "obj": "fungsi", 
            "type": TYPE_REAL, "ref": -1, "nrm": 0, "lev": 0, "adr": 14, "init": 1},
            
            {"idx": 19, "id": "sqrt", "link": 18, "obj": "fungsi", 
            "type": TYPE_REAL, "ref": -1, "nrm": 0, "lev": 0, "adr": 15, "init": 1},
            
            {"idx": 20, "id": "arctan", "link": 19, "obj": "fungsi", 
            "type": TYPE_REAL, "ref": -1, "nrm": 0, "lev": 0, "adr": 16, "init": 1},
            
            {"idx": 21, "id": "eof", "link": 20, "obj": "fungsi", 
            "type": TYPE_BOOLEAN, "ref": -1, "nrm": 0, "lev": 0, "adr": 17, "init": 1},
            
            {"idx": 22, "id": "eoln", "link": 21, "obj": "fungsi", 
            "type": TYPE_BOOLEAN, "ref": -1, "nrm": 0, "lev": 0, "adr": 18, "init": 1},

            {"idx": 23, "id": "read", "link": 22, "obj": "prosedur", 
            "type": TYPE_UNDEFINED, "ref": -1, "nrm": 0, "lev": 0, "adr": 1, "init": 1},
            
            {"idx": 24, "id": "readln", "link": 23, "obj": "prosedur", 
            "type": TYPE_UNDEFINED, "ref": -1, "nrm": 0, "lev": 0, "adr": 2, "init": 1},
            
            {"idx": 25, "id": "write", "link": 24, "obj": "prosedur", 
            "type": TYPE_UNDEFINED, "ref": -1, "nrm": 0, "lev": 0, "adr": 3, "init": 1},
            
            {"idx": 26, "id": "writeln", "link": 25, "obj": "prosedur", 
            "type": TYPE_UNDEFINED, "ref": -1, "nrm": 0, "lev": 0, "adr": 4, "init": 1},
            
            # Opsional - jika Anda pakai versi Indonesia
            {"idx": 27, "id": "larik", "link": 26, "obj": "tipe", 
            "type": TYPE_ARRAY, "ref": -1, "nrm": 0, "lev": 0, "adr": 0, "init": 1},
            
            {"idx": 28, "id": "rekaman", "link": 27, "obj": "tipe", 
            "type": TYPE_RECORD, "ref": -1, "nrm": 0, "lev": 0, "adr": 0, "init": 1},
        ]    

        # 2. btab: Block Table (dimulai dengan block global)
        self.btab = [{
            "blocks": 0,
            "last": 28,     # -1 artinya NULL
            "lpar": 0,
            "psze": 0,      # Parameter size
            "vsze": 0       # Variable size (lokal)
        }]
        
        # 3. atab: Array Table
        self.atab = []   

        # Display Stack untuk manajemen scope
        self.display = [0] * 20 
        self.display[0] = 0
        self.level = 0

    # ================= HELPER & TRAVERSAL & ISI ATRIBUT =================
    
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

    # ================= SYMBOL TABLE MANAGEMENT =================

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
        """Membuat block baru, naik level"""
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
        """Turun level"""
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
            # Note: Dalam Pascal standard, variabel lokal boleh memiliki nama sama dengan global
            # Tapi tidak boleh sama dengan variabel lain di level (scope) yang sama.
            # Karena loop lookup kita hanya cek link list block ini, ini sudah benar.
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
            "nrm": nrm,
            "lev": self.level,
            "adr": adr,
            "init": init
        }
        
        self.tab.append(new_entry)

        # Update pointer last di btab
        self.btab[btab_idx]["last"] = new_idx
        
        # Update Variable Size (vsze) jika ini variabel (bukan param, bukan type)
        # if obj == "variabel" and init == 0: 
        #      var_size = self.get_type_size(type_code, ref)
        #      self.btab[btab_idx]["vsze"] += var_size

        return new_idx

    def insert_atab(self, xtyp, etyp, low, high, eref=-1):
        new_idx = len(self.atab)

        elsz = 1 # Simplifikasi size element
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

    # ================= PROGRAM & BLOCKS =================

    def visit_ProgramNode(self, node):
        print(f"--- Analyzing Program: {node.name} ---")
        # Masukkan nama program ke scope global (atau biarkan di luar btab[0])
        # Di contoh spek, program masuk tab.
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

    # ================= DECLARATIONS =================

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
            print(f"const_value: {const_value} ({type(const_value)})")
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
        # node.names bisa list (jika a, b: integer) atau single string tergantung ast_builder
        # Berdasarkan ast_builder visit_var_declaration -> mengembalikan list of VarDeclNode
        # Dimana setiap VarDeclNode.names adalah string tunggal (akibat loop di ast_builder)
        
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
        
        # 1. Insert nama prosedur ke scope saat ini
        proc_idx = self.insert_tab(proc_name, "prosedur", TYPE_UNDEFINED, init=1)
        
        # 2. Masuk Scope Baru (Prosedur)
        blk_idx = self.enter_block()
        self.tab[proc_idx]["ref"] = blk_idx
        
        # 3. Proses Parameter
        # Berdasarkan ast_builder, params adalah list of tuples [(name, type_node), ...]
        param_offset = 5
        total_psze = 0
        for param in node.params: 
            p_name = ""
            p_type_node = None
            p_is_var = False # Default by value
            
            # Handling format tuple dari ast_builder
            if isinstance(param, tuple): # Harusnya udah ga mungkin masuk sini
                p_name, p_type_node = param
            elif isinstance(param, VarDeclNode): # Jaga-jaga jika format berubah
                p_name = param.names
                p_type_node = param.var_type
                p_is_var = param.is_var  # <-- BACA FLAG DARI AST
            
            type_res = self.visit(p_type_node)
            type_code, type_ref = type_res["typecode"], type_res.get("ptr", -1)

            # Tentukan nilai NRM
            # Jika is_var True (pass by ref), nrm = 0
            # Jika is_var False (pass by value), nrm = 1
            nrm_val = 0 if p_is_var else 1
            
            # Masukkan parameter sebagai variabel lokal yang sudah di-init
            self.insert_tab(
                name=p_name, 
                obj="variabel", 
                type_code=type_code, 
                ref=type_ref, 
                init=1,
                nrm=nrm_val # <-- GUNAKAN NILAI INI
            )
            param_size = 1 if not p_is_var else self.get_type_size(type_code, type_ref)
            param_offset += param_size
            total_psze += param_size

        # Update ukuran parameter di btab
        self.btab[blk_idx]["psze"] = total_psze
        
        # Update lastpar di btab
        self.btab[blk_idx]["lpar"] = proc_idx + len(node.params) - 1


        # 4. Proses Deklarasi Lokal & Body
        if node.declarations:
            self.visit(node.declarations)
            
        self.visit(node.body)
        
        # 5. Keluar Scope
        self.exit_block()

        self.decorate(node, type=None, idx=proc_idx, lev=self.level)

    def visit_FunctionDeclNode(self, node):
        func_name = node.name
        
        # 1. Cek Tipe Return
        ret_type_res = self.visit(node.return_type)
        ret_code = ret_type_res["typecode"]
        
        # 2. Insert Fungsi
        func_idx = self.insert_tab(func_name, "fungsi", ret_code, init=1)
        
        # 3. Masuk Scope
        blk_idx = self.enter_block()
        self.tab[func_idx]["ref"] = blk_idx
        
        # 4. Params
        total_psze = 0
        param_offset = 5
        for param in node.params:
            p_name = ""
            p_type_node = None
            p_is_var = False # Default by value
            
            if isinstance(param, tuple): # Harusnya udah ga mungkin masuk sini
                p_name, p_type_node = param
            elif isinstance(param, VarDeclNode):
                p_name = param.names
                p_type_node = param.var_type
                p_is_var = param.is_var  # <-- BACA FLAG DARI AST

            type_res = self.visit(p_type_node)
            type_code, type_ref = type_res["typecode"], type_res.get("ptr", -1)

            # Tentukan nilai NRM
            # Jika is_var True (pass by ref), nrm = 0
            # Jika is_var False (pass by value), nrm = 1
            nrm_val = 0 if p_is_var else 1

            self.insert_tab(p_name, "variabel", type_code, type_ref, init=1, nrm=nrm_val)
            param_size = 1 if not p_is_var else self.get_type_size(type_code, type_ref)
            param_offset += param_size
            total_psze += param_size
            
        self.btab[blk_idx]["psze"] = total_psze

        self.btab[blk_idx]["lpar"] = func_idx + len(node.params) - 1
        
        # 5. Result Variable (Variabel magis nama fungsi)
        # Agar bisa di-assign nilai return: function_name := ...
        self.insert_tab(func_name, "variabel", ret_code, init=0)
        
        if node.declarations:
            self.visit(node.declarations)
            
        self.visit(node.body)
        self.exit_block()

        self.decorate(node, type=ret_code, idx=func_idx, lev=self.level)

    # ================= TYPES =================

    def visit_BuiltinTypeNode(self, node):
        mapping = {
            "integer": TYPE_INTEGER, "real": TYPE_REAL,
            "boolean": TYPE_BOOLEAN, "char": TYPE_CHAR
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
        
        visit_element_type = self.visit(node.info["element_type"])
        atab_idx = self.insert_atab(TYPE_INTEGER, visit_element_type["typecode"], low, high, visit_element_type.get("ptr", -1))
        
        self.decorate(node, type=TYPE_ARRAY, idx=atab_idx, lev=None)
        return {"typecode": TYPE_ARRAY, "ptr": atab_idx}

    def visit_RecordTypeNode(self, node):
        new_idx = self.enter_block() 
        

        # fields is list of tuples (name, type_node) from ast_builder
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

    # ================= STATEMENTS =================

    def visit_AssignNode(self, node):
        visit_value = self.visit(node.value)
        rhs_type = visit_value["typecode"]
        target = node.target
        
        # Helper untuk mencari variabel akar (jika akses array/record)
        root_var = target
        while isinstance(root_var, (ArrayAccessNode, RecordAccessNode)):
            root_var = root_var.var

        if isinstance(root_var, VarNode):
            name = root_var.name
            tab_entry = self.lookup(name)
            if not tab_entry: raise SemanticError(f"Undeclared var '{name}'")
            if tab_entry["obj"] == "konstanta": raise SemanticError(f"Cannot assign to constant '{name}'")
            
            # Jika target adalah variabel langsung (bukan elemen array/record)
            if isinstance(target, VarNode):
                lhs_type = tab_entry["type"]
                if not (lhs_type == TYPE_REAL and rhs_type == TYPE_INTEGER) and lhs_type != rhs_type:
                    raise SemanticError(f"Type mismatch assign '{name}': {lhs_type} := {rhs_type}")
            
            # [PERBAIKAN DISINI]
            # Karena kita tidak memanggil visit_VarNode (takut error uninitialized),
            # Kita harus decorate manual di sini supaya AST-nya cantik.
            self.decorate(target, type=tab_entry["type"], idx=tab_entry["idx"], lev=tab_entry["lev"])

            # Jika target kompleks, validasi tipe dilakukan di visit_Access
            # Tapi kita tandai variabel akar sebagai sudah diinisialisasi
            tab_entry["init"] = 1

        elif isinstance(target, (ArrayAccessNode, RecordAccessNode)):
            # Validasi tipe elemen kiri
            lhs = self.visit(target)
            if lhs["typecode"] != rhs_type:
                 # Allow int to real
                 if not (lhs["typecode"] == TYPE_REAL and rhs_type == TYPE_INTEGER):
                    raise SemanticError("Type mismatch in complex assignment")
        
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
        if entry["type"] != TYPE_INTEGER: raise SemanticError("Loop variable must be integer")
        
        start = self.visit(node.start)
        end = self.visit(node.end)
        
        if start["typecode"] != TYPE_INTEGER or end["typecode"] != TYPE_INTEGER:
             raise SemanticError("For-loop bounds must be integers")
        
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
            
        for branch in node.branches:
            for label in branch.labels:
                lbl_res = self.visit(label)
                if lbl_res["typecode"] != sel_type:
                    raise SemanticError("CASE label type mismatch with selector")
            self.visit(branch.stmt)

        self.decorate(node, type=None, idx=None, lev=self.level)

    def visit_ProcedureCallNode(self, node):
        entry = self.lookup(node.name)
        # Built-in check
        if not entry: 
            if node.name.lower() in ['write', 'writeln', 'read', 'readln']: 
                # Visit args untuk memastikan variabel di dalam argumen valid
                if hasattr(node, 'args') and isinstance(node.args, list):
                    for arg in node.args: self.visit(arg)
                return
            raise SemanticError(f"Undeclared procedure '{node.name}'")
            
        if entry["obj"] != "prosedur": raise SemanticError(f"'{node.name}' is not a procedure")
        
        # Visit args
        if hasattr(node, 'args') and isinstance(node.args, list):
            for arg in node.args: self.visit(arg)

        self.decorate(node, type=None, idx=entry["idx"], lev=entry["lev"])

    # ================= EXPRESSIONS =================

    def visit_BinOpNode(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        
        op = node.op.lower()
        l_type, r_type = left["typecode"], right["typecode"]
        l_val, r_val = left.get("value"), right.get("value")
        
        has_val = (l_val is not None) and (r_val is not None)
        res = {"typecode": TYPE_UNDEFINED}

        # --- ARITHMETIC OPERATORS (Support Bahasa Indonesia) ---
        arith_ops = ['+', '-', '*', 'div', 'mod', '/', 'bagi', 'kali', 'kurang', 'tambah']
        
        if op in arith_ops:
            # Tentukan apakah ini operasi bilangan real
            # 'bagi' atau '/' selalu menghasilkan REAL
            # Jika salah satu operand REAL, hasil REAL (kecuali div/mod)
            is_real_result = (op in ['/', 'bagi']) or (l_type == TYPE_REAL or r_type == TYPE_REAL)
            
            if is_real_result and op not in ['div', 'mod']:
                res["typecode"] = TYPE_REAL
                if has_val:
                    if op in ['+', 'tambah']: res["value"] = l_val + r_val
                    elif op in ['-', 'kurang']: res["value"] = l_val - r_val
                    elif op in ['*', 'kali']: res["value"] = l_val * r_val
                    elif op in ['/', 'bagi']: res["value"] = l_val / r_val if r_val != 0 else 0
            
            # Operasi Integer Murni
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

        # --- RELATIONAL OPERATORS ---
        elif op in ['=', '<>', '<', '>', '<=', '>=']:
            res["typecode"] = TYPE_BOOLEAN 
            # Compatible jika tipe sama atau keduanya numerik (int/real)
            if l_type == r_type or (l_type in [TYPE_INTEGER, TYPE_REAL] and r_type in [TYPE_INTEGER, TYPE_REAL]):
                pass
            else:
                raise SemanticError(f"Cannot compare {l_type} with {r_type}")

        # --- LOGICAL OPERATORS (Support Bahasa Indonesia) ---
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
        
        # Cek Inisialisasi
        if tab_entry["obj"] == "variabel" and tab_entry["init"] == 0:
            raise SemanticError(f"Variable '{node.name}' not initialized yet")
            
        self.decorate(node, type=tab_entry["type"], idx=tab_entry["idx"], lev=None)
        return {
            "typecode": tab_entry["type"],
            "ptr": tab_entry["ref"],
            "value": tab_entry["adr"] # Return value jika ini konstanta
        }

    def visit_FunctionCallNode(self, node):
        entry = self.lookup(node.name)
        if not entry: raise SemanticError(f"Undeclared function '{node.name}'")
        if entry["obj"] != "fungsi": raise SemanticError(f"'{node.name}' is not a function")
        
        if hasattr(node, 'args') and isinstance(node.args, list):
            for arg in node.args: self.visit(arg)
        
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

    # --- LITERALS ---
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
        # Mapping Tipe Data untuk display yang lebih user-friendly
        TYPE_MAP = {
            0: 'UNDEF', 1: 'INT', 2: 'REAL', 3: 'BOOL', 
            4: 'CHAR', 5: 'ARRAY', 6: 'RECORD', 7: 'STR'
        }

        print("\n" + "="*90)
        print(f"{'TAB (Identifier Table)':^90}")
        print("="*90)
        # Header sesuai spesifikasi Hal 12
        # print(f"{'IDX':<5} {'ID':<15} {'OBJ':<10} {'TYPE':<8} {'REF':<5} {'NRM':<5} {'LEV':<5} {'ADR':<10} {'INIT':<5} {'LINK':<5}")
        print(f"{'idx':<5} {'identifiers':<15} {'link':<6} {'obj':<12} {'typ':<8} {'ref':<6} {'nrm':<5} {'lev':<5} {'adr':<10} {'init':<5}")
        print("-" * 90)
        
        for item in self.tab:
            t_str = TYPE_MAP.get(item['type'], str(item['type']))
            # Formatting alignment
            # print(f"{item['idx']:<5} {item['id']:<15} {item['obj']:<10} {t_str:<8} "
            #     f"{item['ref']:<5} {item['nrm']:<5} {item['lev']:<5} {str(item['adr']):<10} "
            #     f"{item['init']:<5} {item['link']:<5}")
            print(f"{item['idx']:<5} {item['id']:<15} {item['link']:<6} {item['obj']:<12} "
                  f"{t_str:<8} {item['ref']:<6} {item['nrm']:<5} {item['lev']:<5} "
                  f"{str(item['adr']):<10} {item['init']:<5}")

        print("\n" + "="*60)
        print(f"{'BTAB (Block Table)':^60}")
        print("="*60)
        # Header sesuai spesifikasi Hal 13
        print(f"{'blocks':<5} {'last':<8} {'lpar':<8} {'psze':<8} {'vsze':<8}")
        print("-" * 60)
        
        for i, item in enumerate(self.btab):
            # Menggunakan index list sebagai IDX block
            print(f"{i:<5} {item['last']:<8} {item['lpar']:<8} {item['psze']:<8} {item['vsze']:<8}")

        print("\n" + "="*80)
        print(f"{'ATAB (Array Table)':^80}")
        print("="*80)
        
        if not self.atab:
            print(" (Empty) ")
        else:
            # Header sesuai spesifikasi Hal 13
            print(f"{'arrays':<5} {'xtyp':<8} {'etyp':<8} {'eref':<6} {'low':<6} {'high':<6} {'elsz':<6} {'size':<6}")
            print("-" * 80)
            
            for item in self.atab:
                xtyp_str = TYPE_MAP.get(item['xtyp'], str(item['xtyp']))
                etyp_str = TYPE_MAP.get(item['etyp'], str(item['etyp']))
                
                print(f"{item['arrays']:<5} {xtyp_str:<8} {etyp_str:<8} {item['eref']:<6} "
                    f"{item['low']:<6} {item['high']:<6} {item['elsz']:<6} {item['size']:<6}")

        print("="*80 + "\n")
