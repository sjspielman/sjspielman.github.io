---
layout: page
title: Posts
permalink: /posts/
---

<br>

<div class="post">
{% assign date_format = site.minima.date_format | default: "%m %-d, %Y" %}
<ul>
  {% for post in site.posts %}
    <li>    
      <a class="post-list" href="{{ post.url }}">{{ post.title }} ({{post.date | date: date_format }})</a>
       {{ post.excerpt }}
    </li>
  {% endfor %}
</ul>
</div>

