# Educational Process Mining

Team Members: Meredith Luo, Seyoung Nam, Yinsheng Kou, Youngwon Kim, Wenjin Zhang

## Logo

<img src="https://github.com/EPM-LearningAnalytics/epm/blob/main/logo.svg?raw=true" height="150" width="100">

## Background

It is recognized that **online learning** is becoming increasingly important. Especially during the COVID-19 pandemic, online learning is indispensable in billions of students’ learning journeys. We see that many online learning platforms have emerged, and there are various ways to record how students interact with these platforms in the form of log data. These log data, which cannot be collected in offline classes, should be helpful for instructors and students to understand the learning progress better. However, due to the complexity of the log data, it is challenging to make them interpretable and meaningful for students and instructors.

### **Project Objective**

Our project intends to build a **web tool** to make log data informative for students and instructors. Using our web tool, **students** can visualize their learning progress and receive guidance for the course review to boost their final grades. **Instructors** can better understand their students’ academic performance and easily construct student groups for the group project, which would possibly have a relatively similar academic potential between groups.

## Data Source

[Educational Process Mining (EPM): A Learning Analytics Data Set](https://archive.ics.uci.edu/ml/datasets/Educational+Process+Mining+(EPM)%3A+A+Learning+Analytics+Data+Set)

**Overview**: A group of 115 students of first-year, undergraduate Engineering major at the University of Genoa studied over a simulation environment named Deeds (Digital Electronics Education and Design Suite), and their log activities on the online learning platform, intermediate session grades, and final exam grades are recorded.

## Repository Structure

```md
.
├── epm
│   ├── data_prep
│   ├── graph
│   ├── modeling
│   └── tests
├── data
│   ├── Processes
│   ├── all_log.csv
│   ├── final_grades.xlsx
│   └── intermediate_grades.xlsx
├── docs
│   └── data_info  
├── Dockerfile
├── LICENSE
├── README.md
├── app.py
└── requirements.txt
 ```

### Project Design

<img src="docs/design1.jpg" height="250" width="450" align=center>

## Usage

### Requirements

To start, you need to have **docker** installed. Whatever system you use, follow the tutorial on <a href="https://docs.docker.com/get-docker/">docker's official website</a> and you can get it done smoothly.

### Installation

Clone this repository and run the following code under the repository's root directory:

```bash
docker build -t epm:latest .
```

Then run the following command under the same directory:

```bash
docker run -p 8501:8501 epm:latest
```

Turn to browser and navigate to the URL:localhost:8501

## Use Cases

### Student Use Case

1. Go to the `Log In` page, select `Student`

2. Type your **numeric** student ID under `ID` and your password, then click Log In

3. You can now check your log activities across six sessions under the `Behavior Analysis` section and your grades under the `Grades` section. You can also get suggestions for the final review under the `Review Alert` section.

### Instructor Use Case

1. Go to the `Log In` page, select `Instructor`

2. Type your ID name and Passord, then click Log In

3. You can now check every student's and class average log activities under the `Behavior Analysis` section and students' and average grades under the `Grades` section. Under the `Grouping Assistant` section, we provide you some suggestions for grouping students. We also provide information about who have logged in this website under the `User Profiles` section.

## Feature Request and Bug Report

We want our website to be helpful and informative to both instructors and students. If you would like to see any new features on our website, or if you have any suggestions for improvement or want to report a bug, please feel free to <a href="https://github.com/EPM-LearningAnalytics/epm/issues/new">raise a new issue</a>.

## Acknowledgements

This is a course project for CSE 583 Software Development for Data Scientists. Many thanks to professor David Beck and our TA, Anant Mittal. 