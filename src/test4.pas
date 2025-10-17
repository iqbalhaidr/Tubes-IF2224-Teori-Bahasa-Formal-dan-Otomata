program test4;

var
    x, y: integer;
    hasil: boolean;

begin
    x := 10;
    y := 5;
    hasil := (x > y) and not (x = y);

    if hasil or (x < y) then
        x := 1
    else
        x := 0;

    while x < 5 do
        x := x + 1;

    for x := 1 to 3 do
        y := y + x;
end.
