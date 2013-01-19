<?php
  $name = 'CherryPy CGI PHP World';
?>
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Simple PHP-Page</title>
  <style type="text/css">
    body {
      font-family: sans-serif;
    }
  </style>
</head>
<body>
  <h1>Simple PHP-Page</h1>
  <p>Powered by CherryPy</p>
  <?php for ($i = 0; $i < 4; $i++) { ?>
    <div>Hello <?php echo $name; ?>!</div>
  <?php } ?>
</body>
</html>
