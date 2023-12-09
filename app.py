from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import sqlite3 as sql

def add_task():
    task_string = task_field.get()
    if len(task_string) == 0:
        messagebox.showinfo('Error', 'Field is Empty.')
    else:
        priority = priority_var.get()
        category = category_var.get()
        tasks.append((task_string, priority, category))
        the_cursor.execute('insert into tasks (title, priority, category) values (?, ?, ?)', (task_string, priority, category))
        list_update()
        task_field.delete(0, 'end')

def list_update():
    clear_list()
    for task, priority, category in tasks:
        task_listbox.insert('end', f"{task} (Priority: {priority}, Category: {category})")

# defining the function to delete a task from the list  
def delete_task():
    try:
        # getting the selected index from the list box
        the_index = task_listbox.curselection()
        
        # checking if an item is selected
        if the_index:
            # getting the selected task from the list
            the_value = tasks[the_index[0]]
            
            # removing the task from the list
            tasks.remove(the_value)
            
            # calling the function to update the list
            list_update()
            
            # using the execute() method to execute a SQL statement
            the_cursor.execute('delete from tasks where title = ?', (the_value[0],))
    except Exception as e:
        # displaying the message box with 'No Task Selected' message for an exception
        messagebox.showinfo('Error', 'No Task Selected. Cannot Delete.')
        
def delete_all_tasks():
    message_box = messagebox.askyesno('Delete All', 'Are you sure?')
    if message_box == True:
        while len(tasks) != 0:
            tasks.pop()
        the_cursor.execute('delete from tasks')
        list_update()

def clear_list():
    task_listbox.delete(0, 'end')

def close():
    print(tasks)
    guiWindow.destroy()

def retrieve_database():
    while len(tasks) != 0:
        tasks.pop()
    for row in the_cursor.execute('select title, priority, category from tasks'):
        tasks.append(row)

if __name__ == "__main__":
    guiWindow = Tk()
    guiWindow.title("To-Do List With ❤️ created with love by Thiarara - V1.5 - Github for upgrade")
    
    # Adjusted width and height with padding and margin
    window_width = 680
    window_height = 500
    window_padding_x = 20
    window_padding_y = 20
    
    guiWindow.geometry(f"{window_width}x{window_height}+400+200")
    guiWindow.resizable(0, 0)
    guiWindow.configure(bg="#0C0032")

    style = ttk.Style()
    style.theme_create("custom", parent="alt", settings={
        "TButton": {"configure": {"background": "#D4AC0D", "font": ("Arial", 12, "bold")}},
        "TLabel": {"configure": {"background": "black", "foreground": "white", "font": ("Arial", 12)}},
        "TFrame": {"configure": {"background": "black"}},
        "TOptionMenu": {"configure": {"width": 10}},
    })
    style.theme_use("custom")

    the_connection = sql.connect('listOfTasks.db')
    the_cursor = the_connection.cursor()
    the_cursor.execute('create table if not exists tasks (title text, priority text, category text)')

    tasks = []

    functions_frame = Frame(guiWindow, bg="black")
    functions_frame.pack(side="top", fill="x")

    task_label = Label(functions_frame, text="Enter the Task:", font=("Arial", 12, "bold"), background="black",
                       foreground="white")
    task_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    task_field = Entry(
        functions_frame,
        font=("Arial", 12),
        width=35,
        foreground="black",
        background="white",
    )
    task_field.grid(row=0, column=1, padx=10, pady=10, sticky="w")

    priority_label = Label(functions_frame, text="Priority:", font=("Arial", 12, "bold"), background="black",
                           foreground="white")
    priority_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

    priority_options = ['Low', 'Medium', 'High']
    priority_var = StringVar()
    priority_var.set(priority_options[0])

    priority_menu = OptionMenu(functions_frame, priority_var, *priority_options)
    priority_menu.grid(row=1, column=1, padx=10, pady=10, sticky="w")

    category_label = Label(functions_frame, text="Category:", font=("Arial", 12, "bold"), background="black",
                           foreground="white")
    category_label.grid(row=1, column=2, padx=10, pady=10, sticky="w")

    categories = ['Work', 'Personal', 'Others']
    category_var = StringVar()
    category_var.set(categories[0])

    category_menu = OptionMenu(functions_frame, category_var, *categories)
    category_menu.grid(row=1, column=3, padx=10, pady=10, sticky="w")

    add_button = Button(
        guiWindow,
        text="Add Task",
        width=15,
        command=add_task,
    )
    add_button.place(x=20, y=100)

    task_listbox = Listbox(
        guiWindow,
        width=70,
        height=12,
        font=("Arial", 12),
        selectmode='SINGLE',
        background="WHITE",
        foreground="BLACK",
        selectbackground="#D4AC0D",
        selectforeground="BLACK"
    )
    task_listbox.place(x=20, y=150)

    del_button = Button(
        guiWindow,
        text="Delete Task",
        width=15,
        command=delete_task,
    )
    del_button.place(x=20, y=400)

    del_all_button = Button(
        guiWindow,
        text="Delete All Tasks",
        width=15,
        command=delete_all_tasks
    )
    del_all_button.place(x=140, y=400)

    exit_button = Button(
        guiWindow,
        text="Exit",
        width=15,
        command=close
    )
    exit_button.place(x=260, y=400)

    guiWindow.mainloop()
    the_connection.commit()
    the_cursor.close()
