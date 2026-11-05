export async function onRequestGet(context) {
  const url = new URL(context.request.url);
  const assetRes = await context.env.ASSETS.fetch(new URL('/catalog.json', url.origin));
  const newHeaders = new Headers(assetRes.headers);
  newHeaders.set('Content-Type', 'application/json; charset=utf-8');
  newHeaders.set('Access-Control-Allow-Origin', '*');

  return new Response(assetRes.body, {
    status: assetRes.status,
    headers: newHeaders,
  });
}
