##################################################
#
# In case any of the hyper-parameters is modified in 
# the way the csv file is mapped into descriptors, 
# I need to update the relating vairables
#
# Also, this affects descriptor distributions and like
# so we also update metadata
#
##################################################
python3 descriptor_extractor.py

cd windowtitle_codes/
python3 reduce_to_single_coding.py

cd ../analysis/01_automatic_rule_generation/
python3 metadata.py
