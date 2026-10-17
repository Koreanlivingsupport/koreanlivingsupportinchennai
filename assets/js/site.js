/* Korean Living Support – finder tabs, home-search chips, Seoul–Chennai globe */
(function () {
  var WA = "https://wa.me/917985040232?text=";

  /* ---------- Finder tabs ---------- */
  var tabs = document.querySelectorAll(".finder-tabs [role=tab]");
  tabs.forEach(function (tab) {
    tab.addEventListener("click", function () {
      tabs.forEach(function (t) {
        var on = t === tab;
        t.setAttribute("aria-selected", on ? "true" : "false");
        t.tabIndex = on ? 0 : -1;
        var panel = document.getElementById(t.getAttribute("aria-controls"));
        if (panel) panel.hidden = !on;
      });
    });
    tab.addEventListener("keydown", function (e) {
      if (e.key !== "ArrowRight" && e.key !== "ArrowLeft") return;
      var list = Array.prototype.slice.call(tabs);
      var i = list.indexOf(tab) + (e.key === "ArrowRight" ? 1 : -1);
      var next = list[(i + list.length) % list.length];
      next.focus(); next.click();
    });
  });

  /* ---------- Home search chips -> WhatsApp brief ---------- */
  var finder = document.querySelector("[data-home-finder]");
  if (finder) {
    var link = finder.querySelector("[data-home-link]");
    var update = function () {
      var lines = [finder.getAttribute("data-intro")];
      finder.querySelectorAll("[data-field]").forEach(function (group) {
        var on = group.querySelector(".chip[aria-pressed=true]");
        if (on) lines.push("- " + group.getAttribute("data-label") + ": " + on.textContent.trim());
      });
      link.href = WA + encodeURIComponent(lines.join("\n"));
    };
    finder.querySelectorAll("[data-field]").forEach(function (group) {
      group.querySelectorAll(".chip").forEach(function (chip) {
        chip.addEventListener("click", function () {
          group.querySelectorAll(".chip").forEach(function (c) { c.setAttribute("aria-pressed", c === chip ? "true" : "false"); });
          update();
        });
      });
    });
    update();
  }

  /* ---------- Globe ---------- */
  var canvas = document.querySelector("[data-globe]");
  if (!canvas || !canvas.getContext) return;
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var ctx = canvas.getContext("2d");
  var D = Math.PI / 180;
  var A = { lat: 37.57 * D, lon: 126.98 * D }, B = { lat: 13.08 * D, lon: 80.27 * D };
  function vec(q) { return [Math.cos(q.lat) * Math.cos(q.lon), Math.cos(q.lat) * Math.sin(q.lon), Math.sin(q.lat)]; }
  var va = vec(A), vb = vec(B);
  var om = Math.acos(va[0] * vb[0] + va[1] * vb[1] + va[2] * vb[2]);
  var visible = true;
  if ("IntersectionObserver" in window) {
    new IntersectionObserver(function (es) { visible = es[0].isIntersecting; if (visible && !reduce) requestAnimationFrame(frame); }).observe(canvas);
  }

  function draw(t) {
    var S = canvas.clientWidth || 420, dpr = window.devicePixelRatio || 1, px = Math.round(S * dpr);
    if (canvas.width !== px) { canvas.width = px; canvas.height = px; }
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    var cx = S / 2, cy = S / 2, R = S * 0.4;
    var lon0 = (104 + 16 * Math.sin(t * 0.00022)) * D, lat0 = 18 * D;
    ctx.clearRect(0, 0, S, S);
    function rot(lat, lon, h) {
      var x = Math.cos(lat) * Math.cos(lon), y = Math.cos(lat) * Math.sin(lon), z = Math.sin(lat);
      var cl = Math.cos(-lon0), sl = Math.sin(-lon0);
      var x1 = x * cl - y * sl, y1 = x * sl + y * cl;
      var ca = Math.cos(lat0), sa = Math.sin(lat0);
      var x2 = x1 * ca + z * sa, z2 = -x1 * sa + z * ca;
      h = h || 1;
      return { X: cx + R * h * y1, Y: cy - R * h * z2, d: x2 };
    }
    var halo = ctx.createRadialGradient(cx, cy, R * 0.92, cx, cy, R * 1.3);
    halo.addColorStop(0, "rgba(141,181,166,0.28)"); halo.addColorStop(1, "rgba(141,181,166,0)");
    ctx.fillStyle = halo; ctx.beginPath(); ctx.arc(cx, cy, R * 1.3, 0, 7); ctx.fill();
    var g = ctx.createRadialGradient(cx - R * 0.35, cy - R * 0.4, R * 0.1, cx, cy, R);
    g.addColorStop(0, "#2B5C9E"); g.addColorStop(0.6, "#173A6E"); g.addColorStop(1, "#0A1A33");
    ctx.fillStyle = g; ctx.beginPath(); ctx.arc(cx, cy, R, 0, 7); ctx.fill();
    for (var la = -78; la <= 78; la += 5) {
      var step = 5 / Math.max(0.25, Math.cos(la * D));
      for (var lo = -180; lo < 180; lo += step) {
        var p = rot(la * D, lo * D);
        if (p.d > 0) {
          ctx.fillStyle = "rgba(228,239,235," + (0.1 + 0.55 * p.d).toFixed(3) + ")";
          ctx.beginPath(); ctx.arc(p.X, p.Y, 0.9 + 0.7 * p.d, 0, 7); ctx.fill();
        }
      }
    }
    function along(s) {
      var k1 = Math.sin((1 - s) * om) / Math.sin(om), k2 = Math.sin(s * om) / Math.sin(om);
      var v = [k1 * va[0] + k2 * vb[0], k1 * va[1] + k2 * vb[1], k1 * va[2] + k2 * vb[2]];
      return rot(Math.asin(v[2]), Math.atan2(v[1], v[0]), 1 + 0.24 * Math.sin(Math.PI * s));
    }
    ctx.lineWidth = 3; ctx.lineCap = "round"; ctx.strokeStyle = "rgba(242,167,59,0.95)";
    var prev = along(0);
    for (var i = 1; i <= 90; i++) {
      var cur = along(i / 90);
      if (Math.min(prev.d, cur.d) > -0.15) { ctx.beginPath(); ctx.moveTo(prev.X, prev.Y); ctx.lineTo(cur.X, cur.Y); ctx.stroke(); }
      prev = cur;
    }
    if (!reduce) {
      var pp = along((t * 0.00032) % 1);
      if (pp.d > -0.15) {
        ctx.fillStyle = "rgba(255,255,255,0.25)"; ctx.beginPath(); ctx.arc(pp.X, pp.Y, 10, 0, 7); ctx.fill();
        ctx.fillStyle = "#fff"; ctx.beginPath(); ctx.arc(pp.X, pp.Y, 4.5, 0, 7); ctx.fill();
      }
    }
    function city(q, color, label, dx) {
      var p = rot(q.lat, q.lon);
      if (p.d <= 0) return;
      ctx.fillStyle = color; ctx.globalAlpha = 0.28;
      ctx.beginPath(); ctx.arc(p.X, p.Y, 11 + 3 * Math.sin(t * 0.004), 0, 7); ctx.fill();
      ctx.globalAlpha = 1; ctx.beginPath(); ctx.arc(p.X, p.Y, 6, 0, 7); ctx.fill();
      ctx.strokeStyle = "#fff"; ctx.lineWidth = 2; ctx.stroke();
      ctx.font = "600 15px 'IBM Plex Sans KR', sans-serif";
      ctx.textBaseline = "middle"; ctx.textAlign = dx > 0 ? "left" : "right";
      ctx.lineWidth = 5; ctx.strokeStyle = "rgba(10,26,51,0.9)"; ctx.strokeText(label, p.X + dx, p.Y);
      ctx.fillStyle = "#fff"; ctx.fillText(label, p.X + dx, p.Y);
    }
    city(A, "#8DB5A6", "서울 Seoul", 14);
    city(B, "#F2A73B", "Chennai 첸나이", -14);
  }
  function frame(t) {
    draw(t || 0);
    if (!reduce && visible) requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);
  window.addEventListener("resize", function () { if (reduce) draw(0); });
})();
