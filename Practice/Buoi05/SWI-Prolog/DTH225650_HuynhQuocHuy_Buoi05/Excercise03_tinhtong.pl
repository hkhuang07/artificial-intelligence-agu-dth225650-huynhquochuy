% clauses
sum(N, SN) :-
    sum_acc(N, 0, SN).

sum_acc(0, SN, SN).

sum_acc(N, Acc, SN) :-
    N > 0,
    Acc_Moi is Acc + N, 
    N_Truoc is N - 1,
    sum_acc(N_Truoc, Acc_Moi, SN).