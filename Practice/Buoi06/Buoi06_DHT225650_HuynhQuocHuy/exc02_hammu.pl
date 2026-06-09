% hammu(X,N,V) X là số , N là mu, V là kết quả X^N

% basecase (X^0 = 1).
hammu(_, 0, 1). 

% recursivecase) ---
% (X^N = X * X^(N-1))
hammu(X, N, V) :-
    N > 0,
    N_Truoc is N - 1,
    hammu(X, N_Truoc, V_Truoc),
    V is V_Truoc * X.


