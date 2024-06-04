# Tiler-Swift

Tiler-Swift is an efficient tiling software to speed up sparse tensor operations on coarse-grained reconfigurable arrays (CGRAs) [1]. We will show the run time comparison between different sparse tiling strategies. This software will contain a tile size searching algorithm and an application performance model. They work as a feedback loop to determine the best tiling size to execute on CGRAs.

# Background and Setup

<!--

(approx 1 page)

Provide a description of the problem being solved.  The description can be short (like the introduction section of a paper), but make sure you hit all the main problem definition points we talked about in class:

* What are the inputs/outputs?
* What are the goals/constraints on a solution?
* What is the question that you are asking and trying to answer? (Or equivalently: what is the falsifiable hypothesis that your results will either falsify or support?)

And finally, given this setup of goals and constraints...
* What is the crux of the problem to solve? (What is the hard part of the project that forced you to learn something or figure something out.)
-->

# Approach

<!--

(approx 1-2 pages max)

Please describe your approach.  Please be brief (about a page or so max), but your description should be sufficiently detailed to provide the course staff a basic understanding of your approach. It might be very useful to include a figure here illustrating components of the system and/or their mapping to parallel hardware/or a DNN architecture.

* If your project involved optimizing code. Please describe the process of how you iterated toward a solution (what measurements did you make) What did you try that did not work? How to parts of the problem map to cores, threads, or vector lanes?

* If your project involved optimizing a DNN architecture, you could describe the architecture here, and be sure to provide intuition about how your model architecture choices were motivated by your goals.

* __If your project involved started with an existing piece of code or DNN model, please clearly describe what you started with here, so it's clear what work you actually did in your project. e.g., "We started with this codebase and made these changes..."__
-->

# Evaluation and Results

<!--

(as many pages as needed to make the points you want to make)

To the staff, this is the most important part of the writeup. Begin by providing your own definition of success (this should be in terms of your goals). In other words, re-iterate the question you were trying to answer, or the performance boost you were hoping to obtain. Then describe what data/experiment needs to be run to provide evidence that the goals were either met or not met.

Now describe the relevant parts of your experimental setup. What were the baseline algorithms? What machine was a performance test run on? What did you measure? What was the dataset used?  If you have a programming abstraction project, the experimental setup might include a description of the programs you implemented expressed using the API.

Finally, I want to see the results of an experiment that demonstrate success (or failure) to meet goals. Sometimes great projects fail to meet their goals, or falsify a hypothesis, but they still do a great job in the scientific process of verifying this.

This might include:

* Provide graphs of speedup or execution time?
* Compare total flops or model size
* Compare precision and recall of a model.
* Demonstrate that a 3D NeRF model was obtained, show output images of sufficient quality, etc.

IMPORTANT: In this writeup, I want you to interpret your graphs and numbers for me. What this means will be project dependent, but I want you to consider questions such as: Why does the graph look like it does? Does it make sense to you? What limited your speedup? Is it a lack of parallelism? (dependencies) Communication or synchronization overhead? Data transfer (memory-bound or bus transfer bound)? If a model is performing well, what are it's failure cases? When does it fail to generalize.

As you answer these questions, provide data and measurements to support your conclusions. If you are merely speculating, please state this explicitly. Performing a solid analysis of your implementation is a good way to pick up credit even if your optimization efforts did not yield the performance you were hoping for.
-->


# Team Responsibilities

<!--
Please provide a [very short] breakdown of which parts of the project were performed by each team member. In general we hope to (and intend to) give all team members the same grade, but we still want to know what everyone worked on and what their role was.   
-->

# References
[1] K. Koul, et. al, "AHA: An Agile Approach to the Design of Coarse-Grained Reconfigurable Accelerators and Compilers," in ACM Transactions on Embedded Computing Systems (TECS), April 2022 (https://dl.acm.org/doi/full/10.1145/3534933)

[2] O. Hsu, et. al, "The Sparse Abstract Machine," in International Conference on Architectural Support for Programming Languages and Operating Systems (ASPLOS), March 2023 (https://dl.acm.org/doi/10.1145/3582016.3582051)

[3] R. Lacouture, et. al, "comal" (https://github.com/stanford-ppl/comal)

[4] T. O. Odemuyiwa, et. at, "Accelerating Sparse Data Orchestration via Dynamic Reflexive Tiling," in International Conference on Architectural Support for Programming Languages and Operating Systems (ASPLOS), March 2023 (https://dl.acm.org/doi/10.1145/3582016.3582064)
