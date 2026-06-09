% mod(X, Y, Z): X chia Y được phần dư Z

% Y > 0
mod(X, Y, Z) :-
    Y > 0, 
    Z is X mod Y.

% Y = 0
mod(_, 0, _) :-
    write('Error: Khong the chia cho so 0.'),
    nl, 
    fail.

% Y < 0
mod(_, Y, _) :-
    Y < 0,
    write('Error: So chia Y phai la so duong.'),
    nl,
    fail. 