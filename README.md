# Plastic ORM
An ORM that molds itself to the data


Currently in beta validation. SQLite is the initial test.
See the `dev/` directory for example usage.


# Quickstart

Here's a quick way to get some data out of a SQLite database file:

```python
>>> from plastic.connectors.sqlite import PlasticSqlite
>>> PlasticSqlite._dbInfo = './dev/sqlite-test.db'
>>> class Task(PlasticSqlite): pass
>>> print(Task.find(Task.id[3:]))
[task(id=4,active=0,title='Uninteresting',description='Not much to say here.'),
 task(id=5,active=1,title='Very important',description=None)]
```

To change a record you can set it this way:
```python
>>> task = Task(id=4)
>>> print(task)
task(id=4,active=0,title='Uninteresting',description='Not much to say here.')
>>> task.title = "A bit more interesting"
>>> task._commit()
>>> print(Task(id=4))
task(id=4,active=0,title='A bit more interesting',description='Not much to say here.')
```

> Note: To avoid the need to call `_commit()`, set `_autocommit=True`. 
>   This can be done at the object or class level.
> Also note that for SQLite a commit means _the database file is updated_!

Any column of the table can be referenced as an attribute, and they can also be used as a filter. 
For example, to find the tasks that are still active:
```python
>>> print({task.title: task.description 
           for task 
           in Task.find(Task.active[0])})
{'Skipped': None, 'A bit more interesting': 'Not much to say here.'}
```

Add an entry by instantiating without a bound key:

```python
>>> newTask = Task()
>>> newTask.title = "A new task to do"
>>> newTask.active = True
>>> newTask._commit()
>>> print(Task.find(Task.id[5:])) # get tasks after the last added
[task(id=6,active=1,title='A new task to do',description=None)]
```

Deletion is _not_ yet supported. It wouldn't be hard, but there needs to be some sort of interlocking.
