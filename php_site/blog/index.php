<!DOCTYPE HTML>
<Title>Second Sight</title>


<?php
session_start();

define('USERNAME', 'admin');
define('PASSWORD', 'password');

$db = new PDO('sqlite:posts.db');

$db->exec("CREATE TABLE IF NOT EXISTS posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT
)");

$db->exec("CREATE TABLE IF NOT EXISTS pages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT
)");

$action = isset($_GET['action']) ? $_GET['action'] : 'view';

$protected_actions = ['add', 'edit', 'delete', 'logout', 'add_page', 'edit_page', 'delete_page'];
$expected_auth_value = md5(USERNAME.PASSWORD);
if (in_array($action, $protected_actions)) {
    if (!isset($_COOKIE['auth']) || $_COOKIE['auth'] !== $expected_auth_value) {
        $action = 'login';
    }
}

switch($action) {
    case 'login':
        if ($_SERVER['REQUEST_METHOD'] == 'POST') {
            $username = isset($_POST['username']) ? $_POST['username'] : '';
            $password = isset($_POST['password']) ? $_POST['password'] : '';
            if ($username === USERNAME && $password === PASSWORD) {
                setcookie('auth', md5(USERNAME.PASSWORD), time() + (86400 * 7), "/"); 
                header("Location: ?action=view");
                exit;
            } else {
                echo "Invalid username or password.";
            }
        }
        ?>
        <h2>Login</h2>
        <form method="post" action="?action=login">
            Username: <input type="text" name="username"><br><br>
            Password: <input type="password" name="password"><br><br>
            <input type="submit" value="Login">
        </form>
        <?php
        break;

    case 'logout':
        setcookie('auth', '', time() - 3600, "/");
        header("Location: ?action=view");
        exit;
        break;

  case 'add':
        if ($_SERVER['REQUEST_METHOD'] == 'POST') {
            $title = isset($_POST['title']) ? $_POST['title'] : '';
            $content = isset($_POST['content']) ? $_POST['content'] : '';
            $created_at = date('Y-m-d H:i:s');

            $stmt = $db->prepare("INSERT INTO posts (title, content, created_at) VALUES (:title, :content, :created_at)");
            $stmt->bindParam(':title', $title);
            $stmt->bindParam(':content', $content);
            $stmt->bindParam(':created_at', $created_at);
            if($stmt->execute()) {
                echo "Post added successfully.";
                echo "<br><a href='?action=view'>View Posts</a>";
            } else {
                echo "Error adding post.";
            }
        } else {
            ?>
            <h2>Add Post</h2>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/dropzone/5.9.3/min/dropzone.min.css" />
<form action="upload.php" class="dropzone" id="my-dropzone"></form>
<script src="https://cdnjs.cloudflare.com/ajax/libs/dropzone/5.9.3/min/dropzone.min.js"></script>

<script>
Dropzone.autoDiscover = false;

var myDropzone = new Dropzone("#my-dropzone", {
    maxFilesize: 300,
    acceptedFiles: 'image/*', 
    init: function() {
        this.on("success", function(file, response) {
            console.log(response);
            navigator.clipboard.writeText("uploads/" + file.name);
            document.getElementById("bodytext").value += "\r\n<a href='uploads/"+file.name+"'>'<img width='500' src='uploads/"+file.name+"' /></a><br>\r\n";
        });
        this.on("error", function(file, response) {
            console.log(response);
            document.getElementById('file-url').value = response.fileUrl;
            var copyText = document.getElementById('file-url').value;
        });
    }
});
</script>
<button id="wrapButtonlink">Link</button><button id="wrapButtonred">Red text</button><button id="wrapButtonblue">Blue text</button><button id="wrapButtongreen">Green text</button>
<button id="wrapButtonh1">H1</button><button id="wrapButtonh2">H2</button><button id="wrapButtonh3">H3</button>
            <form method="post" action="?action=add">
                Title: <input type="text" name="title"><br><br>
                Content:<br>

                <textarea name="content" id="bodytext" rows="10" cols="50" ></textarea><br><br>
                <input type="submit" value="Add Post">
            </form>

            <?php
        }
        break;


    case 'edit':
        $id = isset($_GET['id']) ? intval($_GET['id']) : 0;
        if (!$id) {
            echo "Invalid post ID.";
            break;
        }

        if ($_SERVER['REQUEST_METHOD'] == 'POST') {
            $title = isset($_POST['title']) ? $_POST['title'] : '';
            $content = isset($_POST['content']) ? $_POST['content'] : '';
            $updated_at = date('Y-m-d H:i:s');

            $stmt = $db->prepare("UPDATE posts SET title = :title, content = :content, updated_at = :updated_at WHERE id = :id");
            $stmt->bindParam(':title', $title);
            $stmt->bindParam(':content', $content);
            $stmt->bindParam(':updated_at', $updated_at);
            $stmt->bindParam(':id', $id);
            if($stmt->execute()) {
                echo "Post updated successfully.";
                echo "<br><a href='?action=view'>View Posts</a>";
            } else {
                echo "Error updating post.";
            }
        } else {
            $stmt = $db->prepare("SELECT * FROM posts WHERE id = :id");
            $stmt->bindParam(':id', $id);
            $stmt->execute();
            $post = $stmt->fetch(PDO::FETCH_ASSOC);
            if(!$post) {
                echo "Post not found.";
                break;
            }
            ?>
            <h2>Edit Post</h2>
<button id="wrapButtonlink">Link</button><button id="wrapButtonred">Red text</button><button id="wrapButtonblue">Blue text</button><button id="wrapButtongreen">Green text</button>
<button id="wrapButtonh1">H1</button><button id="wrapButtonh2">H2</button><button id="wrapButtonh3">H3</button>
            <form method="post" action="?action=edit&id=<?php echo $id; ?>">
                Title: <input type="text" name="title" value="<?php echo htmlspecialchars($post['title']); ?>"><br><br>
                Content:<br>
                <textarea id="bodytext" name="content" rows="10" cols="50"><?php echo htmlspecialchars($post['content']); ?></textarea><br><br>
                <input type="submit" value="Update Post">
            </form>
            <?php
        }
        break;

    case 'delete':
        $id = isset($_GET['id']) ? intval($_GET['id']) : 0;
        if (!$id) {
            echo "Invalid post ID.";
            break;
        }

        if (isset($_POST['confirm']) && $_POST['confirm'] == 'yes') {
            $stmt = $db->prepare("DELETE FROM posts WHERE id = :id");
            $stmt->bindParam(':id', $id);
            if($stmt->execute()) {
                echo "Post deleted successfully.";
                echo "<br><a href='?action=view'>View Posts</a>";
            } else {
                echo "Error deleting post.";
            }
        } else {
            ?>
            <h2>Delete Post</h2>
            <p>Are you sure you want to delete this post?</p>
            <form method="post" action="?action=delete&id=<?php echo $id; ?>">
                <input type="hidden" name="confirm" value="yes">
                <input type="submit" value="Yes, delete it">
                <a href="?action=view">No, go back</a>
            </form>
            <?php
        }
        break;

    case 'add_page':
        if ($_SERVER['REQUEST_METHOD'] == 'POST') {
            $title = isset($_POST['title']) ? $_POST['title'] : '';
            $content = isset($_POST['content']) ? $_POST['content'] : '';
            $created_at = date('Y-m-d H:i:s');

            $stmt = $db->prepare("INSERT INTO pages (title, content, created_at) VALUES (:title, :content, :created_at)");
            $stmt->bindParam(':title', $title);
            $stmt->bindParam(':content', $content);
            $stmt->bindParam(':created_at', $created_at);
            if($stmt->execute()) {
                echo "Page added successfully.";
                echo "<br><a href='?action=view_pages'>View Pages</a>";
            } else {
                echo "Error adding page.";
            }
        } else {
            ?>
            <h2>Add Page</h2>
<button id="wrapButtonlink">Link</button><button id="wrapButtonred">Red text</button><button id="wrapButtonblue">Blue text</button><button id="wrapButtongreen">Green text</button>
<button id="wrapButtonh1">H1</button><button id="wrapButtonh2">H2</button><button id="wrapButtonh3">H3</button>
            <form method="post" action="?action=add_page">
                Title: <input type="text" name="title"><br><br>
                Content:<br>
                <textarea id="bodytext" name="content" rows="10" cols="50"></textarea><br><br>
                <input type="submit" value="Add Page">
            </form>
            <?php
        }
        break;

    case 'edit_page':
        $id = isset($_GET['id']) ? intval($_GET['id']) : 0;
        if (!$id) {
            echo "Invalid page ID.";
            break;
        }

        if ($_SERVER['REQUEST_METHOD'] == 'POST') {
            $title = isset($_POST['title']) ? $_POST['title'] : '';
            $content = isset($_POST['content']) ? $_POST['content'] : '';
            $updated_at = date('Y-m-d H:i:s');

            $stmt = $db->prepare("UPDATE pages SET title = :title, content = :content, updated_at = :updated_at WHERE id = :id");
            $stmt->bindParam(':title', $title);
            $stmt->bindParam(':content', $content);
            $stmt->bindParam(':updated_at', $updated_at);
            $stmt->bindParam(':id', $id);
            if($stmt->execute()) {
                echo "Page updated successfully.";
                echo "<br><a href='?action=view_pages'>View Pages</a>";
            } else {
                echo "Error updating page.";
            }
        } else {
            $stmt = $db->prepare("SELECT * FROM pages WHERE id = :id");
            $stmt->bindParam(':id', $id);
            $stmt->execute();
            $page = $stmt->fetch(PDO::FETCH_ASSOC);
            if(!$page) {
                echo "Page not found.";
                break;
            }
            ?>
            <h2>Edit Page</h2>
<button id="wrapButtonlink">Link</button><button id="wrapButtonred">Red text</button><button id="wrapButtonblue">Blue text</button><button id="wrapButtongreen">Green text</button>
<button id="wrapButtonh1">H1</button><button id="wrapButtonh2">H2</button><button id="wrapButtonh3">H3</button>
            <form method="post" action="?action=edit_page&id=<?php echo $id; ?>">
                Title: <input type="text" name="title" value="<?php echo htmlspecialchars($page['title']); ?>"><br><br>
                Content:<br>
                <textarea id="bodytext" name="content" rows="10" cols="50"><?php echo htmlspecialchars($page['content']); ?></textarea><br><br>
                <input type="submit" value="Update Page">
            </form>
            <?php
        }
        break;

    case 'delete_page':
        $id = isset($_GET['id']) ? intval($_GET['id']) : 0;
        if (!$id) {
            echo "Invalid page ID.";
            break;
        }

        if (isset($_POST['confirm']) && $_POST['confirm'] == 'yes') {
            $stmt = $db->prepare("DELETE FROM pages WHERE id = :id");
            $stmt->bindParam(':id', $id);
            if($stmt->execute()) {
                echo "Page deleted successfully.";
                echo "<br><a href='?action=view_pages'>View Pages</a>";
            } else {
                echo "Error deleting page.";
            }
        } else {
            ?>
            <h2>Delete Page</h2>
            <p>Are you sure you want to delete this page?</p>
            <form method="post" action="?action=delete_page&id=<?php echo $id; ?>">
                <input type="hidden" name="confirm" value="yes">
                <input type="submit" value="Yes, delete it">
                <a href="?action=view_pages">No, go back</a>
            </form>
            <?php
        }
        break;

case 'view_post':
        $id = isset($_GET['id']) ? intval($_GET['id']) : 0;
        if (!$id) {
            echo "Invalid page ID.";
            break;
        }

        $stmt = $db->prepare("SELECT * FROM posts WHERE id = :id");
            $stmt->bindParam(':id', $id);
            $stmt->execute();
            $post = $stmt->fetch(PDO::FETCH_ASSOC);
            if(!$post) {
                echo "Post not found.";
                break;
            }
        ?>
        <a href="/blog">Home</a>
        <h2><?php echo htmlspecialchars($post['title']); ?></h2>
        <p><?php echo $post['content']; ?></p>
        <?php
        break;

    case 'view_page':
        $id = isset($_GET['id']) ? intval($_GET['id']) : 0;
        if (!$id) {
            echo "Invalid page ID.";
            break;
        }

        $stmt = $db->prepare("SELECT * FROM pages WHERE id = :id");
        $stmt->bindParam(':id', $id);
        $stmt->execute();
        $page = $stmt->fetch(PDO::FETCH_ASSOC);
        if(!$page) {
            echo "Page not found.";
            break;
        }
        ?>
        <a href="/blog">Home</a>
        <h2><?php echo htmlspecialchars($page['title']); ?></h2>
        <p><?php echo $page['content']; ?></p>
        <?php
        break;

    case 'view_pages':
        $stmt = $db->query("SELECT * FROM pages ORDER BY created_at DESC");
        $pages = $stmt->fetchAll(PDO::FETCH_ASSOC);
        ?>
        <a href="/blog">Home</a>
        <h2>Pages</h2>
        <?php if (isset($_COOKIE['auth']) && $_COOKIE['auth'] === $expected_auth_value): ?>
            <a href="?action=add_page">Add New Page</a> | 
            <a href="?action=logout">Logout</a>
        <?php else: ?>
            <a href="?action=login">Login</a>
        <?php endif; ?>
        <ul>
            <?php foreach ($pages as $page): ?>
                <li>
                    <a href="?action=view_page&id=<?php echo $page['id']; ?>"><?php echo htmlspecialchars($page['title']); ?></a>
                    <?php if (isset($_COOKIE['auth']) && $_COOKIE['auth'] === $expected_auth_value): ?>
                        - <a href="?action=edit_page&id=<?php echo $page['id']; ?>">Edit</a>
                        | <a href="?action=delete_page&id=<?php echo $page['id']; ?>">Delete</a>
                    <?php endif; ?>
                </li>
            <?php endforeach; ?>
        </ul>
        <?php
        break;

    case 'view':
    default:
        $page_num = isset($_GET['page']) ? intval($_GET['page']) : 1;
        if ($page_num < 1) $page_num = 1;
        $posts_per_page = 4;
        $offset = ($page_num - 1) * $posts_per_page;

        $stmt = $db->query("SELECT COUNT(*) as total FROM posts");
        $total_posts = $stmt->fetch(PDO::FETCH_ASSOC)['total'];
        $total_pages = ceil($total_posts / $posts_per_page);

        $stmt = $db->prepare("SELECT * FROM posts ORDER BY created_at DESC LIMIT :limit OFFSET :offset");
        $stmt->bindValue(':limit', $posts_per_page, PDO::PARAM_INT);
        $stmt->bindValue(':offset', $offset, PDO::PARAM_INT);
        $stmt->execute();
        $posts = $stmt->fetchAll(PDO::FETCH_ASSOC);

        $stmt = $db->query("SELECT id, title FROM pages ORDER BY title ASC");
        $pages = $stmt->fetchAll(PDO::FETCH_ASSOC);

        ?>
     <a href="/">Home</a>    
    <h2>Blog Posts</h2>
        <?php if (isset($_COOKIE['auth']) && $_COOKIE['auth'] === $expected_auth_value): ?>
            <a href="/blog">Home</a> |
            <a href="?action=add">Add New Post</a> | 
            <a href="?action=view_pages">Manage Pages</a> | 
            <a href="?action=logout">Logout</a>
        <?php else: ?>
            <a href="?action=login">Login</a>
        <?php endif; ?>
        <hr>

                <?php if (isset($_COOKIE['auth']) && $_COOKIE['auth'] === $expected_auth_value): ?>
                    
                <?php endif; ?>
            </tr>
        <?php
       foreach ($posts as $post) {
            echo '<div class="post">';
            echo '<h2><a href=?action=view_post&id='.$post['id'].'><div style="color:red;">' . $post['title'] . '</div></a></h2>';
            echo '<a href=?action=view_post&id='.$post['id'].'><div style="color:brown;">' . $post['created_at'] . '</div></a>';
            echo $post['content'];
            echo '</div>';
            if (isset($_COOKIE['auth']) && $_COOKIE['auth'] === $expected_auth_value) {
                echo "
                    <a href='?action=edit&id=".$post['id']."'>Edit</a> | 
                    <a href='?action=delete&id=".$post['id']."'>Delete</a>
                    ";
            }
echo '<hr>';
        }

        echo "<div style='margin-top: 20px;'>";
        if ($page_num > 1) {
            echo '<a href="?action=view&page=1">First</a> ';
            echo '<a href="?action=view&page='.($page_num - 1).'">Previous</a> ';
        }

        for ($i = 1; $i <= $total_pages; $i++) {
            if ($i == $page_num) {
                echo '<strong>'.$i.'</strong> ';
            } else {
                echo '<a href="?action=view&page='.$i.'">'.$i.'</a> ';
            }
        }

        if ($page_num < $total_pages) {
            echo '<a href="?action=view&page='.($page_num + 1).'">Next</a> ';
            echo '<a href="?action=view&page='.$total_pages.'">Last</a> ';
        }
        echo "</div>";

        break;
}
?>

<script>
document.addEventListener('DOMContentLoaded', function() {
    var textarea = document.getElementById('bodytext');
    var button = document.getElementById('wrapButtonlink');

    button.addEventListener('click', function() {
        var start = textarea.selectionStart;
        var end = textarea.selectionEnd;

        var selectedText = textarea.value.substring(start, end);

        var beforeText = '<a href="';
        var afterText = '>Text link here</a>';

        var newText = beforeText + selectedText + afterText;

        textarea.value = textarea.value.substring(0, start) + newText + textarea.value.substring(end);

        var cursorPosition = start + newText.length;
        textarea.selectionStart = textarea.selectionEnd = cursorPosition;

        textarea.focus();
    });
});
</script>

<script>
document.addEventListener('DOMContentLoaded', function() {
    var textarea = document.getElementById('bodytext');
    var button = document.getElementById('wrapButtonred');

    button.addEventListener('click', function() {
        var start = textarea.selectionStart;
        var end = textarea.selectionEnd;

        var selectedText = textarea.value.substring(start, end);

        var beforeText = '<p style="color:red;">';
        var afterText = '</p>';

        var newText = beforeText + selectedText + afterText;

        textarea.value = textarea.value.substring(0, start) + newText + textarea.value.substring(end);

        var cursorPosition = start + newText.length;
        textarea.selectionStart = textarea.selectionEnd = cursorPosition;

        textarea.focus();
    });
});
</script>

<script>
document.addEventListener('DOMContentLoaded', function() {
    var textarea = document.getElementById('bodytext');
    var button = document.getElementById('wrapButtonblue');

    button.addEventListener('click', function() {
        var start = textarea.selectionStart;
        var end = textarea.selectionEnd;

        var selectedText = textarea.value.substring(start, end);

        var beforeText = '<p style="color:#0070ff;">';
        var afterText = '</p>';

        var newText = beforeText + selectedText + afterText;

        textarea.value = textarea.value.substring(0, start) + newText + textarea.value.substring(end);

        var cursorPosition = start + newText.length;
        textarea.selectionStart = textarea.selectionEnd = cursorPosition;

        textarea.focus();
    });
});
</script>

<script>
document.addEventListener('DOMContentLoaded', function() {
    var textarea = document.getElementById('bodytext');
    var button = document.getElementById('wrapButtongreen');

    button.addEventListener('click', function() {
        var start = textarea.selectionStart;
        var end = textarea.selectionEnd;

        var selectedText = textarea.value.substring(start, end);

        var beforeText = '<p style="color:#00c711;">';
        var afterText = '</p>';

        var newText = beforeText + selectedText + afterText;

        textarea.value = textarea.value.substring(0, start) + newText + textarea.value.substring(end);

        var cursorPosition = start + newText.length;
        textarea.selectionStart = textarea.selectionEnd = cursorPosition;

        textarea.focus();
    });
});
</script>

<script>
document.addEventListener('DOMContentLoaded', function() {
    var textarea = document.getElementById('bodytext');
    var button = document.getElementById('wrapButtonh1');

    button.addEventListener('click', function() {
        var start = textarea.selectionStart;
        var end = textarea.selectionEnd;

        var selectedText = textarea.value.substring(start, end);

        var beforeText = '<h1>';
        var afterText = '</h1>';

        var newText = beforeText + selectedText + afterText;

        textarea.value = textarea.value.substring(0, start) + newText + textarea.value.substring(end);

        var cursorPosition = start + newText.length;
        textarea.selectionStart = textarea.selectionEnd = cursorPosition;

        textarea.focus();
    });
});
</script>

<script>
document.addEventListener('DOMContentLoaded', function() {
    var textarea = document.getElementById('bodytext');
    var button = document.getElementById('wrapButtonh2');

    button.addEventListener('click', function() {
        var start = textarea.selectionStart;
        var end = textarea.selectionEnd;

        var selectedText = textarea.value.substring(start, end);

        var beforeText = '<h2>';
        var afterText = '</h2>';

        var newText = beforeText + selectedText + afterText;

        textarea.value = textarea.value.substring(0, start) + newText + textarea.value.substring(end);

        var cursorPosition = start + newText.length;
        textarea.selectionStart = textarea.selectionEnd = cursorPosition;

        textarea.focus();
    });
});
</script>

<script>
document.addEventListener('DOMContentLoaded', function() {
    var textarea = document.getElementById('bodytext');
    var button = document.getElementById('wrapButtonh3');

    button.addEventListener('click', function() {
        var start = textarea.selectionStart;
        var end = textarea.selectionEnd;

        var selectedText = textarea.value.substring(start, end);

        var beforeText = '<h3>';
        var afterText = '</h3>';

        var newText = beforeText + selectedText + afterText;

        textarea.value = textarea.value.substring(0, start) + newText + textarea.value.substring(end);

        var cursorPosition = start + newText.length;
        textarea.selectionStart = textarea.selectionEnd = cursorPosition;

        textarea.focus();
    });
});
</script>
