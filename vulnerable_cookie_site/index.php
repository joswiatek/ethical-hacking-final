<style type='text/css'>
@import url('style.css');
</style>
<?php
    include('login_check.php');
?>
<div id="main">
<div id="box">
<?php
    if($_COOKIE['login_cookie'] == '1234') {
        print('<div id="data"><h3>Vulnerable Data</h3><div id="lorem">Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut et viverra nisl. Quisque eu orci eu quam pharetra viverra quis quis purus. Vivamus vitae neque in mi viverra sollicitudin vitae et odio. Phasellus at sapien vitae purus pellentesque lobortis. Donec dapibus dictum cursus. Praesent luctus vehicula tortor, nec pulvinar purus volutpat vitae. Etiam sollicitudin leo nec velit lobortis, a finibus ante aliquam. Phasellus egestas lorem eu ipsum molestie accumsan. Sed sed ex mauris. Curabitur lorem urna, ultricies a mauris vel, scelerisque commodo ante.</div></div>');
    } else {
        print('<div id="data"><h3>No Dice</h3></div>');
    }
?>
</div>
</div>
