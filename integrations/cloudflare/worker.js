/**
 * Cloudflare Worker to block IPs from HFish Threat Feed
 */
const FEED_URL = "https://yuexuan521.github.io/honeypot-blocklist/ip_list.txt";

addEventListener('fetch', event => {
  event.respondWith(handleRequest(event.request))
})

async function handleRequest(request) {
  const clientIP = request.headers.get('CF-Connecting-IP');

  // Fetch and cache the list (Cache for 1 hour)
  let blocklist = await fetch(FEED_URL, { cf: { cacheTtl: 3600 } }).then(r => r.text());
  
  // Check if client IP is in the list
  if (blocklist.includes(clientIP)) {
    return new Response('Access Denied: Your IP is listed in HFish Threat Feed.', {
      status: 403,
      statusText: 'Forbidden'
    });
  }

  return fetch(request);
}
