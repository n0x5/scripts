<?php
// BASIC CRUD BLOG STARTING SCRIPT
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

$action = isset($_GET['action']) ? $_GET['action'] : 'view';

$protected_actions = ['add', 'edit', 'delete', 'logout'];
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
            <form method="post" action="?action=add">
                Title: <input type="text" name="title"><br><br>
                Content:<br>
                <textarea name="content" rows="10" cols="50"></textarea><br><br>
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
            <form method="post" action="?action=edit&id=<?php echo $id; ?>">
                Title: <input type="text" name="title" value="<?php echo htmlspecialchars($post['title']); ?>"><br><br>
                Content:<br>
                <textarea name="content" rows="10" cols="50"><?php echo htmlspecialchars($post['content']); ?></textarea><br><br>
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

    case 'view':
    default:
        $page = isset($_GET['page']) ? intval($_GET['page']) : 1;
        if ($page < 1) $page = 1;
        $posts_per_page = 10;
        $offset = ($page - 1) * $posts_per_page;

        $stmt = $db->query("SELECT COUNT(*) as total FROM posts");
        $total_posts = $stmt->fetch(PDO::FETCH_ASSOC)['total'];
        $total_pages = ceil($total_posts / $posts_per_page);

        $stmt = $db->prepare("SELECT * FROM posts ORDER BY created_at DESC LIMIT :limit OFFSET :offset");
        $stmt->bindValue(':limit', $posts_per_page, PDO::PARAM_INT);
        $stmt->bindValue(':offset', $offset, PDO::PARAM_INT);
        $stmt->execute();
        $posts = $stmt->fetchAll(PDO::FETCH_ASSOC);

        ?>
        <h2>Posts</h2>
        <?php if (isset($_COOKIE['auth']) && $_COOKIE['auth'] === $expected_auth_value): ?>
            <a href="?action=add">Add New Post</a> | 
            <a href="?action=logout">Logout</a>
        <?php else: ?>
            <a href="?action=login">Login</a>
        <?php endif; ?>
        <table border="1" cellpadding="5" cellspacing="0">
            <tr>
                <th>ID</th><th>Title</th><th>Content</th><th>Created At</th><th>Updated At</th>
                <?php if (isset($_COOKIE['auth']) && $_COOKIE['auth'] === $expected_auth_value): ?>
                    <th>Actions</th>
                <?php endif; ?>
            </tr>
        <?php
        foreach ($posts as $post) {
            echo "<tr>";
            echo "<td>".htmlspecialchars($post['id'])."</td>";
            echo "<td>".htmlspecialchars($post['title'])."</td>";
            echo "<td>".nl2br(htmlspecialchars($post['content']))."</td>";
            echo "<td>".htmlspecialchars($post['created_at'])."</td>";
            echo "<td>".htmlspecialchars($post['updated_at'])."</td>";
            if (isset($_COOKIE['auth']) && $_COOKIE['auth'] === $expected_auth_value) {
                echo "<td>
                    <a href='?action=edit&id=".$post['id']."'>Edit</a> | 
                    <a href='?action=delete&id=".$post['id']."'>Delete</a>
                    </td>";
            }
            echo "</tr>";
        }
        echo "</table>";

        echo "<div style='margin-top: 20px;'>";
        if ($page > 1) {
            echo '<a href="?action=view&page=1">First</a> ';
            echo '<a href="?action=view&page='.($page - 1).'">Previous</a> ';
        }

        for ($i = 1; $i <= $total_pages; $i++) {
            if ($i == $page) {
                echo '<strong>'.$i.'</strong> ';
            } else {
                echo '<a href="?action=view&page='.$i.'">'.$i.'</a> ';
            }
        }

        if ($page < $total_pages) {
            echo '<a href="?action=view&page='.($page + 1).'">Next</a> ';
            echo '<a href="?action=view&page='.$total_pages.'">Last</a> ';
        }
        echo "</div>";

        break;
}
?>
