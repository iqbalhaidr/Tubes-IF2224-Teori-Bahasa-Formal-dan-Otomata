program LogikaIndo;

variabel
  a, b: integer;
  hasil: real;
  isValid: boolean;

mulai
  a := 20;
  b := 5;
  
  isValid := (a > 10) dan (b < 10);
  
  jika isValid maka
    hasil := a bagi b;  
  
  selama a > 0 lakukan
    a := a - 1;
selesai.