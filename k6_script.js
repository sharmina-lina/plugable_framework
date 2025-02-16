// k6_script.js
/*
import http from 'k6/http';
import { check, sleep } from 'k6';

export default function () {
    // Define the URL of the frontend service
    let url = 'http://localhost:8080';

    // Send a GET request to the frontend service
    let res = http.get(url);

    // Check if the response status is 200
    check(res, {
        'is status 200': (r) => r.status === 200,
    });

    // Sleep for 1 second between iterations
    sleep(1);
} */

import http from 'k6/http';
import { check, sleep } from 'k6';
import { randomIntBetween } from 'k6/utils';

export let options = {
    stages: [
        { duration: '30s', target: 50 },  // Ramp up to 50 users over 30 seconds
        { duration: '1m', target: 100 },  // Stay at 100 users for 1 minute
        { duration: '30s', target: 0 },   // Ramp down to 0 users over 30 seconds
    ],
};

export default function () {
    let url = 'http://localhost:8080/cart';
    let payload = JSON.stringify({
        id: randomIntBetween(1, 100),
        value: `test_value_${randomIntBetween(1, 100)}`,
    });

    let res = http.post(url, payload, {
        headers: { 'Content-Type': 'application/json' },
    });

    check(res, {
        'is status 200': (r) => r.status === 200,
        'response body contains "success"': (r) => r.body.includes('success'),
    });

    sleep(1);
}
