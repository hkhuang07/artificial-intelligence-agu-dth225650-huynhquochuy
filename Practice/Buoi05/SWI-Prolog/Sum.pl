sum(1,1):-!.
sum(N,S) :-
        N > 1,
        N1 is N - 1,
        sum(N1, S1),
        S is N + S1.
do:-
	write("nhap X = "), read(X), sum(X,S),write(S).

