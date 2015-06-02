---
layout: post
title: Announcing Pyvolve!
date:   2015-6-1
permalink: /announcing_pyvolve/
excerpt_separator: <!--more-->
---

Today, the preprint for my new software, [Pyvolve](http://sjspielman.org/pyvolve) was [published on biorXiv](http://dx.doi.org/10.1101/020214)! Pyvolve is an open-source Python module for simulating sequences along phylogenies. A comprehensive user-manual for Pyvolve is available with the most recent release from this [github repository](https://github.com/sjspielman/pyvolve).

<!--more-->


Pyvolve is written in pure Python, with dependencies of NumPy, SciPy, and Biopython. The Pyvolve framework is extremely flexible, allowing you to simulate sequences according to virtually all standard models of nucleotide, amino acid, and codon data, and you can customize *all* model parameters to your heart's content. Further, Pyvolve allows you to provide a custom rate matrix, if the available models are not quite what you're looking for (however, please feel free to get in touch with me if you would like to request that a new model be included!). 

Pyvolve incorporates both site and temporal heterogeneity, and, as you'll see in the preprint linked above, contains several novel simulation features. Below, I show some simple examples of Pyvolve simulations. In general, sequence simulations require several you to do a few things:

* Specify a phylogeny (with branch lengths!)
* Define any evolutionary model(s) to use. In Pyvolve, these are **Model** objects.
* Assign model(s) to partition(s). In Pyvolve, these are **Partition** objects.
* Evolve, using the callable **Evolver** class.

<br>

Partitions are essentially a convenient way of defining "domains" -- each partition can evolve according to a distinct evolutionary model (provided that all partitions evolve the same state, e.g. nucleotides, amino acids, or codons), and each partition can have differing degrees of heterogeneity. 

Examples shown below are minimal and do not capture the full power of Pyvolve -- to really see what Pyvolve can do, have a look at the [user manual](https://github.com/sjspielman/pyvolve/raw/master/user_manual/pyvolve_manual.pdf)!


## Simulating nucleotide sequences

This simple example demonstrates how to evolve nucleotide sequences.

{% highlight python %}
import pyvolve

# Define a phylogeny, from a file containing a newick tree
my_tree = pyvolve.read_tree(file = "file_with_tree.tre")

# Define a nucleotide model, as a Model object.
my_model = Model("nucleotide")

# Assign the model to a Partition. The size argument indicates to evolve 250 positions
my_partition = Partition(models = my_model, size = 250)

# Evolve!
my_evolver = Evolver(partitions = my_partition, tree = my_tree)
my_evolver()
{% endhighlight %}

<br>
The code shown above will simulate a nucleotide alignment of 250 positions along the phylogeny provided in `file_with_tree.tre`. This code simulates nucleotides according to default parameters: mutation rates among nucleotides are equal, and nucleotide equilibrium frequencies are equal at 0.25 each. We can customize these parameters by adding a *second argument to Model*: a dictionary of parameters to customize. 

To customize mutation rates, we can use the key `"mu"`. This key should have an associated value of a dictionary of mutation rates. Mutation rates are symmetric, denotated by keys `"AT"`, `"AC"`, etc. (where "AT" is the rate from A to T, and conversely T to A). To customize frequencies, we can use the key `"state_freqs"`, whose associated value should be a list/numpy array of frequencies ordered ACGT. 

This code chunk simulates nucleotide sequences with customized parameters:
{% highlight python %}
import pyvolve

# Define a phylogeny, from a file containing a newick tree
my_tree = pyvolve.read_tree(file = "file_with_tree.tre")

# Define a nucleotide model with custom parameters!
mutation = {"AC": 1.5, "AG": 2.5, "AT": 0.5, "CG": 0.8, "CT": 0.99, "GT": 1.56}
frequencies = [0.25, 0.3, 0.1, 0.35] # f(A) = 0.25, f(C) = 0.3, etc.
my_model = Model("nucleotide", {"mu": mutation, "state_freqs": frequencies} )

# Assign the model to a Partition.
my_partition = Partition(models = my_model, size = 250)

# Evolve!
my_evolver = Evolver(partitions = my_partition, tree = my_tree)
my_evolver()
{% endhighlight %}

For those of you who, like myself, tend towards some minor, completely socially-acceptable laziness, you can alternatively specify mutation rates with simply the key `"kappa"`, which represents the transition-to-transversion bias. Here's how to define such a model:
{% highlight python %}
# Define a nucleotide model kappa
frequencies = [0.25, 0.3, 0.1, 0.35] # f(A) = 0.25, f(C) = 0.3, etc.
my_model = Model("nucleotide", {"kappa": 3.25, "state_freqs": frequencies} )
{% endhighlight %}

<br>
Now we're cookin'! Let's add some more bells and whistles, like *rate heterogeneity*. In the simulations shown above, all positions evolve according to exactly the same model and the same rate. We can incorporate rate heterogeneity by adding a few *keyword arguments* when defining our Model object. In this example, we will specify rate heterogeneity with a custom distribution, although as you'll see in the [user manual](https://github.com/sjspielman/pyvolve/raw/master/user_manual/pyvolve_manual.pdf), you can also specify that rates be distribution according to a gamma distribution.

To implement rate heterogeneity (this holds for nucleotide and amino-acid models!), you need to specify the *scalar factors* which govern the heterogeneity, and a list of *probabilities* associated with each factor. This list will determine the probability that a given site evolves according to the associated factor. (Note that if you don't specify these probabilties, each category will be equally likely).

Let's go ahead and add in four rate categories, some slow and some fast, with associated probabilities. Specify a list of rate factors with the argument `rate_factors`, and specify a list of probabilities with the argument `rate_probs` (should sum to 1!). These lists are associated 1:1, as in the first item in `rate_factors` will have a probability equal to the first item in `rate_probs`.

{% highlight python %}
import pyvolve

# Define a phylogeny, from a file containing a newick tree
my_tree = pyvolve.read_tree(file = "file_with_tree.tre")

# Define our parameters
mutation = {"AC": 1.5, "AG": 2.5, "AT": 0.5, "CG": 0.8, "CT": 0.99, "GT": 1.56}
frequencies = [0.25, 0.3, 0.1, 0.35] # f(A) = 0.25, f(C) = 0.3, etc.

factors = [3.5, 2.5, 0.08, 0.005] # Two fast categories, and two slow categories
probs   = [0.05, 0.1, 0.5, 0.35]  # The fast rates will occur with relatively low probabilities

# Define our model with all parameters
my_model = Model("nucleotide", {"mu": mutation, "state_freqs": frequencies}, rate_factors = factors, rate_probs = probs)

# Assign the model to a Partition.
my_partition = Partition(models = my_model, size = 250)

# Evolve!
my_evolver = Evolver(partitions = my_partition, tree = my_tree)
my_evolver()
{% endhighlight %}
 
By default, Pyvolve outputs several files:
+ simulated\_alignment.fasta
+ site\_rates.txt
+ site\_rates\_info.txt

The first file contains the simulated alignment, and the latter two files contain information about site-specific rates and/or parameters. Using these two files, you can determine at which rate each site evolved. 


<br> And finally, one more example - what if we wanted to use *multiple models* in our simulation? For this task, we'll need to define multiple Partition objects. In the example below, one Partition object will be assigned default parameters, and one Partition will be assigned custom parameters.
{% highlight python %}
import pyvolve

# Define a phylogeny, from a file containing a newick tree
my_tree = pyvolve.read_tree(file = "file_with_tree.tre")

# Define default model
model1 = Model("nucleotide")

# Define customized model
mutation = {"AC": 1.5, "AG": 2.5, "AT": 0.5, "CG": 0.8, "CT": 0.99, "GT": 1.56}
frequencies = [0.25, 0.3, 0.1, 0.35] # f(A) = 0.25, f(C) = 0.3, etc.
model2 = Model("nucleotide", {"mu": mutation, "state_freqs": frequencies}, rate_factors = factors, rate_probs = probs)

# Assign each model to a Partition.
partition1 = Partition(models = model1, size = 100)
partition2 = Partition(models = model2, size = 200)

# Evolve, provided both partitions in a list to Evolver
my_evolver = Evolver(partitions = [partition1, partition2], tree = my_tree)
my_evolver()
{% endhighlight %}

In the resulting sequence file, the first 100 positions will have evolved according to `model1`, and the next 200 positions (there will be a total of 300 positions!) will evolve according to `model2`.


For more, yes more!, ways to use Pyvolve, check out the (drumroll...) [user manual](https://github.com/sjspielman/pyvolve/raw/master/user_manual/pyvolve_manual.pdf)! Please feel free to post any questions and/or file bug reports on Pyvolve's github repository Issues section. Enjoy!


<br><br><br>










