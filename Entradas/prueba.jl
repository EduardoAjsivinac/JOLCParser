println("");
println("=======================================================================");
println("=============================IFs ANIDADOS==============================");
println("=======================================================================");
aux = 10;
if aux > 0
    println("PRIMER IF CORRECTO");
    if true && (aux == 1)
        println("SEGUNDO IF INCORRECTO");
    elseif aux > 10
        println("SEGUNDO IF INCORRECTO");
    else
        println("SEGUNDO IF CORRECTO");
    end;
elseif aux <= 3
    println("PRIMER IF - ");
    if true && (aux == 1)
        println("SEGUNDO IF INCORRECTO");
    elseif aux > 10
        println("SEGUNDO IF INCORRECTO");
    else
        println("SEGUNDO IF CORRECTO");
    end;
end;