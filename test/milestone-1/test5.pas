program test5;

var
    angka: array[1..5] of integer;
    i: integer;

begin
    for i := 1 to 5 do
        angka[i] := i;

    angka[3] := 3.1415E+2;
end.