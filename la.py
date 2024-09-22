import os
file_path = '/Users/devanshsaroja/Documents/a-data science/movie_recom_system_envi/movies.pkl'
if os.path.exists(file_path):
    print("File found!")
else:
    print("File not found!")