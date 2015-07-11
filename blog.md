---
layout: post
title:  "News and Posts"
permalink: /blog/
---
<br><br>

<ul class="posts-list">
  {% for post in site.posts %}
    <li>
      <a class="post-title" href="{{ post.url }}">{{ post.title }}</a>
      <div class="post-excerpt" {{ post.excerpt }} </div>
    </li>
    <br><br>
  {% endfor %}
</ul>
