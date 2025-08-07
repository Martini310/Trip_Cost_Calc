const originalAttachShadow = Element.prototype.attachShadow;

Element.prototype.attachShadow = function (init) {
  if (this.localName === 'gmp-place-autocomplete') {
    const shadow = originalAttachShadow.call(this, {
      ...init,
      mode: 'open'
    });

    const style = document.createElement('style');
    style.textContent = `
      input {
        background-color: white !important;
        color: #1f2937 !important; /* text-gray-800 */
        font-size: 1.1rem;
        padding: 0;
        border-radius: 0.5rem;
      }
      .widget-container {
        border: none !important;
      }
      .focus-ring {
        display: none !important;
      }
      ul {
        border: none !important;
        background: white !important;
        border-radius: 0.5rem;
      }
      li {
        padding: 0 !important;
        border-radius: 0.5rem !important;
      }
      .place-autocomplete-element-row .place-autocomplete-element-text-div .place-autocomplete-element-place-result--matched {
        color: black !important
      }
      .place-autocomplete-element-row .place-autocomplete-element-text-div .place-autocomplete-element-place-name {
        color: rgb(145, 145, 145) !important
      }
      li:hover {
        background-color: #e5e7eb !important; /* Tailwind gray-200 */
      }
    `;
    shadow.appendChild(style);
    return shadow;
  }

  return originalAttachShadow.call(this, init);
};