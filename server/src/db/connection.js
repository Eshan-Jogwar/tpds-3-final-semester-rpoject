const Database = require('better-sqlite3');
const fs = require('fs');
const path = require('path');

const dbPath = process.env.DATABASE_PATH || path.join(__dirname, '../../../data/campuspulse.db');
const dbDir = path.dirname(dbPath);

if (!fs.existsSync(dbDir)) {
  fs.mkdirSync(dbDir, { recursive: true });
}

const db = new Database(dbPath, {
  // verbose: process.env.NODE_ENV === 'development' ? console.log : null
});

// Configure essential SQLite performance and integrity PRAGMAs
db.pragma('foreign_keys = ON');
db.pragma('journal_mode = WAL');
db.pragma('busy_timeout = 5000');

function initializeDatabase() {
  const tableCheck = db.prepare("SELECT name FROM sqlite_master WHERE type='table' AND name='tickets'").get();
  if (!tableCheck) {
    console.log('[DB] Fresh database detected. Executing schema.sql and seed.sql...');
    const schemaSql = fs.readFileSync(path.join(__dirname, 'schema.sql'), 'utf-8');
    db.exec(schemaSql);

    const seedSql = fs.readFileSync(path.join(__dirname, 'seed.sql'), 'utf-8');
    db.exec(seedSql);
    console.log('[DB] Database successfully initialized with 3NF tables, views, and seed data.');
  }
}

initializeDatabase();

module.exports = db;
