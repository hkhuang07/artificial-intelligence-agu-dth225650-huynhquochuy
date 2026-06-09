% div(X, Y, Z): X chia Y lấy phần nguyên là Z

%  X >= Y
div(X, Y, Z) :-
    X >= Y,
    Y > 0,
    Z is X // Y. 

%  X < Y
div(X, Y, 0) :-
    X < Y,
    Y \== 0. 