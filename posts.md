---
layout: page
title: Posts
permalink: /posts/
---

<br>

This page contains my impressively-barebones blog, which one day will perhaps take off.

<ul class="listing">
{% for post in site.posts %}
 <li>
    {% assign date_format = site.minima.date_format | default: "%b %-d, %Y" %}
     <span class="post-meta">{{ post.date | date: date_format }}</span>
     <a class="post-link" href="{{ post.url | relative_url }}"> {{ post.date | date: date_format }}:  {{ post.title | escape }} </a> 
  </li>
{% endfor %}
</ul>
