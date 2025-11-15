program Tes111213142122;

variabel
  radius: integer;
  area, res1, res2, res3: real;

prosedur namaProsedur1(r: integer; a: real);
  konstanta
    pi := 3;

  mulai
    jika r < 5 maka
      a := 75
    selainitu
      a := pi * r * r;
  selesai;

prosedur namaProsedur2;
  mulai
    writeln('Testing prosedur without paramater');
  selesai;

fungsi namaFungsi1(r: integer) : real;
  konstanta
    pi := 3;

  mulai
    jika r < 5 maka
      namaFungsi1 := 75
    selainitu
      namaFungsi1 := pi * r * r;
  selesai;

fungsi namaFungsi2 : real;
  mulai
    namaFungsi2 := 75
  selesai;

mulai
  radius := 5;

  namaProsedur1(radius, res1);
  namaProsedur2(harusnyaBisaTanpaParameterTapiKarenaDiSpekSemuaProecedureDanFunctionCallHarusPakeParenthesisJadiKalimatIniDigunakanSebagaiFillerSupayaValid);
  
  res2 := namaFungsi1(radius);
  res3 := namaFungsi2(harusnyaBisaTanpaParameterTapiKarenaDiSpekSemuaProecedureDanFunctionCallHarusPakeParenthesisJadiKalimatIniDigunakanSebagaiFillerSupayaValid);
selesai.