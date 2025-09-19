# VG-Frankensteiner Anything Engine — Component Index

The **VG-Frankensteiner_v2_active** canvas is a two-page automation lab. Page one (Input Configuration) lets creators describe a desired "engine" in natural language, load reference banks, and fine-tune generation flags before hitting the Magic Box. Page two (Execution & Results) then exposes up to ten bots that can remix, extend, or critique the generated pipeline.

## Experience Map
- **Magic Box (Genie)** – Accepts a freeform description plus optional file, chosen model, and target bot count, then calls Poe to design a JSON engine template with live streaming feedback.
- **Three Banks System** – Dedicated uploaders for Keys (techniques), Input payloads, and Prompt templates with status chips, previews, and download/export utilities.
- **Execution Deck** – Ten themed bot panels, each with accordion-based model pickers, prompt health indicators, optional flag controls, execution buttons, and output transcript drawers.
- **Global Utilities** – Persistent nav buttons for state save/load/export, a processing log timeline, per-bot clipboard/download helpers, and toggles for showing/hiding inactive bots.

## Key Modules Extracted
1. **Magic Box Layout & Flow** – `magic_box.md` captures the HTML controls, the full Genie architect prompt, and the JavaScript for executing the engine, handling streamed JSON, and revealing model-specific flags.
2. **Accordion Model Picker** – `accordion_manager.md` documents the rebuilt accordion selector tailored for this app (with dual display/search states, provider/series toggles, and keyboard support).
3. **Flag Manager** – `flag_manager.md` explains how dynamic tuning forms are injected per model, covering both Magic Box-wide and bot-specific flag containers.
4. **Bot Panel Template** – `bot_panel_template.md` shows the reusable layout for each bot card, including status headings, prompt slots, execution controls, and output management bar.

Each document blends the lifted template/code with usage notes so both builders and day-to-day operators can navigate the system confidently without touching the original canvas file.
