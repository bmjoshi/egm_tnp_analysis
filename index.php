<html>
<head>
<title><?php echo getcwd(); ?></title>

<style type='text/css'>

body {
    font-family: Consolas,Menlo,"courier new",monospace;
    font-size: 9pt;
    line-height: 10.5pt;
}

div.header_bar {
  height: 48px;
  vertical-align: middle;
  white-space: nowrap;
  -moz-box-align: center;
  align-items: center;
  display: -webkit-box;
  display: -moz-box;
  display: -ms-flexbox;
  display: -webkit-flex;
  display: flex;
  -moz-user-select: -moz-none;
  box-shadow: 0 2px 4px 0 rgba(0,0,0,.1);
}

div.header {
    font-family: 'Google Sans', 'Google Sans Text', Roboto, sans-serif;
    padding: 20px;
    text-align: center;
    background: white;
    color: black;
    font-size: 20px;
    box-shadow: 0 2px 4px 0 rgba(0,0,0,.1);
}

div.pic h3 { 
    font-size: 11pt;
    margin: 0.5em 1em 0.2em 1em;
}
div.pic p {
    font-size: 11pt;
    margin: 0.2em 1em 0.1em 1em;
}
div.pic {
    display: block;
    float: left;
    background-color: white;
    border: 1px solid #ccc;
    padding: 2px;
    text-align: center;
    margin: 2px 10px 10px 2px;
    -moz-box-shadow: 7px 5px 5px rgb(80,80,80);    /* Firefox 3.5 */
    -webkit-box-shadow: 7px 5px 5px rgb(80,80,80); /* Chrome, Safari */
    box-shadow: 7px 5px 5px rgb(80,80,80);         /* New browsers */  
}
a { text-decoration: none; color: rgb(80,0,0); }
a:hover { text-decoration: underline; color: rgb(255,80,80); }
</style>
</head>


<body>
<div clas="header_bar">
<div class="header">
<h1><?php echo "Bhargav Joshi\n" ?></h1>
<h2><a name="plots">Plots</a></h2>
<p><form>Filter: <input type="text" name="match" size="30" value="<?php if (isset($_GET['match'])) print htmlspecialchars($_GET['match']);  ?>" /><input type="Submit" value="Go" /></form></p>
</div>
</div>

<?php
$pwd = getcwd();
print "<h3>Path = $pwd</h3>";
?>

<div>
<?php
$displayed = array();
if ($_GET['noplots']) {
    print "Plots will not be displayed.\n";
} else {
  $other_exts = array('.pdf', '.cxx', '.eps', '.root', '.txt', '.C', '.log');
    $filenames = glob("*.png"); sort($filenames);
    foreach ($filenames as $filename) {
        if (isset($_GET['match']) && !fnmatch('*'.$_GET['match'].'*', $filename)) continue;
        array_push($displayed, $filename);
        print "<div class='pic'>\n";
        print "<h3><a href=\"$filename\">$filename</a></h3>";
        print "<a href=\"$filename\"><img src=\"$filename\" style=\"border: none; width: 300px; \"></a>";
        $others = array();
        foreach ($other_exts as $ex) {
            $other_filename = str_replace('.png', $ex, $filename);
            if (file_exists($other_filename)) {
                array_push($others, "<a class=\"file\" href=\"$other_filename\">[" . $ex . "]</a>");
                if ($ex != '.txt') array_push($displayed, $other_filename);
            }
        }
        if ($others) print "<p>Also as ".implode(', ',$others)."</p>";
        print "</div>";
    }
}
?>
</div>
<div style="display: block; clear:both;">
<h2><a name="files">Other files</a></h2>
<ul>
<?
foreach (glob("*") as $filename) {
    if ($_GET['noplots'] || !in_array($filename, $displayed)) {
        if (isset($_GET['match']) && !fnmatch('*'.$_GET['match'].'*', $filename)) continue;
        if (is_dir($filename)) {
            print "<li>[DIR] <a href=\"$filename\">$filename</a></li>";
        } else {
            print "<li><a href=\"$filename\">$filename</a></li>";
        }
    }
}
?>
</ul>
</div>
</body>
</html>
