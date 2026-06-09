% facts
edge(a, b).
edge(a, f).
edge(b, c).
edge(c, d).
edge(c, e).
edge(e, d).
edge(f, g).
edge(f, c).
edge(f, e).
edge(g, c).

% clauses

% X -> Z -> Y
tedge(Node1, Node2) :-
    edge(Node1, SomeNode),
    edge(SomeNode, Node2).

% X -> Y
path(Node1, Node2) :-
    edge(Node1, Node2).

% X-> (...) -> Y
path(Node1, Node2) :-
    edge(Node1, SomeNode),
    path(SomeNode, Node2).

