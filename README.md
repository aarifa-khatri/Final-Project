# Final-Project
A demonstration of our final project dashboard

The provided code needs an associated csv file, with data columns that are specified in the beginning of the code as well as a csv file with professors and comments on the professor. Note that these csv files are examples of what could be used in the future for a larger set of data in the ME department.
From left to right these columns store semester/year, professor name, image url, course prefix, course name, A (# of students with letter grade), B, C, other.
The code runs so that it outputs the dashboard on a web browser.
To display the dashboard, one will need to open the Command Prompt and have the file path lead to where the code is saved.
Then in the Command Prompt, type: "bokeh serve --show 'name_of_file'". This shows the dashboard/graphs on the web browser.
Make sure to save the Spyder code before typing the above statement in Command Prompt.
The code consists of reading the csv files, storing the data, and using the data to print pictures, comments, and grade distributions based on changing the name of the professor from a dropdown menu. 
