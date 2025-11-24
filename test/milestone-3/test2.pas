program CekScope;

variabel
  globalVar: integer;

prosedur hitung(param: integer);
variabel
  lokalVar: integer;
mulai
  lokalVar := 50;
  globalVar := param + lokalVar;
selesai;

mulai
  globalVar := 10;
  hitung(globalVar);
selesai.