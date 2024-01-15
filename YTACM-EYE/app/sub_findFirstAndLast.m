function Y = sub_findFirstAndLast(X)
  Y = [find(X, 1) find(X, 1, "last")];
end
