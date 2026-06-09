% clauses
  kt(1,_):- write("Day la so nguyen to").
  kt(2,_):- write("Day la so nguyen to").
  kt(N,M):- N1 is N-1,N2 is M/N1, N3 is round(M/N1),tieptuc(N1,N2,N3,M).
  tieptuc(_,N2,N3,_):- N2 is N3, write("Day khong phai la so nguyen to").
  tieptuc(N1,N2,N3,M):- N2 =\= N3,kt(N1,M).