println("=======================================================================");
println("==========================FUNCIONES Y RETURN===========================");
println("=======================================================================");
function potenciaNativa(base::Int64, exponente::Int64)
    resultado = base;
    while exponente > 1
        resultado = resultado * base;
        exponente = exponente - 1;
    end;
    println(sumarTodo(base,exponente))
    return resultado;
end;

function sumarTodo(num1::Int64, num2::Int64)
    result = 0;
    if num1 < 0 || num2 < 0
        return -1;
    end;

    while num1 > 0 || num2 > 0
        result = result + (num1 + num2);
        num1 = num1 - 1;
        num2 = num2 - 1;
    end;
    return result;
end;

println(potenciaNativa(5, 7));
println(potenciaNativa(2, 2));
println(potenciaNativa(4, 2));
