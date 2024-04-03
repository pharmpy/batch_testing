.. start-longdesc

Scripts for testing Pharmpy with batches of models.
Activate one of the testing environments of Pharmpy and then run

.. code-block::

  pytest --model_dir=mypath tests

.. end-longdesc

Workflow
--------

1. Add validation story as issues with priority tags
2. Use clear, short titles for issues to easily get an overview (e.g. "Test that $SIZES is added correctly when adding thetas")
3. Implement test where reference point is not using Pharmpy nor is hard coded (e.g. use regex to check that $SIZES has been added)
