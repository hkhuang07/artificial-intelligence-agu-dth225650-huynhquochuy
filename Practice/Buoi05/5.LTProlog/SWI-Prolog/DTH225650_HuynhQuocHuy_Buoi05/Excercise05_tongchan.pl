% facts
sum_even_recursive(0, 0).

% clauses
sum_even_recursive(N, SN) :-
    N > 0,
    N_Truoc is N - 2,
    sum_even_recursive(N_Truoc, SN_Truoc),
    SN is SN_Truoc + N.

tong_chan(N, SN) :-
    N mod 2 =:= 1, 
    N1 is N - 1, 
    sum_even_recursive(N1, SN).

tong_chan(N, SN) :-
    N mod 2 =:= 0,
    N >= 0,
    sum_even_recursive(N, SN).

tong_chan(N, 0) :-
    N < 0.  