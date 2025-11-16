program UjiSemua;

konstanta
  max = 10;
  angka = 5;

tipe
  Angka = integer;
  Data = rekaman
    x, y : integer;
    z : char;
  selesai;
  Matriks = larik[1 .. 5] dari Angka;

variabel
  a, b : integer;
  d : Data;
  m : Matriks;

mulai
  a := 1;
  b := max;

  d.x := 10;
  d.y := 20;
  d.z := 'A';

  m[1] := 100;

selesai.
