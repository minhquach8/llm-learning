document.addEventListener("DOMContentLoaded", function() {
    const input = document.getElementById("todo-input");
    const addButton = document.getElementById("add-todo");
    const todoList = document.getElementById("todo-list");

    // Load existing todos
    const todos = JSON.parse(localStorage.getItem("todos")) || [];
    todos.forEach(todo => addTodoElement(todo));

    // Add a new todo
    addButton.addEventListener("click", function() {
        const todoText = input.value.trim();
        if (todoText !== "") {
            const todo = { text: todoText, done: false };
            todos.push(todo);
            saveTodos();
            addTodoElement(todo);
            input.value = "";
        }
    });

    function addTodoElement(todo) {
        const li = document.createElement("li");
        const text = document.createElement("span");
        text.textContent = todo.text;
        text.style.textDecoration = todo.done ? "line-through" : "none";

        const editButton = document.createElement("button");
        editButton.textContent = "Edit";
        editButton.addEventListener("click", function() {
            const newText = prompt("Edit todo:", todo.text);
            if (newText !== null) {
                todo.text = newText.trim();
                saveTodos();
                text.textContent = todo.text;
            }
        });

        const deleteButton = document.createElement("button");
        deleteButton.textContent = "Delete";
        deleteButton.addEventListener("click", function() {
            todoList.removeChild(li);
            todos.splice(todos.indexOf(todo), 1);
            saveTodos();
        });

        text.addEventListener("click", function() {
            todo.done = !todo.done;
            text.style.textDecoration = todo.done ? "line-through" : "none";
            saveTodos();
        });

        li.appendChild(text);
        li.appendChild(editButton);
        li.appendChild(deleteButton);
        todoList.appendChild(li);
    }

    function saveTodos() {
        localStorage.setItem("todos", JSON.stringify(todos));
    }
});
