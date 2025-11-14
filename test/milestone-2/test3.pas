program test3;

variabel
    a, b: integer;

mulai
    a := 7;
    b := 3;

    a := a + b;
    a := a - b;
    a := a * b;
    a := a / b;
    a := a bagi b;
    a := a mod b;

    jika a = b maka
        a := 0;

    jika a <> b maka
        a := 1;

    jika a <= b maka
        a := 2;

    jika a >= b maka
        a := 3;
selesai.
