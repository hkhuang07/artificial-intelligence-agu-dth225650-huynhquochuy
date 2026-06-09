% facts
  cha(nam,minh).
  cha(minh,lam).
  me(thu,phi).
  cha(long,giang).
  cha(long,thu).
% clauses
  ong_noi(X,Y):- cha(X,Z),cha(Z,Y).
  ong_ngoai(X,Y):- cha(X,Z),me(Z,Y).
