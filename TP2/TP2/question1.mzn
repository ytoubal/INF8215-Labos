include "globals.mzn"; 

int: r; % number of rows 
int: c; % number of columns
array[1..r] of int: rowinsects; % total of insects by row
array[1..c] of int: colinsects; % total of insects by col
array[1..r, 1..c] of 0..r*c: knownpositions;  % known number of insects, 0 appears when unknown


array[1..r, 1..c] of var 1..r*c: x; % the final garden grid (decision variable)


%Constraints
constraint forall(i in 1..r)(sum(row(x, i))=rowinsects[i]); % sum of the insects in each row
constraint forall(j in 1..c)(sum(col(x, j))=colinsects[j]); % sum of the insects in each column

constraint forall(i in 1..r, j in 1..c)(
    if knownpositions[i,j] > 0 then x[i,j] = knownpositions[i,j] else true endif ); % set the known positions
    

output [
  "["
]
++
[
  if j = 1 then "\n" else "," endif ++
    if fix(x[i,j]) < 10 then "  " else " "  endif ++
    show(x[i,j]) ++
  if j = c then 
    ", f(" ++ show(rowinsects[i]) ++ "),"
  else 
    ""
  endif
  | i in 1..r, j in 1..c
] 
++
["\n"]++
[
  "f(" ++ show(colinsects[j]) ++ "),"
  | j in 1..c
]

++ ["]\n"]
;