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
    <div class="header">
      <h1>User Administration</h1>
      <p>{{selection}}</p>
    </div>
    <form>
      <div>
        <input id="id" name="id" placeholder="User identifier" Type="number"/>
      </div>    
  
      <div>
        <input id="name" name="name" placeholder="User name" Type="text"/>
      </div>    
  
      <div>
        <label for="active">User active</label>
        <select id="active" name="active">
          <option value="">Choose</option>
          <option value="1">Active</option>
          <option value="0">Inactive</option>
        </select>
      </div>    
  
      <div>
        <label for="admin">User type</label>
        <select id="admin" name="admin">
          <option value="">Choose</option>
          <option value="1">Administrator</option>
          <option value="0">User</option>
        </select>
      </div>    
    </div>

    <div>
      <button id="search" type="submit">Search</button>
    </div>    
  </form>
  <div>
    <p>{{resultset['lastrowid']}}</p>
    <p>{{resultset['lastcount']}}</p>
    <p>{{resultset['rowcount']}}</p>
    <p>{{resultset['rows']}}</p>
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