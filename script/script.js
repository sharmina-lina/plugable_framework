
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
    vus: 10, // Number of Virtual Users
    duration: '10s', // Test runs for 10 seconds
    thresholds: {
        http_req_duration: ['p(95)<500'], // Ensure 95% of requests complete under 500ms
    },
};

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
    sleep(Math.random() * 2.8 + 0.5);
}

    