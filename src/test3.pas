program test3;

var
    a, b: integer;

begin
    a := 7;
    b := 3;

    a := a + b;
    a := a - b;
    a := a * b;
    a := a / b;
    a := a div b;
    a := a mod b;

    if a = b then
        a := 0;

    if a <> b then
        a := 1;

    if a <= b then
        a := 2;

    if a >= b then
        a := 3;
end.
