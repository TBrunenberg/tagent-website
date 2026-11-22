/* Kader – mini-runtime voor de HTML-export.
   Leest de template (#dc-tpl) en de logica (#dc-logic) van een pagina,
   rendert die, en werkt de pagina bij met een kleine DOM-morph bij elke state-wijziging. */
(function () {
  'use strict';
  var tpl = document.getElementById('dc-tpl');
  var logicEl = document.getElementById('dc-logic');
  var root = document.getElementById('dc-root');
  if (!root) return;
  if (!tpl && !root.hasAttribute('data-static')) return;

  var props = {};
  if (logicEl && logicEl.getAttribute('data-props')) {
    try {
      var decl = JSON.parse(logicEl.getAttribute('data-props'));
      Object.keys(decl).forEach(function (k) { if (k[0] !== '$' && decl[k] && 'default' in decl[k]) props[k] = decl[k].default; });
    } catch (e) { /* geen props */ }
  }

  var skipRender = false;
  function DCLogic(p) { this.props = p || {}; this.state = {}; }
  DCLogic.prototype.setState = function (patch, cb) {
    var next = typeof patch === 'function' ? patch(this.state, this.props) : patch;
    this.state = Object.assign({}, this.state, next);
    if (!skipRender) render();
    if (typeof cb === 'function') cb();
  };
  DCLogic.prototype.forceUpdate = function () { render(); };

  var Component;
  try {
    Component = new Function('DCLogic', (logicEl ? logicEl.textContent : '') + '\n;return typeof Component !== "undefined" ? Component : null;')(DCLogic);
  } catch (e) { console.error('Kader runtime: logica kon niet laden', e); }
  var inst = Component ? new Component(props) : { renderVals: function () { return {}; } };
  if (!inst.props) inst.props = props;
  if (!inst.state) inst.state = {};

  /* ---------- waarden opzoeken ---------- */
  function lookup(path, ctx) {
    path = path.trim();
    if (path === 'true') return true;
    if (path === 'false') return false;
    if (path === 'null') return null;
    if (/^-?\d+(\.\d+)?$/.test(path)) return parseFloat(path);
    var parts = path.split('.');
    var v = ctx;
    for (var i = 0; i < parts.length; i++) {
      if (v == null) return undefined;
      v = v[parts[i]];
    }
    return v;
  }
  var whole = /^\s*\{\{([^{}]+)\}\}\s*$/;
  function interp(str, ctx) {
    return str.replace(/\{\{([^{}]+)\}\}/g, function (_, p) {
      var v = lookup(p, ctx);
      return v == null ? '' : String(v);
    });
  }

  /* ---------- template uitvouwen naar losse DOM-nodes ---------- */
  function build(node, ctx, out) {
    if (node.nodeType === 3) {
      out.push(document.createTextNode(interp(node.nodeValue, ctx)));
      return;
    }
    if (node.nodeType !== 1) return;
    var tag = node.localName;
    if (tag === 'sc-for') {
      var list = lookup((node.getAttribute('list') || '').replace(/[{}]/g, ''), ctx) || [];
      var as = node.getAttribute('as') || 'item';
      for (var i = 0; i < list.length; i++) {
        var c = Object.create(ctx);
        c[as] = list[i];
        c.$index = i;
        kids(node, c, out);
      }
      return;
    }
    if (tag === 'sc-if') {
      var val = lookup((node.getAttribute('value') || '').replace(/[{}]/g, ''), ctx);
      if (val) kids(node, ctx, out);
      return;
    }
    if (tag === 'helmet') return;
    var el = node.namespaceURI && node.namespaceURI !== 'http://www.w3.org/1999/xhtml'
      ? document.createElementNS(node.namespaceURI, node.tagName)
      : document.createElement(tag);
    el.__h = {};
    for (var a = 0; a < node.attributes.length; a++) {
      var at = node.attributes[a];
      var name = at.name;
      if (name.indexOf('hint-') === 0) continue;
      var m = at.value.match(whole);
      if (/^on[a-z]+$/.test(name)) {
        if (m) {
          var fn = lookup(m[1], ctx);
          if (typeof fn === 'function') el.__h[name.slice(2)] = fn;
        }
        continue;
      }
      var value;
      if (m) {
        var raw = lookup(m[1], ctx);
        if (raw === false || raw == null) continue;
        value = raw === true ? '' : String(raw);
      } else {
        value = interp(at.value, ctx);
      }
      if (at.namespaceURI) el.setAttributeNS(at.namespaceURI, name, value);
      else el.setAttribute(name, value);
    }
    var src = tag === 'template' ? node.content : node;
    var ch = [];
    kids(src, ctx, ch);
    for (var k = 0; k < ch.length; k++) el.appendChild(ch[k]);
    out.push(el);
  }
  function kids(node, ctx, out) {
    for (var n = node.firstChild; n; n = n.nextSibling) build(n, ctx, out);
  }

  /* ---------- events (één listener per type, handlers per element) ---------- */
  var bound = {};
  function ensureListener(type) {
    if (bound[type]) return;
    bound[type] = true;
    root.addEventListener(type, function (e) {
      var t = e.target;
      while (t && t !== root) {
        if (t.__h && t.__h[type]) {
          skipRender = type === 'input';
          try { t.__h[type](e); } finally { skipRender = false; }
          return;
        }
        t = t.parentNode;
      }
    }, type === 'focus' || type === 'blur');
  }
  function collectEvents(el) {
    if (el.__h) Object.keys(el.__h).forEach(ensureListener);
    for (var c = el.firstChild; c; c = c.nextSibling) if (c.nodeType === 1) collectEvents(c);
  }

  /* ---------- morph: bestaande DOM bijwerken i.p.v. vervangen ---------- */
  function same(a, b) {
    return a.nodeType === b.nodeType && (a.nodeType !== 1 || (a.namespaceURI === b.namespaceURI && a.tagName === b.tagName));
  }
  function patchAttrs(oldEl, newEl) {
    var i, at;
    for (i = oldEl.attributes.length - 1; i >= 0; i--) {
      at = oldEl.attributes[i];
      if (!newEl.hasAttribute(at.name)) oldEl.removeAttribute(at.name);
    }
    for (i = 0; i < newEl.attributes.length; i++) {
      at = newEl.attributes[i];
      if (oldEl.getAttribute(at.name) !== at.value) oldEl.setAttribute(at.name, at.value);
    }
    oldEl.__h = newEl.__h;
  }
  function morph(parent, nextList) {
    var cur = parent.firstChild;
    for (var i = 0; i < nextList.length; i++) {
      var nx = nextList[i];
      if (cur && same(cur, nx)) {
        if (cur.nodeType === 3) {
          if (cur.nodeValue !== nx.nodeValue) cur.nodeValue = nx.nodeValue;
        } else {
          patchAttrs(cur, nx);
          var nkids = [];
          while (nx.firstChild) { nkids.push(nx.firstChild); nx.removeChild(nx.firstChild); }
          morph(cur, nkids);
        }
        cur = cur.nextSibling;
      } else if (cur) {
        parent.insertBefore(nx, cur);
      } else {
        parent.appendChild(nx);
      }
    }
    while (cur) { var nxt = cur.nextSibling; parent.removeChild(cur); cur = nxt; }
  }

  /* ---------- render ---------- */
  var first = true;
  var staticPage = root.hasAttribute('data-static');
  function render() {
    if (staticPage) {
      /* Inhoud staat al in de HTML (vooraf opgebouwd): alleen gedrag koppelen. */
      if (first) { first = false; if (typeof inst.componentDidMount === 'function') inst.componentDidMount(); }
      return;
    }
    var vals = (inst.renderVals && inst.renderVals()) || {};
    var out = [];
    kids(tpl.content, vals, out);
    if (first && !root.firstElementChild) {
      for (var i = 0; i < out.length; i++) root.appendChild(out[i]);
    } else {
      /* Vooraf opgebouwde HTML of een update: bestaande DOM bijwerken. */
      morph(root, out);
    }
    collectEvents(root);
    if (first) {
      first = false;
      if (typeof inst.componentDidMount === 'function') inst.componentDidMount();
    }
  }
  render();
  function toTop() {
    if (location.hash) { var el = document.getElementById(location.hash.slice(1)); if (el) { el.scrollIntoView(); return; } }
    var b = root.style.scrollBehavior; root.style.scrollBehavior = 'auto';
    root.scrollTop = 0; window.scrollTo(0, 0);
    root.style.scrollBehavior = b;
  }
  toTop();
  window.addEventListener('pageshow', toTop);
})();
