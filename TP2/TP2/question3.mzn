include "globals.mzn"; 

int: n; % num rows and columns

int: L = 1; % Lamp
int: P = 2; % Plant

% 1 for a lamp, 2 for a plant and 0 for nothing 
array[1..n,1..n] of 0..2: garden;

% number of plants by row/col
array[1..n] of int: rows;
array[1..n] of int: cols;

% decision variables
array[1..n,1..n] of var 0..P: x;

% 0. fix the lamps
constraint forall(i,j in 1..n)(if garden[i,j] == L then x[i,j] = garden[i,j] endif);

% 1. fix number of plants in each row and col
constraint forall(i in 1..n)(count(row(x,i), P, rows[i]));
constraint forall(j in 1..n)(count(col(x,j), P, cols[j]));

% 2. plants cant touch horizontally, vertically and diagonally
constraint forall(i,j in 1 ..n where x[i,j] = P) (
                  if i+1 <= n then x[i+1,j] != P endif /\
                  if j+1 <= n then x[i,j+1] != P endif /\
                  if i-1 >= 1 then x[i-1,j] != P endif /\
                  if j-1 >= 1 then x[i,j-1] != P endif /\
                  if i+1 <= n /\ j+1 <= n then x[i+1,j+1] != P endif /\
                  if i+1 <= n /\ j-1 >= 1 then x[i+1,j-1] != P endif /\
                  if i-1 >= 1 /\ j-1 >= 1 then x[i-1,j-1] != P endif /\
                  if i-1 >= 1 /\ j+1 <= n then x[i-1,j+1] != P endif 
);

% 3. plants must be beside a lamp horizontally or vertically
constraint forall(i,j in 1 ..n where x[i,j] = P) (
                  if i+1 <= n then x[i+1,j] == L else false endif \/
                  if j+1 <= n then x[i,j+1] == L else false endif \/
                  if i-1 >= 1 then x[i-1,j] == L else false endif \/
                  if j-1 >= 1 then x[i,j-1] == L else false endif 
);

% 4. lamps must be beside at least one plant horizontally or vertically
constraint forall(i,j in 1 ..n where x[i,j] = L) (
                  if i+1 <= n then x[i+1,j] == P else false endif \/
                  if j+1 <= n then x[i,j+1] == P else false endif \/
                  if i-1 >= 1 then x[i-1,j] == P else false endif \/
                  if j-1 >= 1 then x[i,j-1] == P else false endif 
);

solve satisfy;

output 
[
 if j = 1 then "\n" ++ show(rows[i]) ++ " " else " " endif ++
   if fix(x[i,j]) = L then "L" elseif fix(x[i,j]) = P then "P" else "_" endif
| i,j in 1..n
] ++ ["\n  "] ++ [show(cols[i]) ++ " " | i in 1..n];
