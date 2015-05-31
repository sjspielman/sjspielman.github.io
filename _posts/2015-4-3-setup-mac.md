---
layout: post
title: Configuring Yosemite for Biocomputing
date:   2015-4-3
permalink: /configure_yosemite_biocomputing/
---

I recently got myself the new 2015 Macbook Pro, and so far it's been great - especially considering that my old laptop's battery only held a charge for a whopping 2.5 hours. Now, 4 hours since the last charge, I still have 8 hours of battery life remaining. The world is my oyster!

In any case, the first thing I did with the new computer was set up my biocomputing environment, and in my at-long-last-achieved-wisdom, I saved all the steps I took to get my computer up-and-running, and here it is! Bear in mind that these are the steps that I took, and they may or may not work for you.


<br><br>

### Step-by-step guide to a configuring a Biocomputing environment
<br>

**1.** Download XCode from the App Store. This will give you the basics you need to proceed, like clang/clang++ compilers, git, and other goodies. However, note that XCode won't give you a fortran compiler. The quickest option for getting one is to download and install from this link: [http://r.research.att.com/libs/gfortran-4.8.2-darwin13.tar.bz2](http://r.research.att.com/libs/gfortran-4.8.2-darwin13.tar.bz2).

<br>
**2.** XCode comes with it's own text editor, although I am partial to TextWrangler (available here: [http://www.barebones.com/products/textwrangler/download.html](http://www.barebones.com/products/textwrangler/download.html)), which I installed next.

<br>
**3.** Set up the global configurations for git by typing the following lines into terminal:

{% highlight bash %}
git config --global user.name "first last"
git config --global user.email "email"
{% endhighlight %}


where "first last" are replaced with your first and last name ("Stephanie Spielman" for me), and the "email" is replaced with your email.

<br>
**4.** Install Homebrew, a convenient and comprehensive Mac package manager. Personally, I do prefer homebrew over MacPorts or other package managers, although I have no real basis for this preference. If MacPorts or other is your thing, then the next few steps might not be so helpful.
<br>To get homebrew, enter this code into the command line:

{% highlight bash %}
ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
{% endhighlight %}

Note that you might need to "sudo" that command. Also, if you ever want to update your homebrew, use this command:

{% highlight bash %}
brew update
{% endhighlight %}


<br>
**5.** While Mac does come with its own python distribution, this distribution tends to get wonky when dealing with python modules. In the past, I've had some really annoyances trying to get numpy and scipy running properly, so I abandoned Mac's python in favor of homebrew's.
So, once homebrew is installed (it will be in "/usr/local/Cellar/"), use it to download their python version. To make sure that, when using the python interpretter, that you can freely press the up/down/left/right arrows without annoying characters appearing, install readline first!:
{% highlight bash %}
brew install readline --universal
brew install python
{% endhighlight %}
By default, this will give you python-2.7. If you want python3, use this command instead:
{% highlight bash %}
brew install python3
{% endhighlight %}


<br>
**6.** Next, just to make sure that Mac's python doesn't interfere with homebrew's, enter these commands:

{% highlight bash %}
cd /System/Library/Frameworks/Python.framework/Versions
sudo rm Current
# Note that the "2.7.9" below will need to be replaced if its not the version on your system!
sudo ln -s /usr/local/Cellar/python/2.7.9/Frameworks/Python.framework/Versions/Current 
{% endhighlight %}

<br>
**7.** Homebrew's python comes with pip, which you can use to download various libraries. Here's what I did:

{% highlight bash %}
pip install numpy
pip install scipy
pip install "ipython[notebook]" # install iPython and notebook
pip install ipython --upgrade   # the above command does not seem to install most recent iPython, so this line fixes that issue
pip install pandas
{% endhighlight %}


<br>
**8.** Unfortunately, you can't get Biopython with pip, so you have to download from source. You can get Biopython from this website: [http://biopython.org/wiki/Download](http://biopython.org/wiki/Download). Download either biopython-1.65.zip or biopython-1.65.tar.gz, uncompress, and navigate to the directory. Once in the biopython directory, enter the following in terminal to install Biopython:

{% highlight bash %}
python setup.py build
sudo python setup.py install
{% endhighlight %}

<br>
**9.** Pandoc, a package for converting file formats (often from markdown or ipython notebook to html or pdf, etc.), is an especially useful thing to have around. Download from the website: [https://github.com/jgm/pandoc/releases](https://github.com/jgm/pandoc/releases).

<br>
**10.** If you want to convert to pdf, though, you'll need LaTeX on your system (surprisingly enough, if you want to use LaTeX for anything else, you'll still need LaTeX!). For this, you have to download MacTex (from this website: [https://tug.org/mactex/downloading.html](https://tug.org/mactex/downloading.html)). This will give you a convenient installer which guides you through the process. The package is super big though (2.4 GB), so if you internet is not lightning-speed, this might be a good time for a coffee break!

<br>
**11.** Next, we'll get R up and running. This is pretty straightforward - just download the R package installer (the one for Mavericks!) from this website: [http://www.r-project.org](http://www.r-project.org). I recommend against building from source, since this requires a fortran compiler, and as previously mentioned, you'll have to get this running on your own - this link should do it: [http://r.research.att.com/libs/gfortran-4.8.2-darwin13.tar.bz2]([http://r.research.att.com/libs/gfortran-4.8.2-darwin13.tar.bz2]). 

<br>
**12.** Download, if you want, RStudio from this website: [http://www.rstudio.com](http://www.rstudio.com). You'll also need XQuartz, which you can download from this website: [http://xquartz.macosforge.org/landing/](http://xquartz.macosforge.org/landing/)

<br>
**13.** Once R is running, you can install any packages you'll need. I ran the following commands in R for installation:


{% highlight R %}
install.packages("dplyr", dep=T)
install.packages("tidyr", dep=T)
install.packages("ggplot2", dep=T)
install.packages("ape", dep=T) # for phylogeny manipulation
install.packages("lme4", dep=T) # for more linear modeling
install.packages("multcomp", dep=T) # for multiple comparisons in modeling
{% endhighlight %}

<br>
And now, for the most part, you have a functioning biocomputing environment for git, Python, and R! 















