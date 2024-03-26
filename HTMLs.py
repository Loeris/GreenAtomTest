html_start = """<!DOCTYPE html>
<html>
<head>
  <title>Counting</title>
  <style>
    /* CSS styles for centering the button */
    body {
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
    }

    button {
      font-size: 24px;
      padding: 10px 20px;
    }
  </style>
</head>
<body>

  <!-- Button element -->
  <button onclick="window.location.href='/'">End</button>

</body>
</html>"""

html_root = """<!DOCTYPE html>
<html>
<head>
  <title>Start Page</title>
  <style>
    /* CSS styles for centering and sizing */
    body {
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
    }

    label, input, button {
      font-size: 24px;
      padding: 10px 20px;
    }
  </style>
</head>
<body>

  <!-- Input field -->
  <label for="numberInput">Enter a number:</label>
  <input type="number" id="numberInput">

  <!-- Button element -->
  <button onclick="redirectToStartPage()">Start</button>

  <script>
    function redirectToStartPage() {
      const number = document.getElementById("numberInput").value;
      window.location.href = `start?begin=${number}`;
    }
  </script>

</body>
</html>"""