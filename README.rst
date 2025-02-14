.. start-longdesc

Scripts for testing Pharmpy with batches of models.

1. Activate one of the testing environments of Pharmpy.
2. `pip install pytest-timeout`
3. Run:

.. code-block::

  pytest -n10 --testdefs=testdefs/main.toml tests

.. end-longdesc

Workflow
--------

Put the user requirement you want to validate in a comment tag in the test file. For example:

```python
# validate: has_first_order_absorption detects first order absorption for ADVAN2 models
```

Implement test where reference point is not using Pharmpy nor is hard coded (e.g. use regex to check which ADVAN a model has)
