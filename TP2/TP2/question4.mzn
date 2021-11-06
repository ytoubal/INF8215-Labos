include "globals.mzn";

int: n_nurse; % Number of nurses
int: n_week; % Number of weeks in our horizon
int: n_day; % Number of days in our horizon (7 * n_week). Monday is the first day of the week
int: n_work_period; % Number of work period. It equals 4 (MATIN, SOIREE, NUIT, REPOS)

% Indexing the work periods
int: MATIN = 1;
int: SOIREE = 2;
int: NUIT = 3;
int: REPOS = 4;

int: dur_work_period; % Duration of the work periods (6h)

array[1..n_day,1..n_work_period] of int: demande_min; % Number of nurses required for each day and each work period (= 0 for REPOS)
array[1..n_nurse,1..n_day,1..n_work_period] of int: preference; % Work preference for each nurse

% Decision variables
array[1..n_nurse,1..n_day,1..n_work_period] of var 0..1: x; % work period [MATIN, SOIREE, NUIT, REPOS]
var int: sum_preference;

%Constraints
%

% 3. Respect the required minimum number of nurses
constraint forall(j in 1..n_day, k in 1..n_work_period) (sum(n in 1..n_nurse)(x[n,j,k]) >= demande_min[j,k]);

% 4. Restrict to only 1 period of work per day
constraint forall(i in 1..n_nurse, j in 1..n_day) (
                  sum(w in 1..n_work_period)(x[i,j,w]) == 1
);

% 5. Limit weekly hours to 36h
constraint forall(i in 1..n_nurse, k in 1..n_work_period where k != REPOS) (
                  sum(d in 1..n_day)(x[i,d,k]) * dur_work_period <= 36
);

% 6. Request at least 4 days of work per week
constraint forall(i in 1..n_nurse) (
                  sum(d in 1..n_day, k in 1..n_work_period where k != REPOS)(x[i,d,k]) >= 4
);

% 7. Give nurses a break after a night shift
constraint forall(i in 1..n_nurse, j in 1..n_day where x[i,j, NUIT] = 1) (
               if j+1 <= n_day 
                   then forall (k in 1..n_work_period where k != REPOS) (x[i,j+1,k] = 0) /\ 
                   x[i,j+1,n_work_period] = 1 
               endif
);

% 8. Forbid isolated working days
constraint forall(i in 1..n_nurse, j in 1..n_day, k in 1..n_work_period where x[i,j, REPOS] = 1) (
               if j+1 <= n_day /\ j+2 <= n_day then 
                   if x[i, j+1, REPOS] == 0 then x[i, j+2, REPOS] != 1 
                   endif 
               endif
);

% 9 Forbid nurses in working more than 3 consecutive days
constraint forall(i in 1..n_nurse, j in 1..n_day-3) (
               if x[i,j,REPOS] == 0 /\ x[i,j+1,REPOS] == 0 /\ x[i,j+2,REPOS] == 0
                   then (x[i,j+3,REPOS] = 1)
               endif
);

% Calculate preference
sum_preference = sum(i in 1..n_nurse, j in i..n_day, k in 1..n_work_period where x[i,j,k]=1)(preference[i,j,k]);

solve maximize sum_preference;

output
[
  "total: " ++ show(sum_preference) ++ "\n" ++
  "solution:\n\t    "
]
++
["Day \(j)\t" | j in 1..n_day]
++ 
[ 
  if j = 1 then "\n NURSE \(i): " else "\t" endif ++
    if fix(x[i,j,4]) == 1 then "--" elseif fix(x[i,j,3]) == 1  then "NUIT" elseif fix(x[i,j,2]) == 1  then "SOIREE" elseif fix(x[i,j,1]) == 1 then "MATIN" else "NONE" endif
  | i in 1..n_nurse, j in 1..n_day
];

