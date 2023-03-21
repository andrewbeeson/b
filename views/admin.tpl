<!doctype html>
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <!-- Bootstrap CSS -->
    <link rel="stylesheet" 
			href="https://cdn.jsdelivr.net/npm/bootstrap@4.0.0/dist/css/bootstrap.min.css" 
			integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" 
			crossorigin="anonymous"
		>

    <title>Administration&nbsp;&mdash;&nbsp;{{config['app.name']}}</title>
  </head>
  <body>
    <div class="container-fluid pt=3">
      <div class="header">
        <h1>User Administration</h1>
        <p>{{selection}}</p>
      </div>
      <form class="row">
        <div class="col-md-4 align-middle m-2">
          <input id="id" name="id" placeholder="User identifier" type="number" value="{{parameters['id']}}"/>
        </div>    
    
        <div class="col-md-4 align-middle m-2">
          <input id="name" name="name" placeholder="User name" type="text" value="{{parameters['name']}}"/>
        </div>    
    
        <div class="col-md-1 align-middle m-2">
          <select id="active" name="active">
            <option value="">Any</option>
            <option value="1" {{'selected' if parameters['active'] == 1 else ''}}>Active</option>
            <option value="0" {{'selected' if parameters['active'] == 0 else ''}}>Inactive</option>
          </select>
        </div>    
    
        <div class="col-md-1 align-middle m-2">
          <select id="admin" name="admin">
            <option value="">Any type</option>
            <option value="1" {{'selected' if parameters['useradmin'] == 1 else ''}}>Administrator</option>
            <option value="0" {{'selected' if parameters['useradmin'] == 0 else ''}}>User</option>
          </select>
        </div>
      
        <div class="col-md-1 align-middle m-2">
          <button class="btn " id="search" type="submit">Search</button>
        </div>    
      </form>
      <div class="row">
<% if resultset['rowcount'] == 0: %>
        <p>No records found</p>
<% else: %>
        <table class="table table-striped">
          <tr>
            <th>Id</th>
            <th>Name</th>
            <th>Active</th>
            <th>Administrator</th>
          </tr>
  <% for row in resultset['rows']: %>
          <tr>
            <td>{{row['id']}}</td>
            <td>{{row['username']}}</td>
            <td>{{'Yes' if row['active'] == 1 else 'No' if row['active'] == 0 else ''}}</td>
            <td>{{'Administrator' if row['useradmin'] == 1 else 'Player' if row['useradmin'] == 0 else ''}}</td>
          </tr>
  <% end %>
        </table>
<% end %>
      </div>
    </div>
    
    <!-- Optional JavaScript -->
    <!-- jQuery first, then Popper.js, then Bootstrap JS -->
    <script 
      src="https://code.jquery.com/jquery-3.2.1.slim.min.js" 
			integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" 
			crossorigin="anonymous">
		</script>
    <script 
			src="https://cdn.jsdelivr.net/npm/popper.js@1.12.9/dist/umd/popper.min.js" 
			integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" 
			crossorigin="anonymous">
		</script>
    <script 
			src="https://cdn.jsdelivr.net/npm/bootstrap@4.0.0/dist/js/bootstrap.min.js" 
			integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" 
			crossorigin="anonymous">
		</script>
  </body>
</html>