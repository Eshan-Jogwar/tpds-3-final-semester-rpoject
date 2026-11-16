// Automated Test Suite for CampusPulse REST API (Guideline 7: Test with Evidence)

const assert = require('assert');
const http = require('http');
const app = require('../server/src/app');

let server;
const PORT = 5055;
const BASE_URL = `http://localhost:${PORT}/api/v1`;

function makeRequest(method, path, body = null) {
  return new Promise((resolve, reject) => {
    const url = new URL(BASE_URL + path);
    const options = {
      method,
      hostname: url.hostname,
      port: url.port,
      path: url.pathname + url.search,
      headers: {
        'Content-Type': 'application/json'
      }
    };

    const req = http.request(options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const parsed = JSON.parse(data);
          resolve({ status: res.statusCode, body: parsed });
        } catch (e) {
          resolve({ status: res.statusCode, raw: data });
        }
      });
    });

    req.on('error', reject);

    if (body) {
      req.write(JSON.stringify(body));
    }
    req.end();
  });
}

async function runTests() {
  console.log('=== Starting CampusPulse Empirical Test Suite (Guideline 7) ===\n');
  let passed = 0;
  let failed = 0;

  server = app.listen(PORT);

  try {
    // TC-01: Healthcheck
    {
      const res = await makeRequest('GET', '/health');
      assert.strictEqual(res.status, 200);
      assert.strictEqual(res.body.status, 'healthy');
      assert.strictEqual(res.body.database, 'SQLite (On-Disk, Serverless)');
      console.log('✔ TC-01: Healthcheck endpoint returns 200 and healthy SQLite status.');
      passed++;
    }

    // TC-02: Normal Case - Create valid ticket
    let createdUuid;
    {
      const payload = {
        title: 'Broken Lab Stool in Lab 302',
        description: 'One of the rolling stools has a missing caster wheel.',
        category: 'furniture',
        urgency_level: 'medium',
        facility_id: 1,
        created_by: 1
      };
      const res = await makeRequest('POST', '/tickets', payload);
      assert.strictEqual(res.status, 201);
      assert.strictEqual(res.body.success, true);
      assert(res.body.ticket_uuid);
      createdUuid = res.body.ticket_uuid;
      console.log(`✔ TC-02: Normal Case - Ticket lodged successfully with UUID: ${createdUuid}`);
      passed++;
    }

    // TC-03: Retrieve Ticket by UUID with Audit Log
    {
      const res = await makeRequest('GET', `/tickets/${createdUuid}`);
      assert.strictEqual(res.status, 200);
      assert.strictEqual(res.body.data.ticket_uuid, createdUuid);
      assert.strictEqual(res.body.data.status, 'submitted');
      assert(res.body.data.timeline.length >= 1);
      console.log('✔ TC-03: Retrieve Ticket - Verified ticket details and audit trail.');
      passed++;
    }

    // TC-04: Boundary Case - Description too short (<10 chars)
    {
      const payload = {
        title: 'Short description test',
        description: 'Too short',
        category: 'plumbing',
        urgency_level: 'low',
        facility_id: 1
      };
      const res = await makeRequest('POST', '/tickets', payload);
      assert.strictEqual(res.status, 400);
      assert.strictEqual(res.body.success, false);
      console.log('✔ TC-04: Boundary Case - Rejected description with <10 characters (HTTP 400).');
      passed++;
    }

    // TC-05: Boundary Case - Title too long (>200 chars)
    {
      const payload = {
        title: 'A'.repeat(201),
        description: 'Valid long description for boundary testing purposes.',
        category: 'electrical',
        urgency_level: 'low',
        facility_id: 1
      };
      const res = await makeRequest('POST', '/tickets', payload);
      assert.strictEqual(res.status, 400);
      assert.strictEqual(res.body.success, false);
      console.log('✔ TC-05: Boundary Case - Rejected title with >200 characters (HTTP 400).');
      passed++;
    }

    // TC-06: Error / Invalid Input - Missing category
    {
      const payload = {
        title: 'Missing category test',
        description: 'Valid description for testing missing required fields.',
        urgency_level: 'low',
        facility_id: 1
      };
      const res = await makeRequest('POST', '/tickets', payload);
      assert.strictEqual(res.status, 400);
      assert.strictEqual(res.body.success, false);
      console.log('✔ TC-06: Error Input - Rejected payload with missing category (HTTP 400).');
      passed++;
    }

    // TC-07: Transition status (Atomic transaction & Audit write)
    {
      const payload = {
        status: 'resolved',
        remarks: 'Replaced missing caster with spare in storage.',
        changed_by: 4
      };
      const res = await makeRequest('PATCH', `/tickets/${createdUuid}/status`, payload);
      assert.strictEqual(res.status, 200);
      assert.strictEqual(res.body.success, true);

      // Verify updated status
      const checkRes = await makeRequest('GET', `/tickets/${createdUuid}`);
      assert.strictEqual(checkRes.body.data.status, 'resolved');
      assert.strictEqual(checkRes.body.data.timeline.length, 2);
      console.log('✔ TC-07: Atomic Status Transition - Verified ticket marked resolved with audit trail.');
      passed++;
    }

    // TC-08: Analytics KPIs aggregation
    {
      const res = await makeRequest('GET', '/analytics/kpis');
      assert.strictEqual(res.status, 200);
      assert(res.body.data.total_tickets > 0);
      assert(typeof res.body.data.sla_compliance_rate === 'number');
      console.log('✔ TC-08: Analytics Module - Verified KPI calculation and SLA compliance metrics.');
      passed++;
    }

    console.log(`\n=======================================================`);
    console.log(`Test Execution Summary: ${passed} passed, ${failed} failed.`);
    console.log(`All criteria strictly validated against project guidelines!`);
    console.log(`=======================================================\n`);
  } catch (err) {
    console.error('Test Failed with assertion error:', err);
    failed++;
  } finally {
    server.close();
    process.exit(failed > 0 ? 1 : 0);
  }
}

runTests();
