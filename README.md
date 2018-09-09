# Vote-Aggregation
Some algorithms exploring the problem of aggregating votes from a number of sources, attempting to find and discredit outliers.
Voting is an extremely common task, and occurs every day, from ratings on Amazon, to voting on movie ratings.

We explore different methods of aggregating votes, and try come up with a robust way to aggreagte all the scores, and try to ensure that collusion against the system is determined and ruled out in the final outcome. Collusion being an attempt, by some number of voting parties to vote in a particular way which would skew the system.

# Setup
We setup voters as "sensors" gathering temperature data. their votes constitue a temperature reading at some given time t. So each sensor has TT number of sensor readings. TT = 288 temp readings in the day.
The temperature data is generated using a sin function, and the readings are created randomly using a bayesian distribution. The variances of this distribution are provided randomly to each sensor.
The goal is to have an algorithm which attempts to evaluate what the variances of these sensors might be, in order to provide weights to each sensor and so the submitted readings from each sensor will be aggregated accordingly.

# Credit
This is a python implementation of mathematica code by Aleks Ignjatovic, as part of an Advanced Algorithms course from the University of New South Wales Sydney.

Though I have implemented the code in python, the setup and equations used for this were obtained from the mathematica code provided within the course.

Papers on the topic:
https://www.researchgate.net/publication/257676510_Robust_evaluation_of_products_and_reviewers_in_social_rating_systems

https://www.researchgate.net/publication/279070608_An_Iterative_Algorithm_for_Reputation_Aggregation_in_Multi-dimensional_and_Multinomial_Rating_Systems
