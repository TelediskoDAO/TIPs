async function myTasks(s) {
  const tasks = await s.r("project.task", { user_id: s.uid });
  for (let task of tasks) {
    console.log(JSON.stringify(task, null, 2));
    // console.log(task.id, task.name);
  }
}

async function tasksByProject(s, projectId) {
  const tasks = await s.r("project.task", { project_id: projectId });
  for (let task of tasks) {
    console.log(JSON.stringify(task, null, 2));
    // console.log(task.id, task.name);
  }
}

async function durations(s) {
  const durations = await s.r("project.task.duration", { create_uid: s.uid });
  console.log(JSON.stringify(durations, null, 2));
}

async function myTrackings(s) {
  const durations = await s.r("project.task.duration", { create_uid: s.uid });
  const tasks = {};
  let total = 0;
  for (let duration of durations) {
    const [id, name] = duration.task;
    const value = duration.value;
    tasks[id] = {
      name,
      hours: value + (tasks[id] ? tasks[id].hours : 0),
    };
    total += value;
  }

  for (let key of Object.keys(tasks)) {
    console.log(`[${key}] ${tasks[key].name}: ${tasks[key].hours}h`);
  }
  console.log(`${total}h`);
  //  const task = tasks[key];
  //  const [id, name] = task.task;
  //  const hours = console.log(task);
  //  console.log;
  //}
}
module.exports = {
  myTasks,
  myTrackings,
  durations,
  tasksByProject,
};
