program TesKasus5;

tipe
  Data = rekaman
    kode : integer;
    nilai : integer;
  selesai;

variabel
  p : integer;
  d : char;

mulai
  p := 3;
  d.kode := 0;
  d.nilai := 0;

  kasus p dari
    1: satu;
    2: dua;
    3, 4, 5: blok1;
    10: blok2;
    -1: minusSatu;
  akhir;

selesai.
