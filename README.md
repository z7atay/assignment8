# Assignment 8
The program contains an app for a fictional weekly cafeteria written in Python.

# Functions
The main functions include:

I) collectFormData()
     return dict meal
   This function returns the state of the widgets from the root window, saves the results in a dictionary meal and passes on the results to function addMeal()
   
II) addMeal()
   This function creates a nested dictionary by adding the meals to dictionary with weekdays as keys.

III) saveWeekly()
   This function saves the nested dictionary from addMeal() to file. 

IV) iterateNestedDict(dict weekly)
      return string weekly
     
     This function is called by the displayWeekly() function when the content read from file is formatted to a string.

V) displayWeekly()
 
   This function reads the locally saved weekly meal planner from a text file and displays the content in an info box.
   In case the user has not saved to file yet, the weekly meal plan is displayed from session in an info box.
   In case no weekly meal plan was created either in session or as file the user is prompted to create on. 

VI) download()
   This function enables the user to download the weekly meal planner text file to their local machine.

# User Input

The user is prompted to select mains, dessert from the drop downboxes and select drinks by clicking the relevant check boxes.
Meals can be added per day and the weekly meal plan saved to file.
The user can choose to display the weekly meal from file or session and download the weekly meal plan.

# Output

The user will see the weekly plan in a info box.

# License

z7atay/assignment is licensed under the

GNU General Public License v3.0
Permissions of this strong copyleft license are conditioned on making available complete source code of licensed works and modifications, which include larger works using a licensed work, under the same license. Copyright and license notices must be preserved. Contributors provide an express grant of patent rights.
