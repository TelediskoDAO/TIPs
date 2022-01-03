```
TIP: 3
Name: API access to Odoo models
Type: Standard
Status: raw
Editor: Alberto Granzotto @vrde
```

# API access to Odoo models

This document is governed by [TIP-0](../0).

## 1 Abstract

An important requirement for the successful implementation of the DAO is the integration with the Odoo API. Odoo stores crucial information about the activity of the DAO, such as: projects, tasks, and hours worked by its contributors, just to name few. By having easy access to the data stored in Odoo, Teledisko can build a variety of tools to streamline the participation to the DAO.

## 2 Motivation

Teledisko uses [Odoo ERP][odoo] for managing contribuors, projects, assets, do time tracking, and much more. Odoo offers a rich set of apps that can be customized to fulfill the needs of the company using it.

There are two main reasons why accessing Odoo data is important.

1. Teledisko is migrating to a DAO structure. This means that some of the data contained in Odoo must be available "in the blockchain". By being able to pull data from Odoo, a custom *Oracle* would be able to push updates to the smart contracts of the DAO.
2. Time tracking on Odoo is cumbersome. Contributors are currently doing time tracking on different apps ([Gleeo][gleeo], spreadsheets) and **then** update the timesheets in Odoo. This adds friction and makes time tracking more difficult that it should be. By being able to interact with Odoo models instead of the Odoo UI, we can redefine how time tracking works.

This TIP discusses what's the best approach to create, read, update, and delete records in Odoo from an external program.

## 3 Specification

Odoo exposes an external [RPC API][external-api] that can be used to extend the functionality of the system. The RPC API implement a JSON and an XML interface. Both interfaces are easily accessible from a variety of programming languages.

## 3.1 Project management models

We use three Odoo models for project management, `project`, `task`, and `duration`.

### 3.1.1 The "project" model


### 3.1.2 The "task" and model

Fields:

- Model name: `project.task`.
- Id: `id: <task_id>`.
- Type: `task` or `subtask`.
  - `task` if `is_subtask == false`, `task_id == false`.
  - `subtask` if `is_subtask == true`, `task_id == [<parent_task_id>, <parent_task_name>]`.
- Parent:
  - Tasks and subtasks belong to a project: `project_id: [<project_id>, <project_name>]`.
  - Subtasks belongs also to a task: `task_id: [<parent_task_id>, <parent_task_name>]`.
- Children:
  - If the task has subtasks: `subtask_ids: [<task_id>, ... ]`
- Title: `name: <name>`.
- Description: `description: <description>`.
- Customer/read only view: `access_url`.
- Assegnee: `user_id: [<user_id>, <user_name>]`.
- Supervisor: `controller: [<user_id>, <user_name>]`.
- Deadline: `date_deadline: "YYYY-MM-DD"`.
- Created: `create_date: "2020-06-04 14:45:48`.
- Last write: `write_date: "2020-06-04 14:45:48`.
- Kanban state: `stage_id: [<stage_id>, <stage_name>]`.
  - If the task has been created, then `stage_id: [1, 'Created']`.
  - If the task is in progress, then `stage_id: [5, 'In Progress']`.
  - If the task is done, then `stage_id: [2, 'Done']`.
  - If the task has been approved by the controller, then `stage_id: [3, 'Approved']`.
- Durations: `duration_entry: [<duration_id>, ...]`.
- Tier: `tier: false | [<tier_id>, <tier_name>]`


### 3.1.3 The "duration" model

- Model name: `project.task.duration`.
- Id: `id: <duration_id>`.
- Parent task: `task: [<task_id>, <task_name>]`.
- Creator: `create_uid: [<user_id>, <user_name>]`.
- Hours: `value: <duration_hours>`.
- Start: `start: YYYY-MM-DD hh-mm-ss`.
- End: `end: YYYY-MM-DD hh-mm-ss`.

## 4 Rationale

Accessing the Odoo API is a common issue, and has been tackled by custom modules like [MUK REST][mukrest] and [Odoo REST API][restapi].

Those modules don't provide much more than the standard RPC API shipped within Odoo, except for the *authentication* endpoint that we are going to implement with [TIP-3](../3).

Moreover, installing a new API module requires more work to install it, and maintain it. By having more code we might incur into bugs, security issues, and unexpected behavior.

## 5 Implementation

This TIP contains two different implementations, one in Python, the other in JavaScript.

### Python implementation

[Python source](./python). By using XML RPC, the script is able to retrieve the list of tasks of the current user.

### JavaScript (Node) implementation

[JavaScript source](./node). By using JSON RPC, the script is able to retrieve all tasks of the current user, and sums up the total amount of time spent per task.

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/)


[odoo]: https://www.odoo.com/
[external-api]: https://www.odoo.com/documentation/12.0/webservices/odoo.html
[webservices]: https://www.odoo.com/documentation/12.0/howtos/backend.html#webservices
[mukrest]: https://apps.odoo.com/apps/modules/13.0/muk_rest/
[restapi]: https://apps.odoo.com/apps/modules/13.0/restapi/
[gleeo]: https://gleeo.com/
