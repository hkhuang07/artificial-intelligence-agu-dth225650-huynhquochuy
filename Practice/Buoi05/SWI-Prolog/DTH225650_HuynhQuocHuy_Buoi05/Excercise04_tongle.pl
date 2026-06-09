% facts
sum_odd_recursive(1, 1).

% clauses
sum_odd_recursive(N, SN) :-
    N > 1,
    N_Truoc is N - 2,
    sum_odd_recursive(N_Truoc, SN_Truoc),
    SN is SN_Truoc + N.

tong_le(N, SN) :-
    N mod 2 =:= 1, 
    sum_odd_recursive(N, SN).

tong_le(N, SN) :-
    N mod 2 =:= 0,
    N1 is N - 1, 
    sum_odd_recursive(N1, SN).

tong_le(N, 0) :-
    N < 1.