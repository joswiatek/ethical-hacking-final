<?php
    session_start();
    if(!isset($_COOKIE['login_cookie'])) {
        header('Location: login.php');
        die();
    }
?>
