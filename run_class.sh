##################################################
#
# This is one-shot-test-all script
# I first remove any previous output files
# And then edit the params.py directly with the provided 
# arguments and test
#
# It accouns for stage-1,2 as well as each subject 
# individually and together
#
##################################################

rm classifiers_results.txt

python3 main_classifiers_console_ver.py 1 'FILE_DEV'
python3 descriptor_extractor.py
python3 main_classifiers.py

python3 main_classifiers_console_ver.py 2 'FILE_DEV'
python3 descriptor_extractor.py
python3 main_classifiers.py

python3 main_classifiers_console_ver.py 1 'FILE_LEADER'
python3 descriptor_extractor.py
python3 main_classifiers.py

python3 main_classifiers_console_ver.py 2 'FILE_LEADER'
python3 descriptor_extractor.py
python3 main_classifiers.py
