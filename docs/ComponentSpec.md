# Component Specification

Meredith Luo, Seyoung Nam, Yinsheng Kou, Youngwon Kim, Wenjin Zhang|[Team Repo](https://github.com/EPM-LearningAnalytics/EPM_Project)

## **Software components**

1. **Visualizations**
    * Visualizing students’ learning activities across sessions and comparing individual students’ learning performance with the class average.
    * **Input**
        * Log data will be used for plotting. On the users’ end, students need to provide ID numbers, and instructors need to choose the portal for teachers. Students then can select which session’s activities they want to take a closer look at or compare activities between sessions. Instructors can select which students they want to pay attention to. 
    * **Output**
        * On the HTML page, plots such as line plots, bar charts, and tables displaying descriptive statistics will be generated. 

2. **Machine learning models**
    * **Classification with k Nearest Neighbor(kNN)**
        * We will first aggregate the log activities data into meaningful explanatory variables and select a certain number of variables that are statistically significant to academic performance. Then we will divide three groups( students expected to achieve a low score, mid score, and high score in the final exam) by using the kNN model. This grouping function will ease the instructor’s work to create teams with a similar intellectual capacity by picking a student from three different groups.
    * **Log Regression**
        * We want to build a model to tell which section (or chapter) each student has not studied enough and thus needs to review the section before the final exam. For setting the output variable, we assume two scenarios. The first one is a student’s final exam score becomes deteriorated compared to the intermediate test score, which case is assigned 1. The second case is the opposite, meaning that the student’s score is improved. We assign this case to 0. For the input variables, we will process the log activities data, filter out statistically insignificant factors, and retrieve four to five factors with a high potential in explaining the output. 

3. **Database**
    * Log activities data of each student enrolled in the engineering course
    * Intermediate grades data
    * Final grades data

4. **A HTML page**
    * It displays visualizations, a grouping function for team projects, predictions of the final scores, and suggestions for students’ learning/reviewing for the final.
    * **Input**
        * First, they need to specify whether they are students or teachers. Second, if they are students, then they need to provide a student ID. 
    * **Output**
        * For students, they will see visualizations of their individual learning progress and they can compare it with the class average learning activities. They are also able to see based on their current learning activities, what’s the probability of them passing the final exam. Some suggestions on reviewing particular sessions could be provided. For teachers, they can see the visualizations of the whole class. They can also zoom in on one particular student. They are also able to see what the probability of passing the exam for every student is. 

## **Interactions to accomplish use cases**

Jenny intends to understand her learning progress better and get some advice on the final exam review. She signs in our application by specifying she is a student and providing her student ID. These two inputs from Jenny (i.e., student identity and student ID) satisfied the required inputs for both visualizations and the machine learning engine. On the webpage, various visual aids based on Jenny’s log activities will be generated. The machine learning engine will utilize Jenny’s log activities and predict which performance group Jenny belongs to and whether Jenny needs to review more before the final exam. 

## **Preliminary plan**

* A list of tasks in priority order
    1. Build machine learning models for EDM datasets 
    2. Choose the best model for EDM datasets 
    3. Search available design mockups of our webtool 
    4. Create our webtool’s graphic design
    5. Test the webtool
