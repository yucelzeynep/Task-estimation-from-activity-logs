# Task estimation from activity logs
This repository contains the resources necessary for reproducing the results reported in our manuscript. The implementation is done in Python 3.5.2 with no specific dependencies.

Specifically, it is organized as collection data, main routines, auxiliaries and tools. Please see below for brief explanation of each component. For a high-level overview of each  script, please see the docstrings appearing on the top of each file. 

**Data and annotations**

The activity logs and task annotations are provided together. Namely, the columns in data/annotation_*.csv involve both the descriptors and the assigned tasks as organized as follows

| Column no. | Header | Contents | 
| :---      |  :------  |:------  |
|  1   | -  | -   |
|  2   | 開始時刻   | Start time   |
|  3   | 終了時刻   | End time  |
|  4   | 左クリック   | Left clicks   |
|  5   | 右クリック   | Right clicks   |
|  6   | 打鍵回数   | Key strokes   |
|  7   | 実行ファイル名   | Application   |
|  9   | 候補1   | Task annotation (candidate-1)   |
|  10   | 候補2   |  Task annotation (candidate-2)   |
|  11   | 候補3   |  Task annotation (candidate-3)   |
|  12   | 自動推定 | Automatic estimation by association rules   |

In this respect, columns 2-7 contain the descriptors, whereas columns 9-11 contain the annotations. On the other hand, column 12 contains the outcomes of an implementation of the benchmark method (based on association rules) in Visual Basic [1]. However, in this project, we prefer using a devoted routine for this (see below for the explanation of main_benchmark.py), so as to be able to carry out a detailed analysis on a common platform and provide comparisons to the proposed method. 


**Main routines**

The three main approaches discussed in the article can be tested by running the below 'main' routines. In particular, 
1. main_benchmark.py implements the benchmark method based on association rules.
2. main_bayesian_blended.py implements the proposed Bayesian estimation scheme.
3. main_classifers.py provides estimation with standard classifiers. 


###### Benchmark method

The main_benchmark.py routine applies the association rules on the actions for estimating the tasks. The list of (antecedents and consequences) of association rules and the functions, which apply those rules on the actions, can be found in tools_rule.py. 

For a more detailed analysis together with a comparison with the proposed method, see main_proposed.py.

###### Proposed Bayesian estimation method
The main_proposed.py routine implements the Bayesian scheme. Several variations of it, for instance non-/hierarchical, as well as assuming different relevance characteristics or in/dependence relations between descriptors, can be realized by setting the relating hyper-parameters in params.py file. 

Moreover, this routine does not only the Bayesian approach but also the benchmark method and provides detailed comparison. 

###### Estimation with standard classifiers

This routine applies K-Nearest Neighbor, Random Forest and Support Vector classification. The functions which separate training and test data, do cross-validation and tabulate classification outcomes can be found in tools_classifier.py. 


**Auxiliary routines**

Moreover, the routines, which are not called online, but rather relate the selection of hyper-parameters etc., are provided as auxiliary scripts (as aux_*.py files). Specifically, there are two auxiliaries for 
1. Judging relevance of descriptors for the given tasks 
2. Assessing in/dependence of descriptor pairs

The first one is implemented in aux_cramersV.py, whereas the second one is realized by aux_entropy.py. Moreover, tools_cramersV.py contain the functions which tabulate V in a straightforward as well as bias-corrected manner. In addition, tools_entropy.py involve functions for computing joint entropy and mutual information. 

**Tools**

Any functions necessary for the implementation of the main or auxiliary routines are provided as tools (i.e. as tools_*.py files). In addition to the tools explained above, we implemented several sets of functions such as the ones for managing dictionary variables (tools_dic.py), for managing file operations (tools_file.py), and for illustration of results as tables or figures (tools_presentation.py).



