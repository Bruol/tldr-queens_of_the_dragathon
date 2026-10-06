import topics from './search.json';

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (/^\/download\/\d+\/$/.test(url.pathname)) {
      url.pathname = url.pathname.slice(0, -1);
      return env.ASSETS.fetch(new Request(url, request));
    }
    if (url.pathname !== '/search' && url.pathname !== '/search/') {
      return env.ASSETS.fetch(request);
    }
    if (!['GET', 'HEAD'].includes(request.method)) {
      return new Response('Method not allowed', { status: 405, headers: { Allow: 'GET, HEAD' } });
    }
    if (url.pathname === '/search') {
      url.pathname = '/search/';
      return Response.redirect(url, 301);
    }
    const query = url.searchParams.get('query') || '';
    // SQLite's default LIKE comparison folds ASCII letters only.
    const fold = value => value.replace(/[A-Z]/g, char => char.toLowerCase());
    const matches = new Set(topics.filter(topic => fold(topic.summary).includes(fold(query))).map(topic => String(topic.id)));
    const assetUrl = new URL('/search/', url);
    const response = await env.ASSETS.fetch(new Request(assetUrl, request));
    return new HTMLRewriter()
      .on('[data-topic-id]', { element(element) { if (!matches.has(element.getAttribute('data-topic-id'))) element.remove(); } })
      .on('input[name="query"]', { element(element) { element.setAttribute('value', query); } })
      .on('#no-results', { element(element) { if (!matches.size) element.removeAttribute('hidden'); } })
      .transform(response);
  }
};
