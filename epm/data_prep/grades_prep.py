#!/usr/bin/env python
# coding: utf-8
"""
This module preprocess the grades files
"""


import os
import glob
import pandas as pd
import scipy.stats as stats
import numpy as np
from sklearn.preprocessing import StandardScaler



def read_grades(dir1 = 'data/EPM_Project/EPM_dataset/Data/intermediate_grades.xlsx',
                dir2 = 'data/EPM_Project/EPM_dataset/Data/final_grades.xlsx'):
    """
    Read grades.xlsx files
    """
    # get intermediate grades
    mid_grades = pd.read_excel(dir1)
    
    # get final grades
    xl_file = pd.ExcelFile(dir2)
    sheet_name = xl_file.sheet_names
    final_1st = pd.read_excel(dir2, sheet_name=sheet_name[0])
    final_2nd = pd.read_excel(dir2, sheet_name=sheet_name[1])
    
    return mid_grades, final_1st, final_2nd


def final_manipulation(final_1st,final_2nd):
    """
    This function merge two final grades into one single file
    """
    # students who took exams twice
    twotimer = list(set(final_1st['Student ID']).intersection(set(final_2nd['Student ID'])))
    # 1st test takers without taking the second exam
    final_2nd_unique=final_2nd[-final_2nd['Student ID'].isin(twotimer)]
    # students who took final exams (selected twotimers' first exam score)
    final = final_1st.append(final_2nd_unique).sort_values(by=['Student ID'])

    final_data = {'ID': final['Student ID']}
    
    # aggregate grades of each session
    final_data['FIN1'] = (final['ES 1.1 \n(2 points)'] + final['ES 1.2 \n(3 points)']) / 5 * 100
    final_data['FIN2'] = (final['ES 2.1\n(2 points)'] + final['ES 2.2\n(3 points)']) / 5 * 100
    final_data['FIN3'] = (final['ES 3.1\n(1 points)'] + final['ES 3.2\n(2 points)'] + final['ES 3.3\n(2 points)'] + final['ES 3.4\n(2 points)'] + final['ES 3.5\n(3 points)']) / 10 * 100
    final_data['FIN4'] = (final['ES 4.1\n(15 points)'] + final['ES 4.2\n(10 points)']) / 25 * 100
    final_data['FIN5'] = (final['ES 5.1\n(2 points)'] + final['ES 5.2\n(10 points)'] + final['ES 5.3\n(3 points)']) / 15 * 100
    final_data['FIN6'] = (final['ES 6.1\n(25 points)'] + final['ES 6.2\n(15 points)']) / 40 * 100
    final_100 = pd.DataFrame(data=final_data)
    final = ['FIN1','FIN2','FIN3','FIN4','FIN5','FIN6']
    final_100['FIN1'] = final_100['FIN1'].fillna(0)
    final_100["final_score"] = final_100[final].sum(axis = 1)/6
    final_100

    return final_100


def rebase_mid(mid_grades):
    # Rebase score on 100
    mid_100 = mid_grades
    for i, col_name in enumerate(mid_grades.columns):
        if i == 0: continue
        max_score = mid_grades[[col_name]].max()
        mid_100[[col_name]] = round(mid_grades[[col_name]] / max_score * 100, 2)
        
    mid_100.columns = ['ID', 'MID2', 'MID3', 'MID4', 'MID5', 'MID6']
    return mid_100

def merge_mid_final(mid_100,final_100):
    # merge table
    grades = mid_100.merge(final_100, how='inner', on='ID')
    #grades3['FIN1'] = grades3['FIN1'].fillna(0)
    grades.replace(np.nan, 0)
    return grades

def standardize_grades(grades):
    cols = ['MID2', 'MID3', 'MID4', 'MID5', 'MID6', 'FIN2', 'FIN3', 'FIN4','FIN5', 'FIN6']
    ID_var = grades['ID']
    std = StandardScaler()
    features = grades[cols]
    data_std = std.fit_transform(features)
    data_std = pd.DataFrame(data_std, 
                        index=features.index,
                        columns=features.columns)
    data_std['ID'] = ID_var
    return data_std

def get_result(grades3):
    # add columns representing test result for each sesssion
    for i in range(2,7):
        mid_col = 'MID' + str(i)
        fin_col = 'FIN' + str(i)
        col_name = 'RES' + str(i)
        if i == 2:
            filter = grades3[fin_col]<(grades3[mid_col]*1.3)
        elif i == 3:
            filter = grades3[fin_col]<(grades3[mid_col]*1.2)
        elif i == 4:
            filter = grades3[fin_col]<(grades3[mid_col]*2)
        elif i == 5:
            filter = grades3[fin_col]<(grades3[mid_col]*1.8)
        elif i == 6:
            filter = grades3[fin_col]<(grades3[mid_col]*1.5)
        grades3[col_name] = filter*1
    

def save_grades(grades,outdir = 'Explore/data/grades2.csv'):
    grades.to_csv(outdir)

def main():
    mid,fin1,fin2 = read_grades()
    fin = final_manipulation(fin1,fin2)
    mid = rebase_mid(mid)
    grades = merge_mid_final(mid,fin)
    std_grades = standardize_grades(grades)
    get_result(std_grades)
    #save_grades(std_grades)
    print('Done!')

if __name__ == '__main__':
    main()








