# Educational Process Mining
Team Members: Meredith Luo, Seyoung Nam, Yinsheng Kou, Youngwon Kim, Wenjin Zhang

## Logo
![image](https://github.com/EPM-LearningAnalytics/epm/blob/main/logo.svg?raw=true)

## Background

It is recognized that online learning is becoming increasingly important. Especially during the COVID-19 pandemic, online learning is indispensable in billions of students’ learning journeys. We see that many online learning platforms have emerged, and there are various ways to record how students interact with these platforms in the form of log data. These log data, which cannot be collected in offline classes, should be helpful for instructors and students to understand the learning progress better. However, due to the complexity of the log data, it is challenging to make them interpretable and meaningful for students and instructors. 

## Project Objective
Our project intends to build a web tool to make log data informative for students and instructors. Using our web tool, **students** can visualize their learning progress and receive guidance for the course review to boost their final grades. **Instructors** can better understand their students’ academic performance and easily construct student groups for the group project, which would possibly have a relatively similar academic potential between groups.

## Data source

[Educational Process Mining (EPM): A Learning Analytics Data Set](https://archive.ics.uci.edu/ml/datasets/Educational+Process+Mining+(EPM)%3A+A+Learning+Analytics+Data+Set)

**Overview**: A group of 115 students of first-year, undergraduate Engineering major at the University of Genoa studied over a simulation environment named Deeds (Digital Electronics Education and Design Suite), and their log activities on the online learning platform, intermediate session grades, and final exam grades are recorded.

## Repository Structure
```
.
├── LegTextScraper
│   ├── states
│   ├── test
│   └── dashboard_helper.py
├── data
│   ├── dashboard
│   └── states
├── doc
├── examples
├── LICENSE
├── README.md
├── app.py
├── environment.yml
├── requirements.txt
└── travis.yml
 ```
## Installation
This application is running upon the Docker container. Please download and install Docker from [its official website](https://docs.docker.com/get-docker/) if you have not installed Docker in your operating system. After the installation, please follow the steps below.

1. In your command-line interface, move to the directory Dockerfile is located (root directory of this project).
2. Build the Docker image by entering the following command.
    ```console
    $ docker build -t epm:latest .
    ```
3. Run app.py on the Docker image.
    ```console
    $ docker run -p 8501:8501 epm:latest
    ```
4. To run the application, open your Internet browser and enter `localhost:8501`.

## Usage


## Use Cases
- Jenny is taking the engineering course using Deeds. At the beginning of the course, she was very determined to strengthen her basic knowledge of electronics and complete the course successfully. However, after two months of her study, she found herself not paying enough attention to the course and easily distracted by YouTube videos and social media while taking the course. As the final exam date approaches, she wants to stop her bad habits and set up the course review plan to boost her performance in the final exam. To do so, she signs in to our application, types in her ID, and takes a look at her log activities with visual aids. She becomes very embarrassed by the fact that she actually spent more time being idle (meaning she did something else during the study) than time spent studying on the platform. Additionally, she receives recommendations about which chapter she needs to cover first before the final. Because of the recommendation, she successfully completes the course with a much higher score than the class average in the end.   
- Professor Beck teaches an engineering course this quarter. Near the end of this quarter, he is concerned if students in this course would pass the final. Logging into our web and specifying that he is a teacher identity, he can get some plotted view about the student’s logging activities during the past quarter. With a plot about which course recordings are reviewed more frequently, he may have a clear perception about which part of the course makes a bigger impact on the class. He can also identify students who likely fail the course. The prediction is based on our machine learning model. If he focuses on a specific student, he would type in that student’s ID, and our system will output the recordings of his/her logging activities.

## Feature Request and Bug Report
We want our website to be helpful and informative to both instructors and students. If you would like to see any new features on our website, or if you have any suggestions for improvement or want to report a bug, please feel free to <a href="https://github.com/EPM-LearningAnalytics/epm/issues/new">raise a new issue</a>.

## Acknowledgements
