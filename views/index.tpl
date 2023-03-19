<!doctype html>
<html lang="en">
  <head>
    <link 
      href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css" 
      rel="stylesheet" 
      integrity="sha384-rbsA2VBKQhggwzxH7pPCaAqO46MgnOM80zW1RWuH61DGLwZJEdK2Kadq2F9CUG65" 
      crossorigin="anonymous"
    >
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <script 
      src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/js/bootstrap.bundle.min.js" 
      integrity="sha384-kenU1KFdBIe4zVF0s0G1M5b4hcpxyD9F7jL+jjXkk+Q2h455rYXK/7HAuoJl+0I4" 
      crossorigin="anonymous"
    >
    </script>
    <title>{{config.get('app.name', 'Anon')}}</title>
  </head>

  <body>
    <div class="container">
  <%
    if resultset and resultset.rowcount == 1:
      user = resultset.rows[0]
      admin = user["useradmin"]
      name = user["username"]
    else:
      user = admin = name = None
    end
  %>
  % if user:

    <h1>Hello, {{name.title()}}</h1>

    %   if admin:
    <div class="list-group">
      <a href="/admin/game" class="list-group-item list-group-item-action">Administer Game Records</a>
      <a href="/admin/quiz" class="list-group-item list-group-item-action">Administer Quiz Records</a>
      <a href="/admin/user" class="list-group-item list-group-item-action">Administer User Records</a>
      <a href="/login" class="list-group-item list-group-item-action">Log in, again</a>
    </div>
    %   end

  % else:
    <h1>Hello</h1>
    <ul class="list-group">
      <a href="/login" class="list-group-item list-group-item-action">Log in</a>
      <a href="/register" class="list-group-item list-group-item-action">Register</a>
    </ul>
  % end
    </div>
  </body>
</html>