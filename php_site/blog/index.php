<?php
// Start session
session_start();

// Hardcoded username and password
define('USERNAME', 'admin');
define('PASSWORD', 'password');

// Connect to SQLite database
$db = new PDO('sqlite:posts.db');

// Create posts table if it doesn't exist
$db->exec("CREATE TABLE IF NOT EXISTS posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT
)");

// Create pages table for static pages
$db->exec("CREATE TABLE IF NOT EXISTS pages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT
)");

$action = isset($_GET['action']) ? $_GET['action'] : 'view';

// Authentication check for protected actions
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
                // Set authentication cookie
                setcookie('auth', md5(USERNAME.PASSWORD), time() + (86400 * 7), "/"); // Expires in 7 days
                header("Location: ?action=view");
                exit;
            } else {
                echo "Invalid username or password.";
            }
        }
        // Display login form
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
        // Clear authentication cookie
        setcookie('auth', '', time() - 3600, "/");
        header("Location: ?action=view");
        exit;
        break;

    // Post actions (add, edit, delete)
    case 'add':
        if ($_SERVER['REQUEST_METHOD'] == 'POST') {
            // Sanitize user input
            $title = isset($_POST['title']) ? $_POST['title'] : '';
            $content = isset($_POST['content']) ? $_POST['content'] : '';
            $created_at = date('Y-m-d H:i:s');

            // Prepare and execute insert statement
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
            // Display form
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
            // Process form data
            $title = isset($_POST['title']) ? $_POST['title'] : '';
            $content = isset($_POST['content']) ? $_POST['content'] : '';
            $updated_at = date('Y-m-d H:i:s');

            // Prepare and execute update statement
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
            // Retrieve post data
            $stmt = $db->prepare("SELECT * FROM posts WHERE id = :id");
            $stmt->bindParam(':id', $id);
            $stmt->execute();
            $post = $stmt->fetch(PDO::FETCH_ASSOC);
            if(!$post) {
                echo "Post not found.";
                break;
            }
            // Display form pre-filled with post data
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

        // Optionally confirm deletion
        if (isset($_POST['confirm']) && $_POST['confirm'] == 'yes') {
            // Delete from database
            $stmt = $db->prepare("DELETE FROM posts WHERE id = :id");
            $stmt->bindParam(':id', $id);
            if($stmt->execute()) {
                echo "Post deleted successfully.";
                echo "<br><a href='?action=view'>View Posts</a>";
            } else {
                echo "Error deleting post.";
            }
        } else {
            // Ask for confirmation
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

    // Page actions (add_page, edit_page, delete_page)
    case 'add_page':
        if ($_SERVER['REQUEST_METHOD'] == 'POST') {
            // Sanitize user input
            $title = isset($_POST['title']) ? $_POST['title'] : '';
            $content = isset($_POST['content']) ? $_POST['content'] : '';
            $created_at = date('Y-m-d H:i:s');

            // Prepare and execute insert statement
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
            // Display form
            ?>
            <h2>Add Page</h2>
            <form method="post" action="?action=add_page">
                Title: <input type="text" name="title"><br><br>
                Content:<br>
                <textarea name="content" rows="10" cols="50"></textarea><br><br>
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
            // Process form data
            $title = isset($_POST['title']) ? $_POST['title'] : '';
            $content = isset($_POST['content']) ? $_POST['content'] : '';
            $updated_at = date('Y-m-d H:i:s');

            // Prepare and execute update statement
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
            // Retrieve page data
            $stmt = $db->prepare("SELECT * FROM pages WHERE id = :id");
            $stmt->bindParam(':id', $id);
            $stmt->execute();
            $page = $stmt->fetch(PDO::FETCH_ASSOC);
            if(!$page) {
                echo "Page not found.";
                break;
            }
            // Display form pre-filled with page data
            ?>
            <h2>Edit Page</h2>
            <form method="post" action="?action=edit_page&id=<?php echo $id; ?>">
                Title: <input type="text" name="title" value="<?php echo htmlspecialchars($page['title']); ?>"><br><br>
                Content:<br>
                <textarea name="content" rows="10" cols="50"><?php echo htmlspecialchars($page['content']); ?></textarea><br><br>
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

        // Optionally confirm deletion
        if (isset($_POST['confirm']) && $_POST['confirm'] == 'yes') {
            // Delete from database
            $stmt = $db->prepare("DELETE FROM pages WHERE id = :id");
            $stmt->bindParam(':id', $id);
            if($stmt->execute()) {
                echo "Page deleted successfully.";
                echo "<br><a href='?action=view_pages'>View Pages</a>";
            } else {
                echo "Error deleting page.";
            }
        } else {
            // Ask for confirmation
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

    // View a single page
    case 'view_page':
        $id = isset($_GET['id']) ? intval($_GET['id']) : 0;
        if (!$id) {
            echo "Invalid page ID.";
            break;
        }

        // Retrieve page data
        $stmt = $db->prepare("SELECT * FROM pages WHERE id = :id");
        $stmt->bindParam(':id', $id);
        $stmt->execute();
        $page = $stmt->fetch(PDO::FETCH_ASSOC);
        if(!$page) {
            echo "Page not found.";
            break;
        }
        // Display the page
        ?>
        <h2><?php echo htmlspecialchars($page['title']); ?></h2>
        <p><?php echo nl2br(htmlspecialchars($page['content'])); ?></p>
        <?php
        break;

    // View list of pages
    case 'view_pages':
        // Retrieve all pages
        $stmt = $db->query("SELECT * FROM pages ORDER BY created_at DESC");
        $pages = $stmt->fetchAll(PDO::FETCH_ASSOC);
        ?>
        <a href="/">Home</a>
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

    // View posts (default action)
    case 'view':
    default:
        // Pagination
        $page_num = isset($_GET['page']) ? intval($_GET['page']) : 1;
        if ($page_num < 1) $page_num = 1;
        $posts_per_page = 4;
        $offset = ($page_num - 1) * $posts_per_page;

        // Get total number of posts
        $stmt = $db->query("SELECT COUNT(*) as total FROM posts");
        $total_posts = $stmt->fetch(PDO::FETCH_ASSOC)['total'];
        $total_pages = ceil($total_posts / $posts_per_page);

        // Retrieve posts for current page
        $stmt = $db->prepare("SELECT * FROM posts ORDER BY created_at DESC LIMIT :limit OFFSET :offset");
        $stmt->bindValue(':limit', $posts_per_page, PDO::PARAM_INT);
        $stmt->bindValue(':offset', $offset, PDO::PARAM_INT);
        $stmt->execute();
        $posts = $stmt->fetchAll(PDO::FETCH_ASSOC);

        // Retrieve all pages for navigation
        $stmt = $db->query("SELECT id, title FROM pages ORDER BY title ASC");
        $pages = $stmt->fetchAll(PDO::FETCH_ASSOC);

        ?>
        <h2>Blog Posts</h2>
        <?php if (isset($_COOKIE['auth']) && $_COOKIE['auth'] === $expected_auth_value): ?>
            <a href="/">Home</a> |
            <a href="?action=add">Add New Post</a> | 
            <a href="?action=view_pages">Manage Pages</a> | 
            <a href="?action=logout">Logout</a>
        <?php else: ?>
            <a href="?action=login">Login</a>
        <?php endif; ?>
        <hr>

                <?php if (isset($_COOKIE['auth']) && $_COOKIE['auth'] === $expected_auth_value): ?>
                    <th>Actions</th>
                <?php endif; ?>
            </tr>
        <?php
       foreach ($posts as $post) {
            //echo "<tr>";
            //echo "<td>".htmlspecialchars($post['created_at'])."</td>";
            //echo "<td>".htmlspecialchars($post['id'])."</td>";
            //echo "<td>".htmlspecialchars($post['title'])."</td>";
            //echo "<td>".nl2br(htmlspecialchars($post['content']))."</td>";
            echo '<div class="post">';
            echo '<h2 style="color:red;">' . $post['title'] . '</h2>';
            echo '<div style="color:brown;">' . $post['created_at'] . '</div>';
            echo $post['content'];
            echo '</div>';
            //echo "<td>".htmlspecialchars($post['updated_at'])."</td>";
            if (isset($_COOKIE['auth']) && $_COOKIE['auth'] === $expected_auth_value) {
                echo "
                    <a href='?action=edit&id=".$post['id']."'>Edit</a> | 
                    <a href='?action=delete&id=".$post['id']."'>Delete</a>
                    ";
            }
echo '<hr>';
        }

        // Display pagination links
        echo "<div style='margin-top: 20px;'>";
        if ($page_num > 1) {
            echo '<a href="?action=view&page=1">First</a> ';
            echo '<a href="?action=view&page='.($page_num - 1).'">Previous</a> ';
        }

        // Display page numbers
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
