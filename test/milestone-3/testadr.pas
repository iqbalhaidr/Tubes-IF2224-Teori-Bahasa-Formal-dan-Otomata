program CekScope;

tipe
  Angka5 = larik[1 .. 5] dari integer;
  recordtipe = rekaman
    id: integer;
    nilai: real;
  selesai;
  

variabel
  global1Var: integer;
  a: real;
  varRecord: recordtipe;
  global2Var: integer;


prosedur hitung(param: integer);
variabel
  lokal1Var: integer;
  lokalArr : Angka5;
  lokal2Var: integer;
mulai
  lokalArr[0] := 2;
  lokal1Var := 50;
  lokal2Var := 100 + lokal1Var;
  global1Var := param + lokal2Var;
selesai;

mulai
  varRecord.id := 5;
  varRecord.nilai := 1.8;

  global1Var := 10;
  hitung(global1Var);

  global2Var := 2 * global1Var;
  global1Var := global1Var + varRecord.id;
  a := 5.2 + varRecord.nilai;
selesai.