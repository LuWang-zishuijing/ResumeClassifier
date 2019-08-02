# ResumeClassifier
When a producer/director plans for new movie production, she usually arrange auditions for casting purposes. There will of course be many applicants to apply. Without reading the resumes or recommendations for all of the applicants through, how could she quickly filter out those disqualified applicants? of course, this system addresses this problem by automatically reading the reference letters through and recommend the producer/director about promising candidates to arrange an audition.


##Methods
#*Data Collection.  Implement a crawler that scrapes data from Wikipedia. The targeted are from an IMDB dataset. 
#*Multi-Label Classification. In the training data set, each actor is tagged with movie types she has cast a role in. With this data, we create a classifier for each movie type, which could predict whether a candidate would succeed in a specific movie type, then combine the results together to know whether a candidate could be a good fit.
#*Latent Dirichlet Allocation(LDA). Categorizing the actors by the movie types they cast in is just one way. As an alternative experiment, I want to automatically cluster actors with an unsupervised learning approach. Based on the assumption that the actors wikipedia pages conforms a “hidden-topic” based model. I used LDA to implement topic-based statistical model as well.

##Conclusion and Further Steps:
#*One vs Rest transforms the multi-label problem into a set of binary classification problems.
#*LDA can be used to measure performance on information retrieval. 
#*Each industry has its own requirements. Take the movie industry for example, in the initial casting stage, it is usually required to consider both the candidate’s professional experience and her visual appearance. Therefore, in order to improve the accuracy of screening, in addition to improving the resume analysis model, analyzing video, image materials submitted by the candidate is also necessary.
#*It should be possible to apply these methods to other industries to help accelerate hiring and screening process.

##Involved Technologies:
Python, NumPy, pandas, nltk, sklearn, genism, AWS EC2, SQL, Spark, Flask, Bootstrap

##Reference:
https://towardsdatascience.com/topic-modeling-and-latent-dirichlet-allocation-in-python-9bf156893c24
https://radimrehurek.com/gensim/models/ldamodel.html
https://pyldavis.readthedocs.io/en/latest/modules/API.html#pyLDAvis.prepare
https://towardsdatascience.com/journey-to-the-center-of-multi-label-classification-384c40229bff

