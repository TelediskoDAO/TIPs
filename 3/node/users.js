async function users(s) {
  const tasks = await s.r("res.users", [], {
    fields: ["display_name", "email", "ethereum_address"],
  });
  for (let task of tasks) {
    console.log(JSON.stringify(task, null, 2));
    // console.log(task.id, task.name);
  }
}

module.exports = {
  users,
};
