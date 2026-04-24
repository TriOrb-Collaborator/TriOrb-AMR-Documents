(() => {
  const isMqttApiPage = () => /\/packages\/mqtt\.html$/.test(window.location.pathname);

  const isPlainLeftClick = (event) =>
    event.button === 0 && !event.metaKey && !event.ctrlKey && !event.shiftKey && !event.altKey;

  const ros2ApiLink = (target) => {
    const anchor = target.closest?.(".content a[href], article a[href]");
    if (!anchor) {
      return null;
    }

    const href = anchor.getAttribute("href") || "";
    if (!/\/API\.html(?:#.*)?$/.test(href)) {
      return null;
    }
    return anchor;
  };

  const ensureModal = () => {
    let modal = document.getElementById("mqtt-api-modal");
    if (modal) {
      return modal;
    }

    modal = document.createElement("div");
    modal.id = "mqtt-api-modal";
    modal.className = "mqtt-api-modal";
    modal.hidden = true;
    modal.innerHTML = `
      <div class="mqtt-api-modal__backdrop" data-mqtt-modal-close></div>
      <section class="mqtt-api-modal__dialog" role="dialog" aria-modal="true" aria-labelledby="mqtt-api-modal-title">
        <header class="mqtt-api-modal__header">
          <div>
            <p class="mqtt-api-modal__eyebrow">ROS2 API reference</p>
            <h2 id="mqtt-api-modal-title">ROS2 API</h2>
          </div>
          <div class="mqtt-api-modal__actions">
            <a class="mqtt-api-modal__open" href="#" target="_blank" rel="noopener">別タブで開く</a>
            <button class="mqtt-api-modal__close" type="button" aria-label="閉じる" data-mqtt-modal-close>×</button>
          </div>
        </header>
        <iframe class="mqtt-api-modal__frame" title="ROS2 API"></iframe>
      </section>
    `;
    document.body.appendChild(modal);

    modal.addEventListener("click", (event) => {
      if (event.target.closest("[data-mqtt-modal-close]")) {
        closeModal();
      }
    });

    return modal;
  };

  const closeModal = () => {
    const modal = document.getElementById("mqtt-api-modal");
    if (!modal) {
      return;
    }
    modal.hidden = true;
    document.documentElement.classList.remove("mqtt-api-modal-open");
    modal.querySelector("iframe").setAttribute("src", "about:blank");
  };

  const openModal = (anchor) => {
    const modal = ensureModal();
    const title = anchor.textContent.trim() || "ROS2 API";
    const frame = modal.querySelector("iframe");
    const openLink = modal.querySelector(".mqtt-api-modal__open");

    modal.querySelector("#mqtt-api-modal-title").textContent = title;
    frame.setAttribute("src", anchor.href);
    openLink.setAttribute("href", anchor.href);
    modal.hidden = false;
    document.documentElement.classList.add("mqtt-api-modal-open");
    modal.querySelector(".mqtt-api-modal__close").focus();
  };

  document.addEventListener("click", (event) => {
    if (!isMqttApiPage() || !isPlainLeftClick(event)) {
      return;
    }

    const anchor = ros2ApiLink(event.target);
    if (!anchor) {
      return;
    }

    event.preventDefault();
    openModal(anchor);
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
      closeModal();
    }
  });
})();
