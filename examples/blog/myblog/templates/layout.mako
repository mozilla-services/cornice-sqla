#-*- coding: utf-8 -*-
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>My Blog</title>
    <link rel="shortcut icon" href="/assets/favicon.ico">
    <link rel="stylesheet" href="/assets/bootstrap.min.css">
    <link rel="stylesheet" href="/assets/myblog.css">
    <script src="/assets/jquery.js" type="text/javascript"></script>
    <script src="/assets/json2.js" type="text/javascript"></script>
  </head>

  <body>
    <div class="topbar">
      <div class="fill">
        <div class="container">
          <a class="brand" href="#">My Blog</a>
          <ul class="nav">
            <li class="active"><a href="#">Home</a></li>
            <li><a href="#about">About</a></li>
            <li><a href="#contact">Contact</a></li>
          </ul>
        </div>
      </div>
    </div>

    <div class="container">
      ${next.body()}
    </div>

  </body>
</html>
