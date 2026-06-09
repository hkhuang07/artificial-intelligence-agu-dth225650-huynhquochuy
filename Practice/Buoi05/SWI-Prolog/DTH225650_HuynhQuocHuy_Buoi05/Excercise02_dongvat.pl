% facts
loai_an_co(de).
loai_hung_du(chosoi).

% clauses
loai_an_thit(X) :- loai_hung_du(X).

uong(X, nuoc) :- loai_an_thit(X).
uong(X, nuoc) :- loai_an_co(X).

an(X, thit) :- loai_an_thit(X).

an(X, co) :- loai_an_co(X).

an(X, Y) :- loai_an_thit(X),loai_an_co(Y).

tieu_thu(X, Y) :- an(X, Y).
tieu_thu(X, Y) :- uong(X, Y).


