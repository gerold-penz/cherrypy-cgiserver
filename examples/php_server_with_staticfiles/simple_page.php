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
  <div style="float: right; margin-left: 3em; margin-bottom: 3em;">
    <img src="images/cherrypy.png" alt="CherryPy" />
  </div>

  <h1>Simple PHP-Page</h1>

  <p>Powered by CherryPy</p>

  <p>
    Lorem ipsum dolor sit amet, consectetuer adipiscing elit.
    Aenean commodo ligula eget dolor. Aenean massa.
    Cum sociis natoque penatibus et magnis dis parturient montes, nascetur
    ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu,
    pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo,
    fringilla vel, aliquet nec, vulputate eget, arcu.
  </p>

  <?php for ($i = 0; $i < 4; $i++) { ?>
    <div style="text-align: center">Hello <?php echo $name; ?>!</div>
  <?php } ?>

  <p>
    Lorem ipsum dolor sit amet, consectetuer adipiscing elit.
    Aenean commodo ligula eget dolor. Aenean massa.
    Cum sociis natoque penatibus et magnis dis parturient montes, nascetur
    ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu,
    pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo,
    fringilla vel, aliquet nec, vulputate eget, arcu.
  </p>

  <div style="clear: both"></div>
</body>
</html>
