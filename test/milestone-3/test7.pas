program TestSemantic;

konstanta
  MAX = 10;
  PI = 3.14;
  NAME = 'PascalS';

tipe
  Vector = larik [1..10] dari integer;

  Point = rekaman
    x, y: integer;
  selesai;

  Shape = rekaman
    id: integer;
    vertices: Vector;
    center: Point;
    active: boolean;
  selesai;

variabel
  gval, i: integer;
  greal: real;
  isvalid: boolean;
  myshape: Shape;
  coords: larik [1..5] dari Point;
  writeln: integer;

fungsi factorial(n: integer): integer;
mulai
  jika n <= 1 maka
    factorial := 1
  selainitu
    factorial := n * factorial(n - 1);
selesai;

prosedur swap(var a, b: integer);
variabel 
  temp: integer;
mulai
  temp := a;
  a := b;
  b := temp;
selesai;

prosedur processlogic(limit: integer);
variabel
  counter: integer;
  localbool: boolean;
mulai
  counter := 0;
  
  selama counter < limit lakukan
  mulai
    counter := counter + 1;
    
    jika (counter mod 2 = 0) dan (counter > 5) maka
      writeln := 1
    selainitu
      writeln := 1;
  selesai;

  ulangi
    counter := counter - 1;
  sampai counter = 0;

  kasus limit dari
    1: writeln := 1;
    10: writeln := 1;
  akhir;
selesai;

mulai
  gval := 5;
  greal := 10.5 + 2.5;
  isvalid := true;

  myshape.id := 1;
  myshape.active := tidak isvalid; 
  myshape.vertices[1] := 100;
  myshape.center.x := 50;
  
  coords[1].y := myshape.center.x * 2;

  processlogic(MAX);

  gval := factorial(5) + 10;

  swap(myshape.id, gval);

  untuk i := 1 ke 5 lakukan
  mulai
    coords[i].x := i * i;
    writeln := 1;
  selesai;

  writeln := 1;
selesai.