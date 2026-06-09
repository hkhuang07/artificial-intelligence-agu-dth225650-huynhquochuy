% facts
nguoi(minh,nam,20).
nguoi(phi,nam,24).
nguoi(lan,nu,27).
nguoi(thu,nu,24).
% clauses
ket_hon(X,Y):- nguoi(X,nam,T1),nguoi(Y,nu,T2),T1>=T2.