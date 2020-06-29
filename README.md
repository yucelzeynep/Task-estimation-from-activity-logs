# Task estimation from activity logs
The data and codes necessary to reproduce the results reported in our manuscript

The repository is organized such that the three main approaches discussed in the article can be tested as separate 'main' modules. In particular, 
(i) main_benchmark.py implements the benchmark method based on association rules.
(ii) main_bayesian_blended.py implements the proposed Bayesian estimation scheme 
(iii) main_classifers.py provides estimation with standard classifiers. 

In addition, any functions necessary for the above implementations are provided as tools (as tools_*.py files).

Moreover, the routines, which need not to be called online, but rather relate the selection of hyper-parameters, are provided as auxiliary scripts (as aux_*.py files).

**Main routines**

**Tools**

**Auxiliary routines**



