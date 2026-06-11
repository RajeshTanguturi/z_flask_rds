async function loadTasks() {

    const response = await fetch("/tasks");
    const tasks = await response.json();

    const taskList = document.getElementById("taskList");

    taskList.innerHTML = "";

    tasks.forEach(task => {

        const li = document.createElement("li");

        li.innerHTML = `
            <div>
                ${task.task_name}
                <span class="status ${task.status.toLowerCase()}">
                    ${task.status}
                </span>
            </div>

            <div>
                <button onclick="markDone(${task.id})">
                    Done
                </button>

                <button onclick="deleteTask(${task.id})">
                    Delete
                </button>
            </div>
        `;

        taskList.appendChild(li);
    });
}


async function addTask() {

    const input = document.getElementById("taskInput");

    if (!input.value.trim()) return;

    await fetch("/tasks", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            task_name: input.value
        })
    });

    input.value = "";

    loadTasks();
}


async function markDone(id) {

    await fetch(`/tasks/${id}`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            status: "Done"
        })
    });

    loadTasks();
}


async function deleteTask(id) {

    await fetch(`/tasks/${id}`, {
        method: "DELETE"
    });

    loadTasks();
}


loadTasks();