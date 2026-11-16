const app = require('./app');

const PORT = process.env.PORT || 5000;

app.listen(PORT, () => {
  console.log(`=======================================================`);
  console.log(` CampusPulse Server is running!`);
  console.log(` Port:    http://localhost:${PORT}`);
  console.log(` Student: http://localhost:${PORT}/index.html`);
  console.log(` Admin:   http://localhost:${PORT}/admin.html`);
  console.log(` BI Dash: http://localhost:${PORT}/analytics.html`);
  console.log(` Health:  http://localhost:${PORT}/api/v1/health`);
  console.log(`=======================================================`);
});
