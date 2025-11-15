program test4;

variabel
    x, y: integer;
    hasil: boolean;

mulai
    x := 10;
    y := 5;


    jika x < y maka
        x := 1
    selainitu
        x := 0;

    selama x < 5 lakukan
        x := x + 1;

    untuk x := 1 ke 3 lakukan
        y := y + x;
selesai.
