% facts
  cha(nam,minh).
  cha(minh,lam).
  cha(long,giang).
  cha(minh,hung).
  cha(long,thu).
  me(thu,hong).
  me(thu,phi).
% clauses
  ong_noi(X,Y):- cha(X,Z),cha(Z,Y).
  ong_ngoai(X,Y):- cha(X,Z),me(Z,Y).
