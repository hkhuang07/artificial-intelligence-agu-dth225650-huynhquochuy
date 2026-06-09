%facts
parent(nam,lan).
parent(long,minh).
parent(teo,cuti).
parent(lan,tuyet).
male(nam).
male(long).
male(cuti).
female(lan).
female(minh).
%clauses
cha(X,Y):- parent(X,Y),male(X).
me(X,Y):- parent(X,Y),female(X).
