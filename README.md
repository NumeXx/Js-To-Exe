# Js-To-Exe
Simple Tools to Convert JS-TO-EXE (Coded in Python 3.x)

# DONATION
<pre>
<span class="pl-k">&gt;</spam><a href="https://www.paypal.com/paypalme/NumeXGans" rel="nofollow"><code> Paypal</code></a>
<span class="pl-k">&gt;</spam> Gopay : 082198256727 - NumeX Gans
</pre>
import express from 'express';
import session from 'express-session';
import sqlite3 from 'sqlite3';
import bcrypt from 'bcrypt';
import passport from 'passport';
import LocalStrategy from 'passport-local';
import { fileURLToPath } from 'url';
import { dirname } from 'path';
import { createServer } from 'http';
import { renderFile } from 'ejs';

const app = express();
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const db = new sqlite3.Database('database.db');

app.use(express.urlencoded({ extended: true }));
app.use(session({ secret: 'your_secret_key', resave: false, saveUninitialized: true }));
app.use(passport.initialize());
app.use(passport.session());
app.set('view engine', 'ejs');
app.set('views', __dirname + '/views');

passport.use(new LocalStrategy((username, password, done) => {
    db.get("SELECT * FROM users WHERE username = ?", [username], (err, user) => {
        if (err) return done(err);
        if (!user) return done(null, false, { message: 'Incorrect username.' });
        bcrypt.compare(password, user.password, (err, res) => {
            if (res) return done(null, user);
            return done(null, false, { message: 'Incorrect password.' });
        });
    });
}));

passport.serializeUser((user, done) => {
    done(null, user.id);
});

passport.deserializeUser((id, done) => {
    db.get("SELECT * FROM users WHERE id = ?", [id], (err, user) => {
        done(err, user);
    });
});

function initSqliteDb() {
    db.serialize(() => {
        db.run(`CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )`);
        db.run(`CREATE TABLE IF NOT EXISTS kpi (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            target_value TEXT NOT NULL,
            responsible_department TEXT NOT NULL,
            reporting_frequency TEXT NOT NULL,
            user_id INTEGER,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )`);
    });
}

initSqliteDb();

app.get('/register', (req, res) => {
    res.render('register');
});

app.post('/register', (req, res) => {
    const { username, password } = req.body;
    const hashedPassword = bcrypt.hashSync(password, 10);
    db.run("INSERT INTO users (username, password) VALUES (?, ?)", [username, hashedPassword], (err) => {
        if (err) {
            console.error(err.message);
            return res.redirect('/register');
        }
        res.redirect('/login');
    });
});

app.get('/login', (req, res) => {
    res.render('login');
});

app.post('/login', passport.authenticate('local', {
    successRedirect: '/',
    failureRedirect: '/login',
    failureFlash: true
}));

app.get('/logout', (req, res) => {
    req.logout();
    res.redirect('/login');
});

app.get('/', (req, res) => {
    if (!req.isAuthenticated()) return res.redirect('/login');
    db.all("SELECT * FROM kpi WHERE user_id = ?", [req.user.id], (err, kpis) => {
        res.render('index', { kpis });
    });
});

app.get('/add-kpi', (req, res) => {
    if (!req.isAuthenticated()) return res.redirect('/login');
    res.render('kpi');
});

app.post('/add-kpi', (req, res) => {
    const { name, description, target_value, responsible_department, reporting_frequency } = req.body;
    db.run("INSERT INTO kpi (name, description, target_value, responsible_department, reporting_frequency, user_id) VALUES (?, ?, ?, ?, ?, ?)", 
        [name, description, target_value, responsible_department, reporting_frequency, req.user.id], (err) => {
            if (err) {
                console.error(err.message);
                return res.redirect('/add-kpi');
            }
            res.redirect('/');
        });
});

app.get('/edit-kpi/:kpi_id', (req, res) => {
    if (!req.isAuthenticated()) return res.redirect('/login');
    db.get("SELECT * FROM kpi WHERE id=? AND user_id=?", [req.params.kpi_id, req.user.id], (err, kpi) => {
        res.render('kpi', { kpi });
    });
});

app.post('/edit-kpi/:kpi_id', (req, res) => {
    const { name, description, target_value, responsible_department, reporting_frequency } = req.body;
    db.run("UPDATE kpi SET name=?, description=?, target_value=?, responsible_department=?, reporting_frequency=? WHERE id=? AND user_id=?", 
        [name, description, target_value, responsible_department, reporting_frequency, req.params.kpi_id, req.user.id], (err) => {
            if (err) {
                console.error(err.message);
                return res.redirect(`/edit-kpi/${req.params.kpi_id}`);
            }
            res.redirect('/');
        });
});

app.get('/delete-kpi/:kpi_id', (req, res) => {
    db.run("DELETE FROM kpi WHERE id=? AND user_id=?", [req.params.kpi_id, req.user.id], (err) => {
        if (err) {
            console.error(err.message);
        }
        res.redirect('/');
    });
});

app.get('/kpi-stats', (req, res) => {
    if (!req.isAuthenticated()) return res.redirect('/login');
    db.all("SELECT target_value FROM kpi WHERE user_id = ?", [req.user.id], (err, kpi_data) => {
        const values = kpi_data.map(kpi => parseInt(kpi.target_value.replace('%', '')));
        // Here you would generate the plot and encode it in base64
        // For simplicity, we will just render a placeholder
        res.render('kpi_stats', { plot_url: 'data:image/png;base64,PLACEHOLDER' });
    });
});

app.get('/filter-kpi', (req, res) => {
    if (!req.isAuthenticated()) return res.redirect('/login');
    res.render('filter_kpi');
});

app.post('/filter-kpi', (req, res) => {
    const { department } = req.body;
    db.all("SELECT * FROM kpi WHERE responsible_department = ? AND user_id = ?", [department, req.user.id], (err, kpis) => {
        res.render('index', { kpis });
    });
});

const server = createServer(app);
server.listen(3000, () => {
    console.log('Server is running on http://localhost:3000');
});
