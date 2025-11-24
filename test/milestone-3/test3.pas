program DataSiswa;

tipe
  Siswa = rekaman
    id: integer;
    nilai: real;
  selesai;

variabel
  kelas: larik [1..30] dari Siswa;
  temp: Siswa;

mulai
  temp.id := 101;
  temp.nilai := 85.5;
  kelas[1] := temp;
selesai.