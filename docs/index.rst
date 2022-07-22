.. cd4ml documentation master file, created by
   sphinx-quickstart on Fri Jul 22 14:46:01 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

CD4ML
=================================

Module built to enable the automation of Machine Learning workflows.

Main concepts
--------------

* Tasks: a function or a class containing a ``run`` method that can be executed in a workflow
* Workflow: sequence of tasks in dependency order that can be run sequentially
* Experiment: a Workflow can be run as an experiment to save data from previous steps and register parameters and outputs
* Provider: the execution environment to run the experiments.


.. toctree::
   :maxdepth: 1
   :caption: Getting Started

   index

Module Documentation
=====================


.. toctree::
   :maxdepth: 2
   :caption: Contents:

.. toctree::
   :maxdepth: 3
   :caption: Modules

   modules/modules


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
