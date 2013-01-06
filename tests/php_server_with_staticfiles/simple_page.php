<?php
  $name = 'CherryPy CGI PHP World';
?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
  <title>Simple PHP-Page</title>
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
  <style type="text/css">
    body {
      font-family: sans-serif;
    }
  </style>
</head>
<body>

  <div style="float: right; margin-left: 3em; margin-bottom: 3em;">
    <img src="../php_files/cherrypy.png" alt="CherryPy" />
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
