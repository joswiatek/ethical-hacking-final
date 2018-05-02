<style type='text/css'>
@import url('style.css');
</style>
<?php
    session_start();
    if(isset($_COOKIE['login_cookie'])) {
        header('Location: index.php');
    }
    $user = $_REQUEST['username'];
    $pass = $_REQUEST['password'];
    if($user == 'admin' && $pass == 'password') {
        setcookie('login_cookie', '1234');
        header('Location: index.php');
    }
?>

<div id="main">
    <div id="box">
        <div id="login">
            <h2>Login to Vulnerable Application</h2>
            <form action="" method="post">
                <table>
                    <tr>
                        <td>
                            <label for="username">Username</label>
                        </td>
                        <td>
                            <input type="text" name="username" id="username" />
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <label for="password">Password</label>
                        </td>
                        <td>
                            <input type="password" name="password" id="password" />
                        </td>
                    </tr>
                    <tr>
                        <td colspan=2>
                            <input type="submit" value="Login" />
                        </td>
                    </tr>
                </table>
            </form>
        </div>
    </div>
</div>
