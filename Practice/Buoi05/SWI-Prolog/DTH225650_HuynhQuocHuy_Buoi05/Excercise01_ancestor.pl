% facts 
parent(an, hung).
parent(thuy, hung).
parent(linh, an).
parent(le, linh).
parent(anh, thuy).
parent(ngoc, le).

% clauses 
ancestor(X, Y) :- parent(X, Y).
ancestor(X, Y) :- parent(X, Z), ancestor(Z, Y).