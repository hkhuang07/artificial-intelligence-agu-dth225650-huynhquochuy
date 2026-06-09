% Định nghĩa quare(X, I) I là căn bậc hai của X 

square(X, I) :-
    X >= 0,
    I is sqrt(X).
    
square(X, I) :-
    X < 0,
    write('Error: Khong the tinh can bac hai so am. '),
    fail. 

Viết chương trinh Prolog hàm chia lấy phần nguyên div(X,Y,Z) với chức năng lấy X chia cho Y được Z. Nếu X < Y thì Z = 0, ngược thì chia lấy phần nguyên. Cung cấp các testcase