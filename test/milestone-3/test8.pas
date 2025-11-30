program ComprehensiveTest;

konstanta
  MAXSIZE = 100;
  PIVALUE = 3.14159;
  APPNAME = 'SemanticTester';
  NEWLINE = '\n';

tipe
  IndexRange = integer;
  
  Matrix = larik [1..10] dari larik [1..10] dari integer;
  
  Student = rekaman
    id: integer;
    name: larik [1..50] dari char;
    gpa: real;
    active: boolean;
  selesai;
  
  Classroom = rekaman
    roomnumber: integer;
    students: larik [1..30] dari Student;
    capacity: integer;
  selesai;
  
  IntArray = larik [0..99] dari integer;

variabel
  i, j, k: integer;
  x, y, z: real;
  flag, done: boolean;
  grid: Matrix;
  class: Classroom;
  scores: IntArray;
  tempstudent: Student;

fungsi calculate(a: integer; b: real; var result: real): boolean;
variabel
  temp: real;
mulai
  temp := a * b;
  result := temp + PIVALUE;
  
  jika result > 100.0 maka
    calculate := true
  selainitu
    calculate := false;
selesai;

fungsi sumarray(arr: IntArray; size: integer): integer;
variabel
  total, idx: integer;
mulai
  total := 0;
  untuk idx := 0 ke size - 1 lakukan
    total := total + arr[idx];
  sumarray := total;
selesai;

prosedur swapstudents(var s1, s2: Student);
variabel
  temp: Student;
mulai
  temp := s1;
  s1 := s2;
  s2 := temp;
selesai;

prosedur updateclassroom(var c: Classroom; room: integer; cap: integer);
mulai
  c.roomnumber := room;
  c.capacity := cap;
selesai;

prosedur testcomplexaccess(dummy: integer);
variabel
  idx: integer;
mulai
  class.students[1].id := 1001;
  class.students[1].gpa := 3.75;
  class.students[1].active := true;
  
  tempstudent := class.students[1];

  class.students[1].name[1] := 'J';
  class.students[1].name[2] := 'o';
  class.students[1].name[3] := 'h';
  class.students[1].name[4] := 'n';
selesai;

prosedur testcontrolflow(n: integer);
variabel
  counter, value: integer;
  condition: boolean;
mulai
  jika n > 0 maka
  mulai
    value := n * 2;
  selesai
  selainitu
  mulai
    value := 0;
  selesai;

  counter := 0;
  selama counter < n lakukan
  mulai
    counter := counter + 1;
  selesai;

  untuk i := 1 ke 10 lakukan
  mulai
    scores[i] := i * i;
  selesai;

  untuk i := 10 turunke 1 lakukan
  mulai
    value := scores[i];
  selesai;

  counter := 0;
  ulangi
    counter := counter + 1;
  sampai counter >= n;

  kasus n dari
    1: value := 10;
    2: value := 20;
    5: value := 50;
    10: value := 100;
  akhir;
selesai;

fungsi complexexpression(a, b, c: integer): real;
variabel
  result: real;
mulai
  result := (a + b) * c / 2.0;

  result := result + ((a - b) * (c + 5)) / 3.0;
  
  complexexpression := result;
selesai;

fungsi testboolean(x, y: integer; flag: boolean): boolean;
variabel
  temp: boolean;
mulai
  temp := (x > y) dan (x < 100);

  temp := ((x >= 0) dan (y <= 10)) atau flag;

  temp := tidak temp;
  
  testboolean := temp atau ((x = y) dan (x <> 0));
selesai;

prosedur testnestedcalls(dummy: integer);
variabel
  success: boolean;
  total: integer;
  res: real;
mulai
  total := sumarray(scores, 50);

  success := calculate(10, 2.5, res);

  jika calculate(5, 3.0, res) maka
    total := sumarray(scores, 10);
selesai;

prosedur testarrays(dummy: integer);
variabel
  a, b: integer;
mulai
  untuk a := 0 ke 99 lakukan
    scores[a] := a;
  
  untuk a := 1 ke 10 lakukan
    untuk b := 1 ke 10 lakukan
      grid[a][b] := a * b;
selesai;

prosedur testrecords(dummy: integer);
variabel
  s1, s2: Student;
mulai
  s1.id := 100;
  s1.gpa := 3.5;
  s1.active := true;

  s2 := s1;

  s2.id := 200;

  swapstudents(s1, s2);
selesai;

prosedur testedgecases(dummy: integer);
variabel
  minval, maxval: integer;
  epsilon: real;
mulai
  minval := 0;
  maxval := MAXSIZE;

  epsilon := 0.0001;

  minval := -100;

  scores[0] := minval;
  scores[99] := maxval;

  grid[1][1] := 1;
  grid[10][10] := 100;
selesai;

mulai
  i := 0;
  x := 0.0;
  flag := false;

  i := MAXSIZE;
  x := PIVALUE;
  
  testcomplexaccess(i);
  testcontrolflow(10);
  testnestedcalls(i);
  testarrays(i);
  testrecords(i);
  testedgecases(i);

  x := complexexpression(5, 3, 2);
  flag := testboolean(10, 20, true);

  i := sumarray(scores, 100);
  
  jika calculate(i, x, y) maka
  mulai
    updateclassroom(class, 101, 30);
  selesai;
selesai.