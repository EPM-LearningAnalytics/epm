#!/usr/bin/env python
# coding: utf-8
"""
This module preprocess the grades files
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler


def read_grades(dir1='../../data/intermediate_grades.xlsx',
                dir2='../../data/final_grades.xlsx'):
    """
    Read grades.xlsx files
    Parameters
    ----------
    dir1: intermidiate grades path
    dir2: final grades path
    """
    # Get intermediate grades
    mid_grades = pd.read_excel(dir1)
    # Get final grades
    xl_file = pd.ExcelFile(dir2)
    sheet_name = xl_file.sheet_names
    final_1st = pd.read_excel(dir2, sheet_name=sheet_name[0])
    final_2nd = pd.read_excel(dir2, sheet_name=sheet_name[1])
    return mid_grades, final_1st, final_2nd


def final_manipulation(final_1st, final_2nd):
    """
    This function merge two final grades into one single file
    Parameters
    ----------
    final_1st: first final grades dataframe
    final_2nd: second final grades dataframe
    Return
    ----------
    A dataframe of one final grades
    """
    # Error meassages
    if not isinstance(final_1st, pd.DataFrame) is True:
        raise ValueError("'final_1st' should be should be a panda dataframe.")
    if not isinstance(final_2nd, pd.DataFrame) is True:
        raise ValueError("'final_2nd' should be should be a panda dataframe.")
    # Students who took exams twice
    twotimer = list(set(final_1st['Student ID']).intersection(set(final_2nd['Student ID'])))
    # 1st test takers without taking the second exam
    final_2nd_unique = final_2nd[-final_2nd['Student ID'].isin(twotimer)]
    # Students who took final exams (selected twotimers' first exam score)
    final = final_1st.append(final_2nd_unique).sort_values(by=['Student ID'])
    final_data = {'ID': final['Student ID']}
    # aggregate grades of each session
    final_data['FIN1'] = (final['ES 1.1 \n(2 points)'] + final['ES 1.2 \n(3 points)']) / 5 * 100
    final_data['FIN2'] = (final['ES 2.1\n(2 points)'] + final['ES 2.2\n(3 points)']) / 5 * 100
    final_data['FIN3'] = (final['ES 3.1\n(1 points)'] + final['ES 3.2\n(2 points)'] +
                          final['ES 3.3\n(2 points)'] + final['ES 3.4\n(2 points)'] +
                          final['ES 3.5\n(3 points)']) / 10 * 100
    final_data['FIN4'] = (final['ES 4.1\n(15 points)'] + final['ES 4.2\n(10 points)']) / 25 * 100
    final_data['FIN5'] = (final['ES 5.1\n(2 points)'] + final['ES 5.2\n(10 points)'] +
                          final['ES 5.3\n(3 points)']) / 15 * 100
    final_data['FIN6'] = (final['ES 6.1\n(25 points)'] + final['ES 6.2\n(15 points)']) / 40 * 100
    final_100 = pd.DataFrame(data=final_data)
    final = ['FIN1', 'FIN2', 'FIN3', 'FIN4', 'FIN5', 'FIN6']
    final_100['FIN1'] = final_100['FIN1'].fillna(0)
    final_100["final_score"] = final_100[final].sum(axis=1)/6
    return final_100


def rebase_mid(mid_grades):
    """
    Rescale mid scores to scores out of 100

    Parameters
    ----------
    mid_grades: first final grades dataframe

    Return
    ----------
    A dataframe of converted mid scores into 100 score bases
    """
    # Error meassage
    if not isinstance(mid_grades, pd.DataFrame) is True:
        raise ValueError("'final_1st' should be should be a panda dataframe.")
    # Rebase score on 100
    mid_100 = mid_grades
    for i, col_name in enumerate(mid_grades.columns):
        if i == 0:
            continue
        max_score = mid_grades[[col_name]].max()
        mid_100[[col_name]] = round(mid_grades[[col_name]] / max_score * 100, 2)
    mid_100.columns = ['ID', 'MID2', 'MID3', 'MID4', 'MID5', 'MID6']
    return mid_100


def merge_mid_final(mid_100, final_100):
    """
    Merge midterm grades and final grades

    Parameters
    ----------
    mid_100: midterm grades dataframe
    final_100: final grades dataframe

    Return
    ----------
    A dataframe containning all grades
    """
    # Error meassages
    if not isinstance(mid_100, pd.DataFrame) is True:
        raise ValueError("'mid_100' should be should be a panda dataframe.")
    if not isinstance(final_100, pd.DataFrame) is True:
        raise ValueError("'final_100' should be should be a panda dataframe.")
    # Merge two dataframes into one
    grades = mid_100.merge(final_100, how='inner', on='ID')
    grades.replace(np.nan, 0)
    return grades


def standardize_grades(grades):
    """
    Normalize grades

    Parameters
    ----------
    grades: A dataframe containning all grades

    Return
    ----------
    A dataframe containning standardized grades
    """
    # Error meassage
    if not isinstance(grades, pd.DataFrame) is True:
        raise ValueError("'grades' should be should be a panda dataframe.")
    # Standzrdize all scores
    cols = ['MID2', 'MID3', 'MID4', 'MID5', 'MID6', 'FIN2', 'FIN3', 'FIN4', 'FIN5', 'FIN6']
    id_var = grades['ID']
    std = StandardScaler()
    features = grades[cols]
    data_std = std.fit_transform(features)
    data_std = pd.DataFrame(data_std,
                            index=features.index,
                            columns=features.columns)
    data_std['ID'] = id_var
    return data_std


def get_result(grades):
    """
    Measure the performance measure for each sesssion

    Parameters
    ----------
    grades: A dataframe containning all standardized grades

    Return
    ----------
    A dataframe with performance measurement
    """
    # Error meassage
    if not isinstance(grades, pd.DataFrame) is True:
        raise ValueError("'grades' should be should be a panda dataframe.")
    # Student behavior changes
    for i in range(2, 7):
        mid_col = 'MID' + str(i)
        fin_col = 'FIN' + str(i)
        col_name = 'RES' + str(i)
        if i == 2:
            behavior_filter = grades[fin_col] < (grades[mid_col]*1.3)
        elif i == 3:
            behavior_filter = grades[fin_col] < (grades[mid_col]*1.2)
        elif i == 4:
            behavior_filter = grades[fin_col] < (grades[mid_col]*2)
        elif i == 5:
            behavior_filter = grades[fin_col] < (grades[mid_col]*1.8)
        elif i == 6:
            behavior_filter = grades[fin_col] < (grades[mid_col]*1.5)
        grades[col_name] = behavior_filter*1
    return grades


def save_grades(grades, outdir='EPM_dataset/Data/complete_grades.csv'):
    """
    Save processed grades to the path

    Parameters
    ----------
    grades: well-done grades dataframe to save
    outdir: the path to save files in

    return
    ----------
    Show the result of saving grades, "Saved"
    """
    # Error meassage
    if not isinstance(grades, pd.DataFrame) is True:
        raise ValueError("'grades' should be should be a panda dataframe.")
    # Save
    grades.to_csv(outdir)
    return print("Saved")
