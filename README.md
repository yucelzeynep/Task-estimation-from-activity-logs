# Task estimation from activity logs
This repository contains the resources necessary for reproducing the results reported in our manuscript. Specifically, it is organized as collection data, main routines, tools, auxiliaries.

**Main routines**

The three main approaches discussed in the article can be tested by running the  'main' routines. In particular, 
(i) main_benchmark.py implements the benchmark method based on association rules.
(ii) main_bayesian_blended.py implements the proposed Bayesian estimation scheme 
(iii) main_classifers.py provides estimation with standard classifiers. 


###### Benchmark method

The main_benchmark.py routine applies the association rules on the actions and estimates tasks. For a detailed analysis and comparison with the proposed method, check main_proposed, which implements not only the Bayesian approach but also the benchmark method and provides comparison. The list of -definitions- of association rules and the functions which apply them on the actions can be found in tools_rule.py. 

###### Proposed Bayesian estimation method
###### Estimation with standard classifiers


**Tools**

Any functions necessary for the implementation of the main routines are provided as tools (i.e. as tools_*.py files).


**Auxiliary routines**

Moreover, the routines, which are not called online, but rather relate the selection of hyper-parameters etc., are provided as auxiliary scripts (as aux_*.py files).


