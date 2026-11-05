export async function onRequestGet(context) {
  const url = new URL(context.request.url);
  const assetRes = await context.env.ASSETS.fetch(new URL('/latest.json', url.origin));
  const newHeaders = new Headers(assetRes.headers);
  newHeaders.set('Content-Type', 'application/json; charset=utf-8');
  newHeaders.set('Access-Control-Allow-Origin', '*');
  newHeaders.set('Cache-Control', 'public, max-age=60');

  return new Response(assetRes.body, {
    status: assetRes.status,
    headers: newHeaders,
  });
}
