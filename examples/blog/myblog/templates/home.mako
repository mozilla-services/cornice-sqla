# -*- coding: utf-8 -*-
<%inherit file="layout.mako"/>

<div class="row">
 <div class="entries">
 </div>

 <h4>People that have contributed to this blog</h4>
 <div class="users">
 </div>

 <script>
 function update() {
 $.getJSON("/users", function(data) {
  var users = data.items;
  $(".users").html('');
  var elm = "<ul>";

  for(var x=0; x < users.length; x++) {
    var user = users[x];
    elm += "<li>" + user.name + "</li>";
   }

   elm += "<ul>";

   $(".users").prepend(elm);

 });

 $.getJSON("/blog", function(data) {
  $(".entries").html('');
  var entries = data.items;

  for(var x=0; x < entries.length; x++) {
    var entry = entries[x];
    var elm = "<h3>" + entry.subject + "</h3>";
    elm += "<p>" + entry.content + "</p>";
    $(".entries").prepend(elm);
  }
 });
 };
 update();
 </script>
 <button onclick="javascript:update();"
            class="btn primary large right">Update</button>
</div>
