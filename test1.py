import os



pch_default_path = r'G:\NC_POSTING_DATA\OUTPUT_DATA\CRITICAL\TEMP'

if os.path.exists(pch_default_path):
    print('yes')
else:
    print('no')
