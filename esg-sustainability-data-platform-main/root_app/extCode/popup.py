
html_text='''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/css/bootstrap.min.css">
  <script src="https://cdn.jsdelivr.net/npm/jquery@3.6.1/dist/jquery.slim.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.1/dist/umd/popper.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/js/bootstrap.bundle.min.js"></script>
</head>
<body>

<div class="container">
  <!-- Button to Open the model -->
  <button type="button" class="btn btn-primary" data-toggle="model" data-target="#mymodel">
    Open model
  </button>

  <!-- The model -->
  <div class="model" id="mymodel">
    <div class="model-dialog">
      <div class="model-content">
      
        <!-- model Header -->
        <div class="model-header">
          <h4 class="model-title">model Heading</h4>
          <button type="button" class="close" data-dismiss="model">&times;</button>
        </div>
        
        <!-- model body -->
        <div class="model-body">
          model body..
        </div>
        
        <!-- model footer -->
        <div class="model-footer">
          <button type="button" class="btn btn-danger" data-dismiss="model">Close</button>
        </div>
        
      </div>
    </div>
  </div>
  
</div>

</body>
</html>'''