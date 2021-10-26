include "globals.mzn"; 

int: n = 5;
% the given results
array[1..4] of int: res = [1,2,5,7];

% number of points for each player
array[1..n] of var 0..3*n: x;

% (i, j) is the result of player i against player j
array[1..n, 1..n] of var {0,1,3}: matches;

% matches agaisnt yourself
constraint forall(i in  1..n)(matches[i,i]=0); 

% result of the matches
constraint forall(i in 1..n-1)(sum(row(matches, i))=res[i]);
constraint forall(i, j in 1..n where i != j) (
                  if matches[i,j] == 3 then matches[j, i] == 0
                  elseif matches[i,j] == 1 then matches[j, i] == 1
                  else true
                  endif
                  );
                  
% Find values of row 5
constraint forall (i in 1..n-1) (matches[5,i] + matches[i,5] > 0);

% results of x
constraint forall(i in 1..n)(x[i]=sum(row(matches, i)) );

solve satisfy;

output 
[
  "Scores\n"
]
++
[
  show(x)
]
++	
[
  "\nMatches\n"
]
++
[ show(matches[i,j]) ++ 
         if j == n then "\n" else " " endif |
         i in 1..n, j in 1..n
]
;