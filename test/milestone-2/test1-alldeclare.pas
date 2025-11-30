program MiniTest;

konstanta
  k = 9;

tipe
  Bil = integer;
  gokil = string;
  murid = packed rekaman
    nama : string;
    umur : integer;
    nomorAbsen : integer;
  selesai;

  Mahasiswa = rekaman
    nama : char;
    umur : integer;
    namaOrtu : string;
  selesai;

variabel
  x : Bil;
  mhs : Mahasiswa;

mulai
  x := k;
selesai.
