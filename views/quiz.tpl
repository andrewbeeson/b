<!doctype html>
<html lang="en">
  <head>
    <link 
      href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css" 
      rel="stylesheet" 
      integrity="sha384-rbsA2VBKQhggwzxH7pPCaAqO46MgnOM80zW1RWuH61DGLwZJEdK2Kadq2F9CUG65" 
      crossorigin="anonymous"
    >
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
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
   
    <title>Maths Quiz</title>
  </head>

  <body>
  <div class=="container">
    <div class=="row">
<h1 class=="heading">{{quiz.name}}</h1>
<p>
    <span>{{question.topic}}</span>
    <span>{{question.number}}</span>
</p>
    </div>
    <div class=="row">
        <p>{{question.text}}</p>
    </div>
    <div class=="row">
        <form>
            <textarea id="AnsInput"Name="Answer" rows="{{question.answerrows}}"/>
            <button name="submit" type="submit">submit</button>
        </form>
    </div>
    <div class=="row">
        <textbox parameter="if you have any questions for your teacher, please enter them here" name="teacherquestion" rows="3"/>
    </div>
  </div>

  </body>
</html>