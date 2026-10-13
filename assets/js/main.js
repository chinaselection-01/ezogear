/* EZO Gear — catalog rendering, product modal & quote form.
   IMPORTANT: prices (item.fob) are NEVER rendered anywhere on the site. */
(function () {
  const P = window.PRODUCTS || { tables: [], chairs: [] };

  /* ---------- Card builders ---------- */
  function tableCard(t) {
    const tagClass = t.accent === "led" ? "tag led" : "tag";
    const tagText = { electric: "Electric", manual: "Manual", fixed: "Fixed", led: "LED" }[t.accent] || "";
    return `
    <article class="card" data-type="table" data-sku="${t.sku}">
      <div class="thumb"><img src="${t.img}" alt="${t.sku}" loading="lazy"></div>
      <div class="body">
        <div class="sku">${t.sku}</div>
        <div class="sub">${t.size}</div>
        <div class="spec">${t.desc}</div>
        <div class="foot">
          <span class="${tagClass}">${tagText}</span>
          <span class="sub">MOQ ${t.moq || "on request"}</span>
        </div>
      </div>
    </article>`;
  }

  function chairCard(c) {
    return `
    <article class="card" data-type="chair" data-sku="${c.sku}">
      <div class="thumb"><img src="${c.cover}" alt="${c.sku}" loading="lazy"></div>
      <div class="body">
        <div class="sku">${c.sku}</div>
        <div class="sub">${c.color}</div>
        <div class="spec">${c.desc}</div>
        <div class="foot">
          <span class="tag">Gaming Chair</span>
          <span class="sub">MOQ ${c.moq || "on request"}</span>
        </div>
      </div>
    </article>`;
  }

  /* ---------- Leisure / office chairs page (with filter chips) ---------- */
  function leisureCard(c) {
    return `
    <article class="card" data-type="leisure" data-sku="${c.sku}">
      <div class="thumb"><img src="${c.cover}" alt="${c.sku}" loading="lazy"></div>
      <div class="body">
        <div class="sku">${c.sku}</div>
        <div class="sub">${c.name}</div>
        <div class="spec">${c.desc}</div>
        <div class="foot">
          <span class="tag">${c.name}</span>
          <span class="sub">MOQ ${c.moq || "on request"}</span>
        </div>
      </div>
    </article>`;
  }

  function initLeisure() {
    const grid = document.getElementById("grid");
    if (!grid) return;
    const chips = document.querySelectorAll(".chip");
    function show(filter) {
      const items = P.leisure.filter((t) => filter === "all" || t.cat === filter);
      grid.innerHTML = items.map(leisureCard).join("");
      bindCards();
    }
    chips.forEach((c) => c.addEventListener("click", () => {
      chips.forEach((x) => x.classList.remove("active"));
      c.classList.add("active");
      show(c.dataset.filter);
    }));
    show("all");
  }

  /* ---------- Tables page (with filter chips) ---------- */
  function initTables() {
    const grid = document.getElementById("grid");
    if (!grid) return;
    const chips = document.querySelectorAll(".chip");
    function show(filter) {
      const items = P.tables.filter((t) => filter === "all" || t.accent === filter);
      grid.innerHTML = items.map(tableCard).join("");
      bindCards();
    }
    chips.forEach((c) => c.addEventListener("click", () => {
      chips.forEach((x) => x.classList.remove("active"));
      c.classList.add("active");
      show(c.dataset.filter);
    }));
    show("all");
  }

  /* ---------- Chairs page ---------- */
  function initChairs() {
    const grid = document.getElementById("grid");
    if (!grid) return;
    grid.innerHTML = P.chairs.map(chairCard).join("");
    bindCards();
  }

  /* ---------- Modal ---------- */
  let modalItem = null;
  function bindCards() {
    document.querySelectorAll(".card").forEach((card) => {
      card.addEventListener("click", () => {
        const type = card.dataset.type;
        const sku = card.dataset.sku;
        const src = type === "table" ? P.tables : type === "leisure" ? P.leisure : P.chairs;
        const item = src.find((x) => x.sku === sku);
        openModal(type, item);
      });
    });
  }

  function openModal(type, item) {
    const back = document.getElementById("modalBack");
    const modal = document.getElementById("modal");
    modalItem = item;
    let galleryHtml = "";
    if (type !== "table") {
      const g = item.gallery || [item.cover];
      galleryHtml = `
        <div class="gallery">
          <div class="main"><img id="mMain" src="${g[0]}" alt=""></div>
          <div class="thumbs">
            ${g.map((src, i) => `<img class="${i === 0 ? "active" : ""}" src="${src}" data-i="${i}" alt="">`).join("")}
          </div>
        </div>`;
    } else {
      const g = item.gallery || [item.img];
      galleryHtml = `
        <div class="gallery">
          <div class="main"><img id="mMain" src="${g[0]}" alt=""></div>
          <div class="thumbs">
            ${g.map((src, i) => `<img class="${i === 0 ? "active" : ""}" src="${src}" data-i="${i}" alt="">`).join("")}
          </div>
        </div>`;
    }
    const extra = [
      item.type ? `<li><strong>Type:</strong> ${item.type}</li>` : "",
      item.color ? `<li><strong>Colors:</strong> ${item.color}</li>` : "",
      item.material ? `<li><strong>Material:</strong> ${item.material}</li>` : "",
      item.net ? `<li><strong>Weight:</strong> ${item.net}${item.gross ? " net / " + item.gross + " gross" : ""}</li>` : "",
      item.carton ? `<li><strong>Carton:</strong> ${item.carton}</li>` : "",
    ].join("");
    const specs = type === "table"
      ? `<ul>
           <li><strong>Model:</strong> ${item.sku}</li>
           <li><strong>Size:</strong> ${item.size}</li>
           <li><strong>Adjustment:</strong> ${item.adj}</li>
           <li><strong>Feature:</strong> ${item.desc}</li>
           ${extra}
           <li><strong>MOQ:</strong> ${item.moq ? item.moq + " pcs" : "On request"}</li>
         </ul>`
      : type === "leisure"
      ? `<ul>
           <li><strong>Model:</strong> ${item.sku}</li>
           <li><strong>Type:</strong> ${item.name}</li>
           <li><strong>Feature:</strong> ${item.desc}</li>
           <li><strong>MOQ:</strong> ${item.moq ? item.moq + " pcs" : "On request"}</li>
           <li><strong>Colors:</strong> Multiple options, contact for availability</li>
         </ul>`
      : `<ul>
           <li><strong>Model:</strong> ${item.sku}</li>
           <li><strong>Color:</strong> ${item.color}</li>
           <li><strong>Feature:</strong> ${item.desc}</li>
           <li><strong>MOQ:</strong> ${item.moq ? item.moq + " pcs" : "On request"}</li>
         </ul>`;
    modal.innerHTML = `
      <div class="modal-wrap">
        <div class="close" id="mClose">&times;</div>
        ${galleryHtml}
        <div class="info">
          <h3>${item.sku}</h3>
          <div class="sku">${type === "table" ? "Gaming Desk" : type === "leisure" ? "Office & Leisure Chair" : "Gaming Chair"}</div>
          ${specs}
          <button class="btn btn-primary" id="mQuote">Get a Quote</button>
        </div>
      </div>`;
    back.classList.add("open");
    document.body.style.overflow = "hidden";

    const close = () => { back.classList.remove("open"); document.body.style.overflow = ""; };
    document.getElementById("mClose").addEventListener("click", close);
    back.addEventListener("click", (e) => { if (e.target === back) close(); });
    document.getElementById("mQuote").addEventListener("click", () => {
      close();
      window.location.href = "contact.html?sku=" + encodeURIComponent(item.sku);
    });
    modal.querySelectorAll(".thumbs img").forEach((th) => {
      th.addEventListener("click", () => {
        document.getElementById("mMain").src = th.src;
        modal.querySelectorAll(".thumbs img").forEach((x) => x.classList.remove("active"));
        th.classList.add("active");
      });
    });
  }

  /* ---------- Contact / quote form ---------- */
  function initContact() {
    const form = document.getElementById("quoteForm");
    if (!form) return;
    const ta = document.getElementById("products");
    const params = new URLSearchParams(location.search);
    const sku = params.get("sku");
    if (sku) ta.value = "Interested in model: " + sku + "\n";

    const SALES_EMAIL = "bob@ezogear.com"; // TODO: replace with your real sales mailbox
    form.addEventListener("submit", (e) => {
      e.preventDefault();
      const name = form.name.value.trim();
      const company = form.company.value.trim();
      const email = form.email.value.trim();
      const country = form.country.value.trim();
      const msg = ta.value.trim();
      const subject = "Quote request from " + (company || name || "Website");
      const body =
        "Name: " + name + "\n" +
        "Company: " + company + "\n" +
        "Email: " + email + "\n" +
        "Country: " + country + "\n" +
        "--------------------------------\n" +
        msg + "\n";
      window.location.href = "mailto:" + SALES_EMAIL + "?subject=" +
        encodeURIComponent(subject) + "&body=" + encodeURIComponent(body);
    });
  }

  /* ---------- Boot ---------- */
  document.addEventListener("DOMContentLoaded", () => {
    /* tables.html 与 chairs.html 共用 id="grid"，必须按页面特征二选一，
       否则后执行的 initChairs 会把 tables 页的桌子覆盖成椅子 */
    const gridEl = document.getElementById("grid");
    if (gridEl && gridEl.dataset.cat === "leisure") {
      initLeisure();         // leisure.html（data-cat 标记优先）
    } else if (document.querySelector(".chip")) {
      initTables();          // tables.html（带筛选 chips）
    } else if (gridEl) {
      initChairs();          // chairs.html
    }
    initContact();
  });
})();
