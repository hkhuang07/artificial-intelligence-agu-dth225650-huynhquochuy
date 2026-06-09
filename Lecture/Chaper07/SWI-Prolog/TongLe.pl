tongle(1,1):-!.
tongle(SN,N):- N > 2,
			N1 is N - 2,
			tongle(SN1,N1),
			SN is SN1 + N.
tong(SN,N):- N mod 2 =:= 0, 
			N >= 2,
			N1 is N - 1, 
			tongle(SN,N1).
tong(SN,N):- N mod 2 =\= 0,
			N > 2, 
			tongle(SN,N).