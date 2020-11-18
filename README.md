# Protocol, Strategies and Analysis for Enabling a Distributed Computation Market for Stream Processing

There are two branches for this codebase.
* streaming-0.1: full working version of our streaming framework. Used for performance measure experiments
and development of the streaming middleware.
* experiments-0.1: testbed for rapid testing of game theoretic approaches.

Directory structure
* src: source code. Instructions for running experiments is located at
src/README.md in streaming-0.1 and experiments-0.1.
* notebooks: jupyter notebooks for retrieving and visualizing 
experiment results.
* sandbox: utility applications


Environment setup
```bash
python -m pip install -r requirements.txt
```