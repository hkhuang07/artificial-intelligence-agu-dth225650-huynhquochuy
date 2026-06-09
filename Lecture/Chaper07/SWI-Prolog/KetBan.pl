% facts
 gioi_tinh(lan,nu).
 gioi_tinh(hong,nu).
 gioi_tinh(thuy,nu).
 gioi_tinh(anh,nam).
 gioi_tinh(binh,nam).
 gioi_tinh(hung,nam).
 dep(lan).
 dep(hong).
 dep(binh).
 khoe(thuy).
 khoe(lan).
 khoe(binh).
 khoe(anh).
 khoe(hung).
 tot(lan).
 tot(thuy).
 thong_minh(hong).
 thong_minh(anh).
 thong_minh(hung).
 thong_minh(binh).
 giau(hong).
 giau(thuy).
 giau(hung).
% clauses
 thich(lan,X):- khoe(X), dep(X), thong_minh(X).
 thich(hong,X):- khoe(X), thong_minh(X), giau(X).
 thich(thuy,X):- khoe(X), dep(X), thong_minh(X).
 thich(anh,X):- dep(X), tot(X), thong_minh(X).
 thich(binh,X):- dep(X), khoe(X).
 thich(hung,X):- khoe(X), tot(X), thong_minh(X).
 ket_ban(X,Y):- gioi_tinh(X,M),
		gioi_tinh(Y,N),
		M\=N,
		thich(X,Y),
		thich(Y,X).