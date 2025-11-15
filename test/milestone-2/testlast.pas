program UjiParserLengkap;

konstanta
  MAXSIZE := 100;
  NAMAKURSUS := 'TBFO IF2224';
  KARAKTERA := 'a';
  PI := 3.14159;

tipe
  RentangAngka = 1..MAXSIZE;
  TipeLarik = larik[1..10] dari integer;
  DataSiswa = rekaman
    nama: string;
    umur: integer;
    nilai: RentangAngka;
  selesai;
  TipeLarikKompleks = larik[10..20] dari DataSiswa;

variabel
  i, j, k: integer;
  status: boolean;
  rataRata: real;
  pilihan: char;
  dataAngka: TipeLarik;
  siswa1: DataSiswa;
  kelasIF: TipeLarikKompleks;

fungsi faktorial(n: integer): integer;
variabel
  hasil: integer;
mulai
  jika (n = 0) maka
    hasil := 1
  selainitu
    hasil := n * faktorial(n - 1);
  faktorial := hasil;
selesai;

prosedur cetakSiswa(s: DataSiswa);
mulai
  writeln('Data Siswa:');
  writeln('Nama: ', s.nama);
  writeln('Umur: ', s.umur);
selesai;

prosedur sapaDunia;
mulai
  writeln('Halo Dunia dari Prosedur!');
selesai;


mulai
  i := 1;
  j := 2;
  rataRata := (i + j) / 2.0;
  status := (i < j) dan (rataRata > 1.0) atau (tidak (j = 0));
  
  dataAngka[1] := 100;
  dataAngka[i + j] := 99;
  
  siswa1.nama := 'Budi';
  siswa1.umur := 20;
  siswa1.nilai := 85;
  
  kelasIF[10].nama := 'Siswa A';
  
  cetakSiswa(siswa1);
  
  sapaDunia(dummyData);
  writeln(dummyData);
  
  writeln('Menguji writeln dengan parameter...');

  jika (siswa1.umur > 18) dan (siswa1.nilai >= 80) maka
  mulai
    writeln(siswa1.nama, ' adalah mahasiswa berprestasi.');
  selesai
  selainitu
    writeln(siswa1.nama, ' perlu belajar lebih giat.');

  untuk i := 1 ke 5 lakukan
  mulai
    dataAngka[i] := i * i;
    writeln('Index ', i, ' = ', dataAngka[i]);
  selesai;
  
  untuk j := 10 turunke 8 lakukan
    writeln('Hitung mundur: ', j);

  k := 5;
  selama k > 0 lakukan
  mulai
    k := k - 1;
  selesai;

  ulangi
    k := k + 1;
  sampai k >= 10;

  pilihan := 'b';
  kasus pilihan dari
    'a': writeln('Anda memilih A');
    'b', 'c':
      mulai
        writeln('Anda memilih B atau C');
        k := faktorial(4);
      selesai;
    'd': writeln('Anda memilih D');
  akhir;

  status := (100 = k) atau (100 <> k);
  status := (k <= 10) dan (k >= 5);
  k := (10 + 5) * 2 - (10 bagi 3) + (10 mod 3);
  k := -k; 

selesai.