#!/bin/bash

N=20
ex="./shoc_run_and_cmp_cxx baseline"


avg_time() {
     n=$1; shift
     (($# > 0)) || return                   # bail if no command given
     for ((i = 1; i <= $N; i++)); do
         { time -p "$@" &>/dev/null; } 2>&1 # ignore the output of the command
                                            # but collect time's output in stdout
     done | awk '
         /real/ { reals[nr]=$2; nr++ }
         /user/ { users[nu]=$2; nu++ }
         /sys/  { syss[ns]=$2; ns++ }
         END    {
	 	  printf("For %f runs: \n",nr-1)
		  { for (j = 1; j < nr; j++) realsum = realsum + reals[j] }
		  { for (j = 1; j < nr; j++) usersum = usersum + users[j] }
		  { for (j = 1; j < nr; j++) syssum = syssum + syss[j] }

		  { for (j = 1; j < nr; j++) realerrorsum = realerrorsum + (reals[j] - realsum/(nr-1))^2  }
		  { for (j = 1; j < nr; j++) usererrorsum = usererrorsum + (users[j] - usersum/(nr-1))^2  }
		  { for (j = 1; j < nr; j++) syserrorsum = syserrorsum + (syss[j] - syssum/(nr-1))^2  }

		  printf("Real: %f +- %f seconds \n", realsum/(nr-1), sqrt(realerrorsum)/(nr-3));
		  printf("User: %f +- %f seconds \n", usersum/(nr-1), sqrt(usererrorsum)/(nr-3));
		  printf("Sys: %f +- %f seconds \n", syssum/(nr-1), sqrt(syserrorsum)/(nr-3));

                }'
 }

#echo " usage: avg_time N command"
#echo " where N=number of repititions"

avg_time ${N} ${ex}
