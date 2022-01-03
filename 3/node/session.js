const uuid = require("uuid");
const fetch = require("node-fetch");

async function jsonRpc(url, method, params) {
  const data = {
    jsonrpc: "2.0",
    method: method,
    params: params,
    id: uuid.v4(),
  };

  const response = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    redirect: "follow",
    body: JSON.stringify(data),
  });
  const json = await response.json();
  if (json.result !== undefined) {
    return json.result;
  } else if (json.error.data.message !== undefined) {
    throw new Error(json.error.data.message);
  } else {
    throw new Error(response);
  }
}

async function call(url, service, method, ...args) {
  return await jsonRpc(url, "call", {
    service: service,
    method: method,
    args: args,
  });
}

function tuplify(query = {}) {
  const params = [];
  for (let key of Object.keys(query)) {
    params.push([key, "=", query[key]]);
  }
  return params;
}

async function session(url, db, username, password) {
  const uid = await call(url, "common", "login", db, username, password);
  const model = call.bind(null, url, "object", "execute_kw", db, uid, password);
  return {
    c: async (name, object) => model(name, "create", [object]),
    r: async (name, query) => model(name, "search_read", [tuplify(query)]),
    u: async (name, id, object) => model(name, "write", [[id], object]),
    uid,
  };
}

module.exports = session;
