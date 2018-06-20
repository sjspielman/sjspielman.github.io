---
layout: post
title: "Inaugural 'Behind the Scenes'"
categories: behindthescenes
date:  2018-06-10
comments: true
permalink: /bts_rates
---

Herein lies my inaugural **~~ BEHIND THE SCENES ~~** (you can tell it's serious because of the tildes) blog post, where I give all you eager readers a glimpse into how this project came together. [Note: this one is about my new paper with Sergei Pond, *The substitution model is largely irrelevant for site-specific protein relative rate inference*, which was just published in MBE.]

I want to do this for a few reasons. The cynical reason, of course the most important, is that I'm not great at blog maintenance (for example my last post was three years ago..), so this gives me something concrete to talk about on a regular basis. 

The more appropriate reasons are as follows - 

+ Nobody *really* reads papers, unless it's for a journal club where *you're* the presenter. If I do a damn fine blog post about it though, maybe you'll be inspired to read the paper for reals. Or, maybe you'll get the whole gist of the paper without having to read it (aka living the dream).
+ When you *do* read a paper, "you think you know, but you have no idea" (apologies) how that paper actually came together. More often than not, the paper you read represents the authors' *conversion* of the actual science done into a nicely packaged story. Missing from this neat little package are many of the failed attempts along the way, the side-paths briefly visited but ultimately abandonned to return to the main road. Project -> paper is a highly non-linear process. So, in these blogs, I'd like to share how the paper came about, highlighting aspects that are complementary to the paper itself. I'd also like to offer some more practical implications, when applicable, of the research.

# Behind the scenes


## Project Background

We wrote [LEISR](https://peerj.com/articles/4339/), an implementation of site-specific relative rates analysis, based on the [Rate4Site approach](https://www.tau.ac.il/~itaymay/cp/rate4site.html) from Tal Pupko's lab at Tel Aviv University. Briefly, LEISR (and Rate4Site) infer, given a fixed tree and multiple sequence alignment (MSA), a rate $$s_i$$ for each site $$i$$ in the MSA. Each $$s_i$$ is effectively a branch-length scaling parameter that tells you how quickly site $$i$$ evolves *relative* to the mean gene-wide evolutionary rate. So, high rates are quickly-evolving sites potentially under positive selection, and low rates are highly conserved sites potentially with strong functional/structural constraints.

We wrote LEISR largely because of my colleagues, and myself, use Rate4Site to study protein evolution but are often thwarted by some algorithmic nuisances. This was really never intended to be a major project, but rather a small side-project to faciliate others, and my own, ability to infer protein evolutionary rates from large and complex datasets in a more flexible manner. 

Then, we figured, "well since we published LEISR, we might as well do something with it?". This is, of course, an extremely scientifically advanced and technical grounding for launching a new project (i.e., this is NEITHER advanced nor technical, and yet some pretty solid science came out of it regardless!). The original goal of the project was to BREAK rate inference. More formally, we asked "What kind of data, inferred with what kind of model, can we feed LEISR to totally destroy any semblance of rate accuracy?" We hoped to identify niche cases where site-wise rate inference failed and gain some insights into why models behave differently under different conditions. 


With this goal in mind, we collected a diverse set of natural protein sequences from different taxonomic scopes ("general", mammalian-only, chloroplast-only, and mitochondrial-only), and threw the LEISR kitchen sink at them. We applied chloroplast models to mitochondrial data, HIV-specific models to mammalian data, etc. We even ran all alignments through with the uninformative and phylogenetically-toxic Jukes Canter (i.e. Poisson or equal-rates) model which universally is the worst-fitting model to any reasonably-sized dataset.

We tried, oh how we tried, to break the rates. But the damn things just wouldn't budge. 
<div class="tenor-gif-embed" data-postid="10391573" data-share-method="host" data-width="25%" data-aspect-ratio="1.5" ><a href="https://tenor.com/view/austin-powers-why-wont-you-die-gif-10391573">Austin Powers Why Wont You Die GIF</a> from <a href="https://tenor.com/search/austinpowers-gifs">Austinpowers GIFs</a></div><script type="text/javascript" async src="https://tenor.com/embed.js"></script>


Rates remained effectively identical across models, no matter what we tried.  Now, importantly, the actual rate estimates differed quite bit across models, albeit rarely significantly. The $$log(s_i)$$, which are a more natural measure for comparing these values due to the shape of their distributions, were correlated at $$r\geq0.98$$. Usually when I see consistently high correlations like this, my BS radar starts beeping; I got pretty skeptical and started hunting for bugs. 

## Deleted Scenes

I embarked to convince myself that the high rate correspondance, despite substantial differences in model was, in fact, real. I tried the following approaches:

1. Since LEISR (and other analogous implementations) consider a fixed tree topology, it's possible that all inferences were biased towards this fixed tree somehow. For a given alignment, the *same* tree (which was inferred with the LG+F model) was used to infer all rates for all models. I therefore re-built trees with two different models, WAG and JC, and re-inferred rates again using different trees. **The rates were still the same.** So, any "reasonable" tree seems to give more or less the same answer. 

2. I *randomized* branch lengths for the input tree, thereby keeping the total tree length and topology but randomly moving the branch lengths around. **The rates were still the same.**

3. I told LEISR to use *random equilibrium frequencies* rather than observed frequencies. **The rates were still the same.** (sensing a theme?)

4. I *randomized the actual amino acids* by creating, for each alignment, a new alignment with original amino acids randomly (but consistently) recoded as another amino acid. For example, I changed all `A`'s to `H`'s, all `H`'s to `S`, and the like. **The rates were still the same.** Now, this result wasn't *as* surprising, since this is sort of what Jukes-Cantor is doing; if all amino acids have the same exchangability in JC, and JC gives rates consistent with other protein models, then the *specific identify* of the amino acids shouldn't have a dramatic effect on what we had already observed.

5. I *randomized sequences along the tree*, simply by randomly re-assigning sequences to different tips. This did not change the tree topology in any way, just changed how the sequences are generally related to each other. **The rates were still the same.**

At this point I made the executive decision to trust my original results and conclude that, even though some models show very strong and clear (and following expected patterns!) model preferences, the *empirical difference among parameters of interest was minimal at best*.


The main exception to this overarching trend came from JC-inferred rates (note, this is in the paper itself, but bears repeating since it's my favorite part). Albeit fairly rarely, JC identified certain sites as evolving more quickly than average, while all other models found these sites were evolving more slowly than average. It turns out that, when sites toggle back-and-forth among amino acids with high model exchangeabilities (i.e. I/L/V!), the associated rate is lower than expected - this is because much of the information that says "we're evolving fast!" is largely taken up by the *phenomenological rate matrix parameter*, and the $$s_i$$ parameter can't get at that information. In JC, where there is no *a priori* information about amino acid exchangebailities, the $$s_i$$ gets to absorb all that variation and ends up with a high value. I would argue that this high value is in fact more appropriate - quickly changing among similar amino acids is still quickly changing.

## FAQ

1. **Should I still look for the best fitting model _when measuring protein rates_?**
<br>You can if you really want to, but it probably won't make much of a difference either way. If anything, you might feel a little bit comforted - even if you use a "worse fit" model, odds are you're going to end up in the same place. What you might do, though, is run several models over your data and look for discrepencies, like we did in this paper (see Figures 5-6, for example). If any site jumps out as being radically different across models, this could be a site worth looking into further.
	

2. **What about when I'm making trees? Should I run ProtTest/ModelTest like I'm "supposed to"?**
<br>Frankly, I don't know to what extent the best-fitting model is going to give you the "best" protein tree. But rest assured, I'm looking into this for you as we speak. In general, I am concerned with the overreliance in the field on model selection procedures as they are currently implemented (see [here](http://mbe.oxfordjournals.org/content/32/4/1097), for example), so I really do promise to get back to you on this question.


3. **Are you really saying I should use Jukes Cantor? I've spent years mocking people who use this model. Must I join their ranks?**
<br>In the circumstance of **measuring relative site-specific rates in proteins**, I actually would recommend this, model fit be damned. I can't tell you yet how I feel about this in other phylogenetic modeling contexts. I can tell you, though, that [Claus Wilke's lab group](http://wilkelab.org) might have a few other things to say on this matter in the coming months. Keep your eyes peeled..
	

4. **What do you think is going on here? The models are clearly different from one another, so why are they agreeing so much?**
<br>Yes, the models do differ, and we can see this clearly through model selection procedures. However, all models considered here are in the same general family of *empirically-derived, phenomenological models of amino-acid exchangability*. None of these models consider evolutionary mechanism (after all, proteins themselves don't evolve - nucleotides do), none consider epistatic effects, none consider the possibility that amino acid fitness may vary across sites/lineages, etc. **Personally, I think all models agree because all models are equally wrong.** Sure some are slightly "more right" (I use this term extremely loosely) than others, but fundamentally none is really going to get at the real evolutionary mechanism that needs to be modeled.	

<br><br><br>

{% if page.comments %} 
<div id="disqus_thread"></div>
<script>

/**
*  RECOMMENDED CONFIGURATION VARIABLES: EDIT AND UNCOMMENT THE SECTION BELOW TO INSERT DYNAMIC VALUES FROM YOUR PLATFORM OR CMS.
*  LEARN WHY DEFINING THESE VARIABLES IS IMPORTANT: https://disqus.com/admin/universalcode/#configuration-variables*/
/*
var disqus_config = function () {
this.page.url = {{ page.permalink }};  // Replace PAGE_URL with your page's canonical URL variable
this.page.identifier = PAGE_IDENTIFIER; // Replace PAGE_IDENTIFIER with your page's unique identifier variable
};
*/
(function() { // DON'T EDIT BELOW THIS LINE
var d = document, s = d.createElement('script');
s.src = 'https://EXAMPLE.disqus.com/embed.js';
s.setAttribute('data-timestamp', +new Date());
(d.head || d.body).appendChild(s);
})();
</script>
<noscript>Please enable JavaScript to view the <a href="https://disqus.com/?ref_noscript">comments powered by Disqus.</a></noscript>
{% endif %}