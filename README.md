# Final-Project
A demonstration of our final project dashboard based on the Bokeh python package.
Our Bokeh dashboard displays an example of how we would like to improve the information organized on common professor review websites. On our dashboard displays the professor's picture, student comments, grade distribution individual professors, and an overall grade distribution of all professors in our CSV file. 

The provided code is accompanied with two csv files, one with grade distributions & image URLs from each professor as well as a csv file with professors and associated student comments. Note that these csv files are examples of what could be used in the future for a larger set of data in the ME department.
From left to right these columns store semester/year, professor name, image url, course prefix, course name, A (# of students with letter grade), B, C, other.
The code runs so that it outputs the dashboard on a web browser.

To display the dashboard, one will need to open the Command Prompt and have the file path lead to where the code is saved.
Then in the Command Prompt, type: "bokeh serve --show bokehproject1.py". This shows the dashboard/graphs on the web browser.
Make sure to save the Python code before typing the above statement in Command Prompt.

The code consists of reading the csv files, processing the data, and using the data to display images, comments, and grade distributions based on changing the name of the professor from a dropdown menu. There is one callback function used to change the info when coosing a different professor from the dropdown menu.
